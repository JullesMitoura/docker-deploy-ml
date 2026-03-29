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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/githubactions/githubactions-original.svg"
     alt="GitHub Actions"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Modulo 06: Pipeline de build com GitHub Actions
> Entrega: CI funcionando

---

## O problema do módulo anterior

Até agora, todo o fluxo  build, teste, execução  acontece manualmente na sua máquina. Isso cria um problema em equipes:

- Quem garante que a imagem que foi para produção foi buildada corretamente?
- Como saber se um PR quebrou o pipeline antes de fazer merge?
- Como reproduzir o build em qualquer máquina sem depender do ambiente local?

**CI (Continuous Integration)** resolve isso: a cada push, o pipeline roda automaticamente  mesma sequência, mesmo ambiente, resultados verificáveis.

---

## O workflow de CI

O arquivo `.github/workflows/modulo6-ci.yml` define o pipeline:

```
Push para main (modulo6/**)
        │
        ▼
┌───────────────────┐    ┌───────────────────┐
│  build-train      │    │  build-inference  │  ← rodam em PARALELO
│  (ubuntu-latest)  │    │  (ubuntu-latest)  │
└────────┬──────────┘    └────────┬──────────┘
         │                        │
         └──────────┬─────────────┘
                    ▼
         ┌──────────────────┐
         │  test            │  ← só começa após AMBOS os builds
         │  (ubuntu-latest) │
         └──────────────────┘
```

### Job `build-train`
1. Checkout do repositório
2. Configura Docker Buildx
3. Builda `Dockerfile.train` com cache do GitHub Actions (scope=train)
4. Exporta imagem como tarball → artefato de CI

### Job `build-inference`
1. Checkout do repositório
2. Configura Docker Buildx
3. Builda `Dockerfile.inference` com cache do GitHub Actions (scope=inference)
4. Exporta imagem como tarball → artefato de CI

### Job `test` (depende dos dois builds)
1. Baixa os tarballs dos jobs anteriores
2. Carrega as imagens no Docker local
3. Executa treino → verifica `model_latest.pkl` e `registry.json`
4. Executa inferência por data
5. Executa inferência por eficiência
6. Lista versões registradas

---

## Cache de build no CI

Sem cache, cada push rebuilda tudo do zero (~3 min por imagem). Com cache:

```yaml
cache-from: type=gha,scope=train
cache-to: type=gha,scope=train,mode=max
```

- `type=gha` → usa o GitHub Actions Cache como backend
- `scope=train` → isola o cache de treino do de inferência
- `mode=max` → armazena todas as camadas intermediárias (máximo de reaproveitamento)

```
Push 1 (sem cache):     build-train  ~3 min  | build-inference  ~2 min
Push 2 (só código):     build-train  ~30 s   | build-inference  ~20 s  ← hit no pip install
Push 3 (novo req.txt):  build-train  ~3 min  | build-inference  ~2 min ← miss (camada inv.)
```

---

## Como os jobs trocam imagens

Jobs do GitHub Actions rodam em VMs independentes  não compartilham sistema de arquivos. A estratégia usada aqui:

```
build-train                    test
───────────────                ─────────────────────────────────
docker build → image           download-artifact → train.tar
docker save  → train.tar  →→→  docker load ← train.tar
upload-artifact                (imagem disponível)
```

O `upload-artifact` / `download-artifact` é o mecanismo de passagem entre jobs.

---

## Separação de jobs: por que importa

| Job separado | Benefício |
|---|---|
| `build-train` e `build-inference` em paralelo | Reduz tempo total do pipeline |
| `test` depende de ambos | Garantia: só testa se os dois builds passaram |
| Builds isolados | Falha em um não afeta o outro durante o build |
| Test job independente | Pode ser reusado em outros pipelines |

---

## Estrutura dos arquivos deste módulo

```
.github/
└── workflows/
    └── modulo6-ci.yml   # ← workflow principal

modulo6/
├── Dockerfile.train        # mesmo do módulo 05
├── Dockerfile.inference    # mesmo do módulo 05
├── .dockerignore
├── requirements-train.txt
├── requirements-inference.txt
├── src/
│   ├── train.py            # com versionamento (módulo 05)
│   ├── inference.py        # com --model-version e --list-versions
│   └── utils/
│       ├── logger.py
│       └── versioning.py
├── data/
│   └── heat_exchanger.db
└── models/
    └── .gitkeep
```

> O workflow vive em `.github/workflows/` na raiz do repositório  essa é a localização padrão que o GitHub Actions detecta automaticamente.

---

## Passo a Passo

### 1. Faça push para o GitHub

O workflow dispara automaticamente em qualquer push que altere `modulo6/**`:

```bash
git add modulo6/ .github/
git commit -m "feat: modulo 6  CI com GitHub Actions"
git push origin main
```

### 2. Acompanhe o pipeline

Na página do repositório no GitHub: **Actions** → **Modulo 6  CI Pipeline**

Você verá os três jobs com status em tempo real:

```
✓ build-train     (2m 45s)
✓ build-inference (2m 10s)
✓ test            (1m 20s)
```

### 3. Verifique o cache na segunda execução

Faça uma pequena alteração em `src/train.py` e faça push novamente. Observe o tempo dos jobs de build:

```
✓ build-train     (28s)   ← pip install cacheado
✓ build-inference (18s)   ← pip install cacheado
✓ test            (1m 20s)
```

### 4. Simule uma falha

Introduza um erro de sintaxe em `src/train.py`:

```python
def train(X, y):
    THIS WILL FAIL
```

O job `test` falha, e o PR fica bloqueado. Corrija o erro e o pipeline fica verde novamente.

### 5. Disparo manual

Na aba **Actions**, selecione **Modulo 6  CI Pipeline** e clique em **Run workflow**  graças ao `workflow_dispatch` no YAML.

---

## Anatomia do workflow YAML

```yaml
on:
  push:
    paths: ["modulo6/**"]   # só dispara se arquivos do módulo6 mudarem
  workflow_dispatch:         # permite disparo manual

jobs:
  build-train:
    runs-on: ubuntu-latest   # VM limpa a cada execução
    steps:
      - uses: actions/checkout@v4              # clona o repositório
      - uses: docker/setup-buildx-action@v3   # habilita BuildKit + cache
      - uses: docker/build-push-action@v5     # build com cache GHA
      - uses: actions/upload-artifact@v4      # exporta imagem entre jobs

  test:
    needs: [build-train, build-inference]     # barreira de dependência
    steps:
      - uses: actions/download-artifact@v4    # recebe imagens dos builds
      - run: docker load -i ...               # carrega no Docker local
      - run: docker run ...                   # executa os containers
```

---

## Checklist de Entrega

- [ ] Push disparou o workflow automaticamente
- [ ] Jobs `build-train` e `build-inference` rodaram em paralelo
- [ ] Job `test` só começou após ambos os builds concluírem
- [ ] Treino gerou `model_latest.pkl` e `registry.json` no CI
- [ ] Inferência retornou predições corretamente no CI
- [ ] Segunda execução mostrou cache hit nos jobs de build
- [ ] Entendeu como artefatos passam entre jobs (`upload/download-artifact`)
- [ ] Entendeu o papel do `needs` na ordenação de jobs

---
