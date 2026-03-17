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

## Modulo 02: Containerizando o projeto
> Entrega: projeto rodando em container

---

## Contexto: os problemas que o Docker resolve

Na Aula 01 você rodou o projeto localmente e provavelmente esbarrou em algum desses erros:

```
ModuleNotFoundError: No module named 'sklearn'
AttributeError: module 'sklearn.metrics' has no attribute 'root_mean_squared_error'
FileNotFoundError: data/heat_exchanger.db
```

Todos eles têm a mesma raiz: **o ambiente da sua máquina não é o ambiente de produção**. O Docker resolve isso empacotando código, dependências e configuração em uma única unidade reproduzível chamada **imagem**.

---

## Conceitos-chave antes de começar

| Conceito | O que é |
|----------|---------|
| **Imagem** | Snapshot imutável do ambiente (sistema + dependências + código) |
| **Container** | Instância em execução de uma imagem — efêmero por padrão |
| **Dockerfile** | Receita de instruções para construir uma imagem |
| **Build** | Processo de transformar o Dockerfile em imagem |
| **Layer** | Cada instrução do Dockerfile gera uma camada; camadas são cacheadas |

---

## O Dockerfile explicado linha a linha

```dockerfile
FROM python:3.13-slim
```
Define a imagem base. `python:3.13-slim` é o Python oficial em cima de um Debian mínimo (~50 MB vs ~1 GB da versão `full`). Sempre prefira `slim` para produção.

```dockerfile
WORKDIR /app
```
Define o diretório de trabalho dentro do container. Todos os caminhos relativos subsequentes partem daqui. Equivale a um `cd /app` permanente.

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
Copiamos o `requirements.txt` **antes** do código-fonte. Isso não é acidente — é estratégia de cache:

```
Se requirements.txt não mudou → Docker reutiliza a camada do pip install
Se só o código mudou         → pip install não é re-executado
```

O flag `--no-cache-dir` evita que o pip armazene o cache de download dentro da imagem, mantendo-a menor.

```dockerfile
COPY src/  src/
COPY data/ data/
```
Copia apenas o que o container precisa para funcionar. O `.dockerignore` garante que `.venv/`, `models/` e outros artefatos não entrem na imagem.

```dockerfile
ENV DB_PATH=data/heat_exchanger.db \
    MODEL_DIR=models \
    LOG_LEVEL=INFO
```
Define variáveis de ambiente com valores padrão. Podem ser sobrescritas em runtime sem precisar reconstruir a imagem.

```dockerfile
CMD ["python", "src/train.py"]
```
Comando padrão executado quando o container sobe. Diferente de `RUN` (que executa no build), `CMD` executa em runtime. Pode ser sobrescrito ao chamar `docker run`.

---

## Estrutura dos arquivos deste módulo

```
modulo2/
├── Dockerfile            # receita da imagem
├── .dockerignore         # o que NÃO deve entrar na imagem
├── requirements.txt      # dependências fixadas com versão
├── src/
│   ├── train.py          # pipeline de treino (idêntico ao modulo1)
│   └── inference.py      # inferência (idêntico ao modulo1)
├── data/
│   └── heat_exchanger.db # banco SQLite com os dados
└── models/               # artefatos gerados (vazios no repositório)
```

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo2
```

### 2. Faça o build da imagem

```bash
docker build -t heat-exchanger-train .
```

O que acontece:
- Docker lê o `Dockerfile` linha a linha
- Cada instrução vira uma camada cacheada
- Ao final, uma imagem chamada `heat-exchanger-train` fica disponível localmente

Verifique que a imagem foi criada:
```bash
docker images | grep heat-exchanger-train
```

### 3. Execute o treino

```bash
docker run heat-exchanger-train
```

Saída esperada:
```
2022-01-01 00:00:00 | INFO     | Conectando ao banco: data/heat_exchanger.db
2022-01-01 00:00:00 | INFO     | Dados carregados: 175 registros | período: 2022-01-01 → 2022-06-30
2022-01-01 00:00:00 | INFO     | Iniciando treino — modelo: LinearRegression
2022-01-01 00:00:00 | INFO     | Treino concluído — coef=-0.017900  intercept=96.4500
2022-01-01 00:00:00 | INFO     | MAE=0.0397%  RMSE=0.0469%  R²=0.9975  ...
2022-01-01 00:00:00 | INFO     | Modelo salvo: models/model.pkl
```

### 4. Sobrescrevendo variáveis de ambiente

Você pode alterar o comportamento do container sem reconstruir a imagem:

```bash
# Aumentar verbosidade dos logs
docker run -e LOG_LEVEL=DEBUG heat-exchanger-train

# Apontar para outro banco de dados
docker run -e DB_PATH=data/outro_banco.db heat-exchanger-train
```

### 5. Executando a inferência

Para rodar a inferência, sobrescreva o `CMD` padrão:

```bash
# Modo 1 — prever eficiência para uma data
docker run heat-exchanger-train python src/inference.py --date 2022-04-15

# Modo 2 — encontrar datas para uma eficiência alvo
docker run heat-exchanger-train python src/inference.py --efficiency 94.5
```

---

## O problema da efemeridade

Você pode ter notado um comportamento inesperado: ao rodar a inferência em um container separado do treino, o modelo não é encontrado:

```
FileNotFoundError: Modelo não encontrado em: models/model.pkl
```

**Por quê?** Containers são efêmeros. O modelo gerado pelo container de treino vive apenas dentro daquele container — quando ele para, os arquivos desaparecem.

Para rodar treino + inferência sem volumes, execute tudo em um único container:

```bash
docker run heat-exchanger-train \
  sh -c "python src/train.py && python src/inference.py --date 2022-04-15"
```

Isso funciona, mas é um workaround. A solução correta — separar o artefato do container — é o tema da **Aula 05** (volumes).

---

## Build otimizado: entendendo o cache

Experimente alterar uma linha em `src/train.py` e fazer o build novamente:

```bash
docker build -t heat-exchanger-train .
```

Observe no output as linhas com `CACHED`:
```
 => CACHED [2/5] WORKDIR /app
 => CACHED [3/5] COPY requirements.txt .
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt   ← reutilizado!
 => [5/5] COPY src/ src/                                               ← re-executado
```

O `pip install` não rodou de novo porque `requirements.txt` não mudou. Se você alterar o `requirements.txt`, toda a cadeia abaixo dele é invalidada e re-executada.

---

## Comparação: local vs container

| | Local (modulo1) | Container (modulo2) |
|---|---|---|
| Ambiente | Depende do seu Python | Python 3.13-slim fixado |
| Dependências | `.venv` local | Instaladas na imagem |
| Portabilidade | Só na sua máquina | Qualquer host com Docker |
| Reprodutibilidade | Depende do SO | Garantida pela imagem |
| Artefatos | Persistem em `models/` | Efêmeros no container |

---

## Checklist de Entrega

- [ ] `docker build` conclui sem erros
- [ ] `docker run` executa o treino e imprime as métricas
- [ ] `docker run -e LOG_LEVEL=DEBUG` altera o nível de log sem rebuild
- [ ] Inferência executada sobrescrevendo o CMD
- [ ] Entendeu por que o modelo "desaparece" entre containers

---

## Próximo passo → Aula 03

Na próxima aula vamos separar treino e inferência em **dois Dockerfiles distintos**, cada um com suas próprias dependências e responsabilidades — o primeiro passo para um pipeline de ML de verdade.
