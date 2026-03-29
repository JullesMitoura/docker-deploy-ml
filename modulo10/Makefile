# =============================================================================
# Makefile — Heat Exchanger ML Pipeline
#
# Consolida todos os comandos do curso em atalhos simples.
# Uso: make <target>
# =============================================================================

TRAIN_IMAGE := heat-exchanger-train
SERVE_IMAGE := heat-exchanger-serve
MODELS_DIR  := $(CURDIR)/models
PORT        := 8000

.PHONY: help build-train build-serve build train serve up stop logs \
        health predict-date predict-efficiency versions clean

# --- Ajuda ------------------------------------------------------------------
help:
	@echo ""
	@echo "Heat Exchanger ML Pipeline"
	@echo "=========================="
	@echo ""
	@echo "Construção:"
	@echo "  make build-train        Builda a imagem de treino"
	@echo "  make build-serve        Builda a imagem de serving"
	@echo "  make build              Builda ambas as imagens"
	@echo ""
	@echo "Execução:"
	@echo "  make train              Executa o treino e gera artefatos"
	@echo "  make serve              Sobe a API de serving (background)"
	@echo "  make up                 build + train + serve (pipeline completo)"
	@echo ""
	@echo "Operações:"
	@echo "  make stop               Para e remove o container de serving"
	@echo "  make logs               Exibe logs da API em tempo real"
	@echo "  make health             Verifica o health da API"
	@echo "  make predict-date       Predição de eficiência (DATE=YYYY-MM-DD)"
	@echo "  make predict-efficiency Predição de data (EFFICIENCY=94.5)"
	@echo "  make versions           Lista versões de modelo disponíveis"
	@echo ""
	@echo "Manutenção:"
	@echo "  make clean              Remove imagens e artefatos locais"
	@echo ""

# --- Construção -------------------------------------------------------------
build-train:
	docker build -f Dockerfile.train -t $(TRAIN_IMAGE) .

build-serve:
	docker build -f Dockerfile.serve -t $(SERVE_IMAGE) .

build: build-train build-serve

# --- Execução ---------------------------------------------------------------
train:
	@mkdir -p $(MODELS_DIR)
	docker run --rm -v $(MODELS_DIR):/app/models $(TRAIN_IMAGE)

serve:
	docker run -d \
	  --name heat-serve \
	  -v $(MODELS_DIR):/app/models \
	  -p $(PORT):8000 \
	  --restart unless-stopped \
	  $(SERVE_IMAGE)
	@echo ""
	@echo "API disponível em http://localhost:$(PORT)"
	@echo "Documentação:     http://localhost:$(PORT)/docs"
	@echo ""

up: build train serve

# --- Operações -------------------------------------------------------------
stop:
	@docker stop heat-serve 2>/dev/null || true
	@docker rm   heat-serve 2>/dev/null || true
	@echo "Container de serving removido."

logs:
	docker logs -f heat-serve

health:
	@curl -s http://localhost:$(PORT)/health | python3 -m json.tool

# Uso: make predict-date DATE=2022-04-15
predict-date:
	@curl -s -X POST http://localhost:$(PORT)/predict/date \
	  -H "Content-Type: application/json" \
	  -d '{"date": "$(DATE)"}' | python3 -m json.tool

# Uso: make predict-efficiency EFFICIENCY=94.5
predict-efficiency:
	@curl -s -X POST http://localhost:$(PORT)/predict/efficiency \
	  -H "Content-Type: application/json" \
	  -d '{"efficiency": $(EFFICIENCY)}' | python3 -m json.tool

versions:
	@curl -s http://localhost:$(PORT)/versions | python3 -m json.tool

# --- Manutenção -------------------------------------------------------------
clean: stop
	@docker rmi $(TRAIN_IMAGE) $(SERVE_IMAGE) 2>/dev/null || true
	@rm -f $(MODELS_DIR)/*.pkl $(MODELS_DIR)/registry.json
	@echo "Imagens e artefatos removidos."
