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

## Modulo 04: Otimização de imagens para ML
> Entrega: imagens menores e mais rápidas

---

## O problema do módulo anterior

No módulo 03 as imagens funcionam, mas carregam mais do que precisam. O processo de `pip install` inclui compiladores, ferramentas de build e cache que não têm utilidade em runtime.

```bash
# Tamanho das imagens do módulo 03 (single-stage)
docker images | grep heat-exchanger
# heat-exchanger-train      ~780 MB
# heat-exchanger-inference  ~710 MB
```

Imagens grandes têm custo real em produção: mais tempo de pull, mais banda, mais espaço em registros, maior superfície de ataque.

---

## Multi-stage build

O multi-stage build resolve isso ao separar a construção em etapas independentes. A imagem final parte do zero — apenas os artefatos explicitamente copiados do stage anterior entram nela.

```
Stage 1: builder                    Stage 2: runtime
─────────────────────────           ─────────────────────────
python:3.11-slim                    python:3.11-slim  (nova, zerada)
  + gcc (compilador)                  + pacotes copiados de /install
  + pip install → /install            + src/
  + cache de download                 + data/  (apenas no train)
                                      ← sem gcc
                                      ← sem cache de pip
                                      ← sem ferramentas de build
```

O `gcc` e o cache de download existem apenas no builder — eles **nunca chegam à imagem final**.

---

## Como o multi-stage funciona

```dockerfile
# Stage 1 — instala tudo, incluindo ferramentas de compilação
FROM python:3.11-slim AS builder

RUN apt-get install -y gcc
RUN pip install --prefix=/install -r requirements.txt

# Stage 2 — imagem final, parte do zero
FROM python:3.11-slim

# Copia apenas os pacotes instalados — gcc fica de fora
COPY --from=builder /install /usr/local
COPY src/ src/
```

`--prefix=/install` direciona o `pip install` para `/build/install` em vez do Python global do builder. O `COPY --from=builder /install /usr/local` transporta apenas esse diretório para a imagem final, mapeando corretamente para o Python do runtime.

---

## .dockerignore aprimorado

O `.dockerignore` deste módulo é mais completo que o dos anteriores. Cada categoria excluída reduz o **contexto de build** — o conjunto de arquivos enviados ao daemon Docker antes do primeiro `FROM`.

```
Módulo 02 .dockerignore: 7 linhas  → contexto ~15 MB (com dados)
Módulo 04 .dockerignore: 50 linhas → contexto ~13 MB (mesmo projeto, menos lixo)
```

Categorias adicionadas:
- `*.pkl`, `*.joblib`, `*.h5`, `*.pt`, `*.onnx` — formatos de modelo
- `notebooks/`, `*.ipynb` — não fazem parte do container de produção
- `.vscode/`, `.idea/` — configurações de IDE
- `.env`, `.env.*` — variáveis de ambiente locais (nunca devem entrar na imagem)
- `tests/`, `.pytest_cache/` — artefatos de teste

---

## Cache de dependências: a ordem importa

O Docker invalida o cache de uma camada se qualquer camada anterior mudou. A estratégia de copiar `requirements.txt` antes do código-fonte maximiza o reuso do cache:

```dockerfile
COPY requirements-train.txt .           # camada 3
RUN pip install -r requirements-train.txt  # camada 4 — cache válido se req não mudou

COPY src/ src/                          # camada 5 — mudanças aqui NÃO invalidam pip install
COPY data/ data/                        # camada 6
```

```
Cenário: você editou src/train.py
  ✓ CACHED  [builder 1/4] RUN apt-get install gcc
  ✓ CACHED  [builder 2/4] COPY requirements-train.txt
  ✓ CACHED  [builder 3/4] RUN pip install          ← reutilizado!
  ✗ [runtime 1/2] COPY src/                        ← re-executado (arquivo mudou)

Cenário: você adicionou uma dependência em requirements-train.txt
  ✓ CACHED  [builder 1/4] RUN apt-get install gcc
  ✗ [builder 2/4] COPY requirements-train.txt      ← invalidado
  ✗ [builder 3/4] RUN pip install                  ← re-executado (req mudou)
  ✗ [runtime 1/2] COPY src/                        ← re-executado
```

---

## Estrutura dos arquivos deste módulo

