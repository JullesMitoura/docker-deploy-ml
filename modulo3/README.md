<div align="center">

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>


<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
     alt="Python"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg"
     alt="Docker"
     width="80"
     height="80"/>
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg"
     alt="scikit-learn"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Modulo 03: Separando treino e inferência
> Entrega: dois containers com responsabilidades claras

---

## O problema do módulo anterior

No módulo 02, treino e inferência rodavam no mesmo container. Isso funcionou como workaround, mas viola um princípio fundamental de engenharia de software: **responsabilidade única**.

```bash
# Módulo 02 — gambeta: tudo num container só
docker run heat-exchanger-train \
  sh -c "python src/train.py && python src/inference.py --date 2022-04-15"
```

**Por que isso é um problema em produção?**

| Problema | Impacto |
|----------|---------|
| Treino e inferência têm ciclos de vida diferentes | Re-treinar força rebuild da imagem de serving |
| Dependências misturadas | Imagem maior do que o necessário |
| Escala independente impossível | Não dá pra rodar 10x inferência e 1x treino |
| Rastreabilidade prejudicada | Qual versão do modelo está em cada container? |

---

## A solução: dois containers, um volume

```
┌─────────────────────┐        volume: ./models/        ┌──────────────────────────┐
│  heat-exchanger-    │  ──── model.pkl ────────────►  │  heat-exchanger-         │
│  train              │                                  │  inference               │
│                     │                                  │                          │
│  src/train.py       │                                  │  src/inference.py        │
│  data/              │                                  │  (sem data/)             │
│  sqlalchemy ✓       │                                  │  sqlalchemy ✗            │
└─────────────────────┘                                  └──────────────────────────┘
```

O **volume** Docker é o elo entre os dois containers: o treino escreve o `model.pkl` em um diretório do host, e a inferência lê desse mesmo diretório.

---

## Separação de dependências

| Dependência | Treino | Inferência | Por quê |
|-------------|:------:|:----------:|---------|
| `scikit-learn` | ✓ | ✓ | Treino e deserialização do modelo |
| `pandas` | ✓ | ✓ | Carga de dados e manipulação de datas |
| `numpy` | ✓ | ✓ | Operações vetoriais |
| `sqlalchemy` | ✓ | ✗ | Inferência não lê banco de dados |

Remover `sqlalchemy` da imagem de inferência reduz dependências e **diminui a superfície de ataque**.

---

## Estrutura dos arquivos deste módulo

```
modulo3/
├── Dockerfile.train        # container de treino (acessa dados, gera modelo)
├── Dockerfile.inference    # container de inferência (lê modelo via volume)
├── .dockerignore           # o que NÃO entra nas imagens
├── requirements-train.txt  # scikit-learn + pandas + numpy + sqlalchemy
├── requirements-inference.txt  # scikit-learn + pandas + numpy
├── src/
│   ├── train.py            # pipeline de treino
│   ├── inference.py        # inferência com erro claro se volume não montado
│   └── utils/
│       └── logger.py       # logger configurável via LOG_LEVEL
├── data/
│   └── heat_exchanger.db   # banco SQLite com os dados
└── models/                 # artefatos gerados — compartilhados via volume
```

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo3
```

### 2. Build das imagens

Cada imagem tem seu próprio Dockerfile:

```bash
# Imagem de treino
docker build -f Dockerfile.train -t heat-exchanger-train .

# Imagem de inferência
docker build -f Dockerfile.inference -t heat-exchanger-inference .
```

Verifique as imagens criadas:
```bash
docker images | grep heat-exchanger
```

### 3. Execute o treino com volume

O flag `-v` monta o diretório local `./models` dentro do container em `/app/models`. O `model.pkl` gerado persiste no host após o container parar.

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-train
```

Saída esperada:
```
2022-01-01 00:00:00 | INFO     | Conectando ao banco: data/heat_exchanger.db
2022-01-01 00:00:00 | INFO     | Dados carregados: 175 registros | período: 2022-01-01 → 2022-06-30
2022-01-01 00:00:00 | INFO     | Iniciando treino — modelo: LinearRegression
2022-01-01 00:00:00 | INFO     | Treino concluído — coef=-0.017900  intercept=96.4500
2022-01-01 00:00:00 | INFO     | MAE=0.0397%  RMSE=0.0469%  R²=0.9975  R²_CV=0.9974±0.0003  Tendência=-0.0179%/dia
2022-01-01 00:00:00 | INFO     | Modelo salvo: models/model.pkl
```

Confirme que o artefato foi gerado no host:
```bash
ls -lh models/
# -rw-r--r--  model.pkl
```

### 4. Execute a inferência com volume

O mesmo volume montado no treino torna o `model.pkl` disponível para o container de inferência — sem cópia, sem rebuild.

```bash
# Modo 1 — prever eficiência para uma data
docker run -v $(pwd)/models:/app/models heat-exchanger-inference \
  python src/inference.py --date 2022-04-15

# Modo 2 — estimar data para uma eficiência alvo
docker run -v $(pwd)/models:/app/models heat-exchanger-inference \
  python src/inference.py --efficiency 94.5
```

### 5. O que acontece sem o volume?

```bash
docker run heat-exchanger-inference python src/inference.py --date 2022-04-15
```

```
FileNotFoundError: Modelo não encontrado em: models/model.pkl
Monte o volume com o modelo treinado:
  docker run -v $(pwd)/models:/app/models heat-exchanger-inference ...
```

A mensagem de erro agora é explícita e orienta o usuário — diferente do módulo anterior.

---

## Entendendo volumes

```
Host (sua máquina)          Container
──────────────────          ─────────────────────────
./models/           ◄────►  /app/models/
  model.pkl                   model.pkl
```

| Característica | Comportamento |
|----------------|---------------|
| **Persistência** | Arquivos sobrevivem ao container parar |
| **Compartilhamento** | Múltiplos containers podem montar o mesmo volume |
| **Bidirecional** | Container lê e escreve no diretório do host |
| **Independência** | Modelo e código têm ciclos de vida separados |

---

## Comparação: módulo 02 vs módulo 03

| | Módulo 02 | Módulo 03 |
|---|---|---|
| Dockerfiles | 1 (unificado) | 2 (treino e inferência) |
| Requirements | 1 arquivo | 2 arquivos (dependências separadas) |
| Modelo | Gerado e consumido no mesmo container | Compartilhado via volume |
| Persistência | Não (container efêmero) | Sim (volume no host) |
| Escalabilidade | Não | Sim (containers independentes) |
| sqlalchemy em inferência | Sim (desnecessário) | Não (imagem menor) |

---

## Checklist de Entrega

- [ ] `docker build -f Dockerfile.train` conclui sem erros
- [ ] `docker build -f Dockerfile.inference` conclui sem erros
- [ ] `docker run -v $(pwd)/models:/app/models heat-exchanger-train` gera o `model.pkl` no host
- [ ] `docker run -v $(pwd)/models:/app/models heat-exchanger-inference python src/inference.py --date ...` retorna a predição
- [ ] `docker run heat-exchanger-inference python src/inference.py --date ...` (sem volume) falha com mensagem clara
- [ ] Entendeu a diferença entre os dois `requirements*.txt`
- [ ] Entendeu como o volume conecta os dois containers

---
