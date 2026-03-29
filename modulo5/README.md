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

## Modulo 05: Gerando e versionando artefatos de modelo
> Entrega: modelo versionado fora da imagem

---

## O problema do módulo anterior

Nos módulos anteriores, o treino sempre sobrescreve `model.pkl`. Isso funciona para um primeiro deploy, mas cria um problema sério em produção:

```
Treino 1 → model.pkl  (boas métricas)
Treino 2 → model.pkl  (dados ruins, métricas piores — mas você não sabe)
```

**Você perdeu a versão anterior sem perceber.** Não há como voltar, comparar métricas entre treinos, ou saber exatamente qual modelo está em produção.

---

## A solução: separação código / modelo / dados

```
Código    → imagem Docker (versionada pelo git)
Modelo    → volume com artefatos versionados por timestamp
Dados     → banco SQLite (versionado separadamente)
```

Cada dimensão tem seu próprio ciclo de vida e mecanismo de versionamento.

---

## Estratégia de versionamento (sem ferramenta externa)

Nenhum MLflow, DVC ou ferramenta adicional. Apenas convenções simples:

### Estrutura do volume após dois treinos

```
models/
├── model_20240101_143052.pkl   ← treino 1 (imutável)
├── model_20240102_091823.pkl   ← treino 2 (imutável)
├── model_latest.pkl             ← cópia do treino mais recente
└── registry.json                ← índice com metadados
```

### registry.json

```json
{
  "latest": "20240102_091823",
  "versions": {
    "20240101_143052": {
      "file": "model_20240101_143052.pkl",
      "trained_at": "2024-01-01T14:30:52",
      "metrics": { "mae": 0.0397, "rmse": 0.0469, "r2": 0.9975, "trend": -0.017900 }
    },
    "20240102_091823": {
      "file": "model_20240102_091823.pkl",
      "trained_at": "2024-01-02T09:18:23",
      "metrics": { "mae": 0.0397, "rmse": 0.0469, "r2": 0.9975, "trend": -0.017900 }
    }
  }
}
```

### Por que timestamp e não número sequencial?

| Timestamp (YYYYMMDD_HHMMSS) | Número sequencial (v1, v2, v3) |
|-----------------------------|-------------------------------|
| Autoexplicativo — você sabe quando foi treinado | Requer estado externo para controlar o próximo número |
| Funciona em paralelo (múltiplos workers) | Colisão possível em treinos simultâneos |
| Não requer banco de dados | Requer banco de dados ou lock |

---

## Novidades no código

### `src/utils/versioning.py` (novo)

| Função | Responsabilidade |
|--------|-----------------|
| `make_version_tag()` | Gera tag `YYYYMMDD_HHMMSS` |
| `save_registry()` | Persiste metadados no `registry.json` |
| `promote_to_latest()` | Copia artefato versionado para `model_latest.pkl` |
| `resolve_model_path()` | Resolve o caminho para uma versão específica ou para latest |
| `list_versions()` | Lista versões do registry, da mais recente para a mais antiga |

### `src/train.py` — o que mudou

Cada execução agora:
1. Gera `model_{tag}.pkl` — artefato imutável com timestamp
2. Copia para `model_latest.pkl` — ponteiro sempre atualizado
3. Atualiza `registry.json` — histórico rastreável

### `src/inference.py` — o que mudou

Dois novos argumentos:
- `--model-version TAG` — carrega versão específica
- `--list-versions` — exibe todas as versões do registry

Nova variável de ambiente:
- `MODEL_VERSION` — alternativa ao argumento CLI para selecionar versão

---

## Estrutura dos arquivos deste módulo

```
modulo5/
├── Dockerfile.train        # multi-stage — gera artefatos versionados
├── Dockerfile.inference    # multi-stage — seleção de versão por argumento ou env var
├── .dockerignore
├── requirements-train.txt
├── requirements-inference.txt
├── src/
│   ├── train.py            # salva model_{tag}.pkl + model_latest.pkl + registry.json
│   ├── inference.py        # aceita --model-version e --list-versions
│   └── utils/
│       ├── logger.py
│       └── versioning.py   # NOVO: toda a lógica de versionamento
├── data/
│   └── heat_exchanger.db
└── models/                 # volume — artefatos versionados persistem aqui
```

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo5
```

### 2. Build das imagens

```bash
docker build -f Dockerfile.train     -t heat-exchanger-train .
docker build -f Dockerfile.inference -t heat-exchanger-inference .
```

### 3. Execute o treino (primeira versão)

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-train
```