```
modulo4/
├── Dockerfile.train        # multi-stage: builder + runtime para treino
├── Dockerfile.inference    # multi-stage: builder + runtime para inferência
├── .dockerignore           # mais completo: notebooks, .env, IDEs, formatos de modelo
├── requirements-train.txt  # scikit-learn + pandas + numpy + sqlalchemy
├── requirements-inference.txt  # scikit-learn + pandas + numpy
├── src/
│   ├── train.py            # pipeline de treino (idêntico ao módulo 03)
│   ├── inference.py        # inferência (idêntico ao módulo 03)
│   └── utils/
│       └── logger.py       # logger configurável via LOG_LEVEL
├── data/
│   └── heat_exchanger.db   # banco SQLite com os dados
└── models/                 # artefatos gerados — compartilhados via volume
```

> O código Python não muda entre módulos — a evolução está na infraestrutura Docker.

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo4
```

### 2. Build das imagens (multi-stage)

```bash
docker build -f Dockerfile.train     -t heat-exchanger-train-v4 .
docker build -f Dockerfile.inference -t heat-exchanger-inference-v4 .
```

Observe no output os dois stages sendo executados:
```
[+] Building ...
 => [builder 1/4] FROM python:3.11-slim
 => [builder 2/4] RUN apt-get install -y gcc
 => [builder 3/4] COPY requirements-train.txt .
 => [builder 4/4] RUN pip install --prefix=/install ...
 => [runtime 1/3] FROM python:3.11-slim              ← nova imagem, zerada
 => [runtime 2/3] COPY --from=builder /install /usr/local
 => [runtime 3/3] COPY src/ src/
```

### 3. Compare o tamanho das imagens

```bash
docker images | grep heat-exchanger
```

Resultado esperado:
```
REPOSITORY                    TAG     SIZE
heat-exchanger-train-v4       latest  ~430 MB   ← módulo 04
heat-exchanger-inference-v4   latest  ~390 MB   ← módulo 04
heat-exchanger-train          latest  ~780 MB   ← módulo 03
heat-exchanger-inference      latest  ~710 MB   ← módulo 03
```

### 4. Execute o treino

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-train-v4
```

### 5. Execute a inferência

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-inference-v4 \
  python src/inference.py --date 2022-04-15

docker run -v $(pwd)/models:/app/models heat-exchanger-inference-v4 \
  python src/inference.py --efficiency 94.5
```

### 6. Observe o cache em ação

Edite uma linha em `src/train.py` e rebuilde:

```bash
docker build -f Dockerfile.train -t heat-exchanger-train-v4 .
```

O `pip install` não será re-executado — o cache da camada é reutilizado.

---

## Comparação: antes vs depois

| | Módulo 03 (single-stage) | Módulo 04 (multi-stage) |
|---|---|---|
| Imagem de treino | ~780 MB | ~430 MB |
| Imagem de inferência | ~710 MB | ~390 MB |
| gcc na imagem final | Sim | Não |
| Cache de pip na imagem | Sim | Não |
| Funcionalidade | Idêntica | Idêntica |
| .dockerignore | 7 linhas | ~50 linhas |

---

## Por que imagens menores importam em produção

| Benefício | Impacto prático |
|-----------|-----------------|
| **Pull mais rápido** | Deploy em segundos, não minutos |
| **Menos banda** | Custo menor em registros de imagem na nuvem |
| **Menor superfície de ataque** | Sem compiladores = menos vetores de exploit |
| **Cache mais eficiente** | Camadas menores = mais reutilização entre builds |
| **Startup mais rápido** | Container inicia em menos tempo (menos para extrair) |

---

## Checklist de Entrega

- [ ] `docker build -f Dockerfile.train` conclui com dois stages visíveis no output
- [ ] `docker build -f Dockerfile.inference` conclui com dois stages visíveis no output
- [ ] Tamanho das imagens v4 é menor que as do módulo 03
- [ ] `docker run -v ...` executa treino e gera `model.pkl` no host
- [ ] Inferência com volume retorna predições corretamente
- [ ] Rebuild após editar `src/train.py` reutiliza cache do `pip install`
- [ ] Entendeu por que `gcc` não aparece na imagem final
- [ ] Entendeu a diferença entre o `.dockerignore` deste módulo e o do anterior

---
