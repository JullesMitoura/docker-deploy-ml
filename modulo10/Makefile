TRAIN_IMAGE := heat-exchanger-train
SERVE_IMAGE := heat-exchanger-serve
MODELS_DIR  := $(CURDIR)/models
PORT        := 8000

.PHONY: help build-train build-serve build train serve up stop logs \
        health predict-date predict-efficiency versions clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

build-train: ## Builda a imagem de treino
	docker build -f Dockerfile.train -t $(TRAIN_IMAGE) .

build-serve: ## Builda a imagem de serving
	docker build -f Dockerfile.serve -t $(SERVE_IMAGE) .

build: build-train build-serve ## Builda ambas as imagens

train: ## Executa o treino e gera artefatos
	@mkdir -p $(MODELS_DIR)
	docker run --rm -v $(MODELS_DIR):/app/models $(TRAIN_IMAGE)

serve: ## Sobe a API de serving em background
	docker run -d \
	  --name heat-serve \
	  -v $(MODELS_DIR):/app/models \
	  -p $(PORT):8000 \
	  --restart unless-stopped \
	  $(SERVE_IMAGE)

up: build train serve ## Pipeline completo: build + train + serve

stop: ## Para e remove o container de serving
	@docker stop heat-serve 2>/dev/null || true
	@docker rm   heat-serve 2>/dev/null || true

logs: ## Exibe logs da API em tempo real
	docker logs -f heat-serve

health: ## Verifica o health da API
	@curl -s http://localhost:$(PORT)/health | python3 -m json.tool

predict-date: ## Predicao de eficiencia (DATE=YYYY-MM-DD)
	@curl -s -X POST http://localhost:$(PORT)/predict/date \
	  -H "Content-Type: application/json" \
	  -d '{"date": "$(DATE)"}' | python3 -m json.tool

predict-efficiency: ## Predicao de data (EFFICIENCY=94.5)
	@curl -s -X POST http://localhost:$(PORT)/predict/efficiency \
	  -H "Content-Type: application/json" \
	  -d '{"efficiency": $(EFFICIENCY)}' | python3 -m json.tool

versions: ## Lista versoes de modelo disponiveis
	@curl -s http://localhost:$(PORT)/versions | python3 -m json.tool

clean: stop ## Remove imagens e artefatos locais
	@docker rmi $(TRAIN_IMAGE) $(SERVE_IMAGE) 2>/dev/null || true
	@rm -f $(MODELS_DIR)/*.pkl $(MODELS_DIR)/registry.json