Saída esperada:
```
2024-01-01 14:30:52 | INFO     | Conectando ao banco: data/heat_exchanger.db
2024-01-01 14:30:52 | INFO     | Dados carregados: 175 registros | ...
2024-01-01 14:30:52 | INFO     | Treino concluído — coef=-0.017900  intercept=96.4500
2024-01-01 14:30:52 | INFO     | MAE=0.0397%  RMSE=0.0469%  R²=0.9975  ...
2024-01-01 14:30:52 | INFO     | Artefato versionado salvo: models/model_20240101_143052.pkl
2024-01-01 14:30:52 | INFO     | Promovido para latest: models/model_latest.pkl
2024-01-01 14:30:52 | INFO     | Registry atualizado — versão: 20240101_143052
2024-01-01 14:30:52 | INFO     | Treino concluído — versão: 20240101_143052
```

Verifique os artefatos:
```bash
ls -lh models/
cat models/registry.json
```

### 4. Execute novamente para gerar uma segunda versão

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-train
```

```bash
ls -lh models/
# model_20240101_143052.pkl  ← primeira versão (preservada)
# model_20240102_091823.pkl  ← segunda versão
# model_latest.pkl            ← segunda versão (atualizada)
# registry.json               ← ambas registradas
```

### 5. Liste as versões disponíveis

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-inference \
  python src/inference.py --list-versions
```

```
INFO     | Versões disponíveis (mais recente primeiro):
INFO     |   20240102_091823 | MAE=0.0397%  R²=0.9975  treino: 2024-01-02T09:18:23 ← latest
INFO     |   20240101_143052 | MAE=0.0397%  R²=0.9975  treino: 2024-01-01T14:30:52
```

### 6. Inferência com versão mais recente (padrão)

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-inference \
  python src/inference.py --date 2022-04-15
```

### 7. Inferência com versão específica

```bash
docker run -v $(pwd)/models:/app/models heat-exchanger-inference \
  python src/inference.py --date 2022-04-15 --model-version 20240101_143052
```

### 8. Versão específica via variável de ambiente

```bash
docker run \
  -v $(pwd)/models:/app/models \
  -e MODEL_VERSION=20240101_143052 \
  heat-exchanger-inference \
  python src/inference.py --date 2022-04-15
```

---

## Boas práticas: não "embutir" o modelo errado

| Prática | Por quê |
|---------|---------|
| Modelo **nunca** entra na imagem Docker | Imagem e modelo têm ciclos de vida independentes |
| `model_latest.pkl` nunca é commitado | Artefato binário não pertence ao git |
| `registry.json` nunca é commitado | Estado de runtime, não de código |
| Versão carregada é sempre logada | Rastreabilidade: você sabe qual modelo respondeu |
| Artefatos versionados são imutáveis | Rollback imediato via `--model-version` |

---

## Rollback de versão

Se um treino novo gerar métricas piores, reverta sem rebuild:

```bash
# Inferência apontando para versão anterior
docker run -v $(pwd)/models:/app/models \
  -e MODEL_VERSION=20240101_143052 \
  heat-exchanger-inference \
  python src/inference.py --date 2022-04-15
```

Nenhuma imagem foi rebuilda. Nenhum código foi alterado.

---

## Checklist de Entrega

- [ ] `docker build -f Dockerfile.train` conclui sem erros
- [ ] `docker build -f Dockerfile.inference` conclui sem erros
- [ ] Primeiro `docker run` de treino gera `model_{tag}.pkl`, `model_latest.pkl` e `registry.json`
- [ ] Segundo `docker run` de treino adiciona nova versão sem apagar a anterior
- [ ] `--list-versions` lista ambas as versões com metadados
- [ ] Inferência com `--model-version` carrega a versão correta
- [ ] Rollback para versão anterior funciona sem rebuild
- [ ] Entendeu por que modelo, código e dados têm ciclos de vida separados

---
