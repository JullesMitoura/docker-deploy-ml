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

## Modulo 01: Setup do Projeto de Machine Learning
> **Entrega**: repositório base funcional, projeto rodando localmente (sem Docker)

---

## Contexto: Por que Docker para ML?

Antes de containerizar qualquer coisa, precisamos entender o problema que o Docker resolve.

### Aplicações tradicionais vs Projetos de ML

| Aspecto | App Tradicional | Projeto de ML |
|---------|----------------|---------------|
| Dependências | Estáveis, versionadas | Bibliotecas com dependências nativas (CUDA, BLAS, etc.) |
| Reprodutibilidade | Alta | Baixa sem controle rigoroso |
| Ambiente | Previsível | Varia entre pesquisa, treino e produção |
| Artefatos | Código | Código + modelo + dados + pré-processador |

### O problema real

Imagine esse cenário:

```
Cientista de dados → treina modelo no laptop (Python 3.10, sklearn 1.3)
Engenheiro de ML   → tenta rodar em servidor (Python 3.8, sklearn 1.1)
Resultado          → erro, comportamento diferente, ou pior: resultados diferentes
```

**Docker resolve isso**: empacota o código, as dependências e o ambiente numa imagem reproduzível.

### Principais vantagens do Docker para ML

- **Reprodutibilidade**: mesma imagem = mesmo resultado, sempre
- **Isolamento**: sem conflito entre projetos ou versões de biblioteca
- **Portabilidade**: roda igual no laptop, no servidor, na nuvem
- **Rastreabilidade**: imagem taggeada = versão do ambiente registrada

### Quando Docker não é suficiente

Docker resolve o isolamento e a portabilidade, mas não orquestra múltiplos containers em escala. Para isso existem ferramentas como Kubernetes, Apache Airflow, e plataformas MLOps (MLflow, Kubeflow). Esses serão mencionados na Aula 10.

---

## Estrutura mínima de um projeto de ML conteinerizado

```
projeto-ml/
├── src/
│   ├── train.py          # pipeline de treino
│   └── inference.py      # lógica de predição
├── data/                 # dados brutos ou banco de dados
├── models/               # artefatos gerados (modelo, referência, etc.)
├── requirements.txt      # dependências fixadas
└── Dockerfile            # (será criado na Aula 02)
```

> **Princípio fundamental:** separe código, dados e artefatos. Cada um tem seu ciclo de vida próprio.

---

## O Case: Monitoramento de Trocador de Calor

Ao longo do curso usaremos dados reais de um **trocador de calor** (`heat_exchanger.db`):

- **Período:** 2022-01-01 a 2022-06-30 (175 registros diários)
- **Tarefa:** modelar a degradação da eficiência térmica ao longo do tempo
- **Modelo:** Regressão Linear Temporal
- **Duas capacidades de inferência:**
  1. Dado uma **data** → prever a eficiência térmica esperada
  2. Dado um **valor de eficiência** → encontrar as datas históricas mais próximas

### Dados disponíveis

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `timestamp` | TEXT | Data da medição (YYYY-MM-DD) |
| `water_inlet_temperature` | REAL | Temperatura de entrada da água (°C) |
| `glycol_inlet_temperature` | REAL | Temperatura de entrada do glicol (°C) |
| `out_glycol_temperature` | REAL | Temperatura de saída do glicol (°C) |
| `out_water_temperature` | REAL | Temperatura de saída da água (°C) |
| `heat_efficiency` | REAL | Eficiência térmica (%) — **alvo** |

### Por que Regressão Linear?

A eficiência cai de forma monotônica ao longo do tempo (~-0.018% por dia), seguindo uma tendência linear clara. Modelos baseados em árvores (como GradientBoosting) não extrapolam bem fora do range de treino — a regressão linear é a escolha correta para capturar e projetar essa degradação.

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo1
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
# .venv\Scripts\activate        # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Explore os notebooks

Os notebooks complementam os scripts com análises interativas. Execute dentro da pasta `modulo1/` com o ambiente virtual ativado:

```bash
pip install jupyter
jupyter notebook notebooks/
```

| Notebook | Conteúdo |
|----------|----------|
| `eda.ipynb` | Análise exploratória completa: qualidade dos dados, evolução temporal, distribuições, correlações e quantificação da tendência de degradação |
| `model_evaluation.ipynb` | Comparação de algoritmos (LinearRegression, Ridge, Polinomial grau 2, RandomForest): métricas, curvas de predição, capacidade de extrapolação e análise de resíduos |

> Os notebooks leem o banco diretamente de `../data/heat_exchanger.db`. Execute-os a partir da pasta `notebooks/` ou ajuste o `DB_PATH` conforme necessário.

---

### 5. Execute o treino

```bash
python src/train.py
```

Saída esperada:
```
Carregando dados de: data/heat_exchanger.db
Registros: 175 | Período: 2022-01-01 → 2022-06-30
Eficiência: min=93.23%  max=96.45%

Treinando modelo de regressão linear temporal...

=== Métricas de Avaliação ===
  MAE       : 0.0397%
  RMSE      : 0.0469%
  R²        : 0.9975
  R² CV (5) : 0.7580 ± 0.2362
  Tendência : -0.0179% por dia

Modelo salvo em     : models/model.pkl
Referência salva em : models/reference_data.pkl
```

### 6. Execute a inferência

```bash
# Modo 1 — prever eficiência para uma data
python src/inference.py --date 2022-04-15

# Modo 2 — encontrar as datas para uma eficiência alvo
python src/inference.py --efficiency 94.5

# Modo 2 com mais resultados
python src/inference.py --efficiency 94.5 --top 5
```

---

## Problemas que você vai encontrar (sem Docker)

Tente rodar o projeto em outra máquina ou num ambiente limpo. Você provavelmente vai ver:

```
# Versão diferente do Python
ModuleNotFoundError: No module named 'sklearn'

# Versão incompatível de pacotes
AttributeError: module 'sklearn.metrics' has no attribute 'root_mean_squared_error'

# Banco de dados não encontrado
FileNotFoundError: data/heat_exchanger.db

# Sistema operacional diferente
OSError: [Errno 2] No such file or directory
```

Esses erros são o ponto de partida para a **Aula 02**, onde containerizamos o projeto e eliminamos esses problemas de vez.

---

## Estrutura dos arquivos deste módulo

```
modulo1/
├── README.md             # este arquivo
├── requirements.txt      # dependências fixadas com versão
├── src/
│   ├── train.py          # pipeline de treino: carrega DB → treina → salva artefatos
│   └── inference.py      # dois modos: --date (eficiência) e --efficiency (data)
├── notebooks/
│   ├── eda.ipynb          # análise exploratória: qualidade, correlações e tendência de degradação
│   └── model_evaluation.ipynb  # comparação de modelos e justificativa da escolha final
├── models/               # artefatos gerados: model.pkl e reference_data.pkl
└── data/
    └── heat_exchanger.db # banco SQLite com os dados do trocador de calor
```

---

## Checklist de Entrega

- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas via `requirements.txt`
- [ ] `train.py` executa sem erros e salva artefatos em `models/`
- [ ] `inference.py --date` retorna a eficiência prevista para uma data
- [ ] `inference.py --efficiency` retorna as datas para uma eficiência alvo
- [ ] `eda.ipynb` executa sem erros e exibe as análises exploratórias
- [ ] `model_evaluation.ipynb` executa sem erros e exibe a comparação de modelos
- [ ] Entendeu a estrutura de pastas e a separação de responsabilidades

---