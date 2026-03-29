# =============================================================================
# OBJETIVO 1: Criação do primeiro Dockerfile
# Um Dockerfile é uma receita de instruções que o Docker lê de cima para baixo
# para construir uma imagem. Cada instrução gera uma camada (layer) cacheada.
# =============================================================================


# =============================================================================
# OBJETIVO 2: Escolha da imagem base
#
# Todo Dockerfile começa com FROM — define o ponto de partida da imagem.
# "python:3.11-slim" é a imagem oficial do Python em cima de um Debian mínimo:
#   - python:3.11        → ~1 GB  (ferramentas de compilação, headers, etc.)
#   - python:3.11-slim   → ~50 MB (apenas o necessário para rodar Python)
#
# Para produção e ML, slim é a escolha certa: imagem menor = deploy mais rápido.
# =============================================================================
FROM python:3.11-slim


# =============================================================================
# WORKDIR — Diretório de trabalho dentro do container
#
# Define a pasta raiz de todos os comandos seguintes (COPY, RUN, CMD).
# Equivale a um "cd /app" permanente. Se a pasta não existir, o Docker a cria.
# =============================================================================
WORKDIR /app


# =============================================================================
# OBJETIVO 3: Instalação de dependências
#
# Copiamos o requirements.txt ANTES do código-fonte — isso é estratégia de cache:
#
#   Se requirements.txt não mudou → Docker reutiliza a camada do pip install
#   Se só o código mudou          → pip install NÃO é re-executado
#
# --no-cache-dir: impede o pip de salvar cache de download dentro da imagem,
# mantendo-a menor.
# =============================================================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# =============================================================================
# Cópia do código-fonte e dos dados
#
# Copiamos DEPOIS do pip install para aproveitar o cache acima.
# O .dockerignore garante que .venv/, models/ e __pycache__/ não entrem aqui.
# =============================================================================
COPY src/  src/
COPY data/ data/


# =============================================================================
# OBJETIVO 5: Uso de variáveis de ambiente
#
# ENV define variáveis de ambiente com valores padrão dentro do container.
# Vantagem: o comportamento pode ser alterado em runtime SEM reconstruir a imagem:
#
#   docker run -e LOG_LEVEL=DEBUG heat-exchanger   ← muda só o log, sem rebuild
#   docker run -e DB_PATH=data/outro.db ...        ← aponta para outro banco
#
# DB_PATH   → caminho do banco SQLite lido por train.py
# MODEL_DIR → pasta onde o model.pkl será salvo após o treino
# LOG_LEVEL → nível de log (INFO por padrão, DEBUG para mais detalhes)
# PYTHONUNBUFFERED → força o Python a escrever logs imediatamente no terminal,
#                    sem buffer — essencial para acompanhar o treino em tempo real
# =============================================================================
ENV DB_PATH=data/heat_exchanger.db \
    MODEL_DIR=models \
    LOG_LEVEL=INFO \
    PYTHONUNBUFFERED=1


# =============================================================================
# OBJETIVO 4: Execução do treino dentro do container
#
# CMD define o comando padrão executado quando o container sobe.
# Diferença importante:
#   RUN  → executa durante o BUILD (para montar a imagem)
#   CMD  → executa durante o RUN   (quando o container é iniciado)
#
# "docker run heat-exchanger" executa o treino.
#
# Para inferência, sobrescreva o CMD em runtime (sem precisar de novo build):
#   docker run heat-exchanger sh -c "python src/train.py && python src/inference.py --date 2022-04-15"
#   docker run heat-exchanger sh -c "python src/train.py && python src/inference.py --efficiency 80.0"
#
# Nota: treino e inferência rodam no mesmo container para que o model.pkl
# gerado pelo treino esteja disponível para a inferência (containers são efêmeros).
# =============================================================================
CMD ["python", "src/train.py"]
