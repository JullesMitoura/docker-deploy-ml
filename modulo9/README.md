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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/fastapi/fastapi-original.svg"
     alt="FastAPI"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Modulo 09: Ambiente de produção
> Entrega: pipeline completo local

---

## O problema do módulo anterior

No módulo 08, treino e serving são orquestrados manualmente — dois `docker run` separados que você precisa lembrar de executar na ordem certa. Em produção, isso é frágil:

```bash
# Módulo 08 — orquestração manual, propensa a erros
docker run -v $(pwd)/models:/app/models heat-exchanger-train   # esquecer isso...
docker run -v $(pwd)/models:/app/models -p 8000:8000 heat-exchanger-serve  # ...quebra isso
```

---

## A solução: Docker Compose + arquivos de ambiente

```
docker compose up
       │
       ├──► train (roda e encerra) ──► model.pkl no volume
       │
       └──► serve (sobe após train) ──► API em http://localhost:8000
```

`docker-compose.yml` define os serviços, volumes e dependências. O `depends_on: condition: service_completed_successfully` garante a ordem correta automaticamente.

---

## Dev vs Prod no Docker

| Configuração | Dev | Prod |
|---|---|---|
| `LOG_LEVEL` | `DEBUG` | `WARNING` |
| Hot reload | Sim (`--reload`) | Não |
| Código fonte | Volume montado | Baked na imagem |
| `restart` | `no` | `unless-stopped` |
| Healthcheck | Implícito | Explícito no Dockerfile |
| Variáveis | `.env` com DEBUG | `.env` com valores restritos |

### Como o Docker Compose gerencia isso

```
docker compose up          → carrega docker-compose.yml + docker-compose.override.yml (dev)
docker compose -f docker-compose.yml up  → só o yml base (prod)
```

`docker-compose.override.yml` é carregado **automaticamente** em `docker compose up`. Para produção, você o ignora explicitamente.

---

## Novidades deste módulo

### `docker-compose.yml`
- Serviço `train`: roda uma vez e encerra (`restart: "no"`)
- Serviço `serve`: execução contínua (`restart: unless-stopped`)
- `depends_on: condition: service_completed_successfully` — barrier entre treino e serving
- Volume nomeado `modulo9_models` — persiste entre `docker compose down/up`

### `docker-compose.override.yml`
- Sobrescreve o CMD para `--reload` (hot reload em dev)
- Monta `./src` como volume para edição sem rebuild
- Define `LOG_LEVEL=DEBUG`

### `Dockerfile.serve` — HEALTHCHECK
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=15s \
  CMD python -c \
    "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \
  || exit 1
```

O Docker verifica a saúde do container periodicamente. `docker ps` mostrará `(healthy)` ou `(unhealthy)`. Orquestradores (Kubernetes, ECS) usam esse status para roteamento de tráfego.

### `.env.example` + `.env`
Variáveis de ambiente em arquivo — não mais hardcoded no comando `docker run`.

---

## Estrutura dos arquivos deste módulo

```
modulo9/
├── docker-compose.yml          # serviços train + serve (modo produção)
├── docker-compose.override.yml # overrides dev (hot reload, DEBUG)
├── .env.example                # template — commitar
├── .env                        # valores reais — NÃO commitar (.gitignore)
├── Dockerfile.train
├── Dockerfile.serve            # com HEALTHCHECK
├── .dockerignore
├── requirements-train.txt
├── requirements-serve.txt
├── src/
│   ├── train.py
│   ├── app.py
│   └── utils/
│       ├── logger.py
│       └── versioning.py
├── data/
│   └── heat_exchanger.db
└── models/
    └── .gitkeep
```

---

## Passo a Passo

### 1. Navegue até o módulo

```bash
cd modulo9
```

### 2. Crie o arquivo de variáveis de ambiente

```bash
cp .env.example .env
```

Edite `.env` conforme necessário (os padrões já funcionam para desenvolvimento local).

### 3. Pipeline completo (modo dev — com override automático)

```bash
docker compose up --build
```

O que acontece:
1. Docker builda as imagens `train` e `serve`
2. Inicia o container `train` → treino executa → `model.pkl` gerado no volume
3. Train encerra com código 0
4. Docker inicia o container `serve` (após train completar)
5. API fica disponível em `http://localhost:8000`

Saída esperada:
```
modulo9-train-1  | INFO     | Treino concluído — versão: 20240101_143052
modulo9-train-1 exited with code 0
modulo9-serve-1  | INFO     | Modelo carregado — versão: 20240101_143052
modulo9-serve-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 4. Verifique o status dos containers

```bash
docker compose ps
```

```
NAME              STATUS
modulo9-train-1   Exited (0)     ← treino encerrou com sucesso
modulo9-serve-1   Up (healthy)   ← API rodando e saudável
```

### 5. Teste a API

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict/date \
  -H "Content-Type: application/json" \
  -d '{"date": "2022-04-15"}'
```

### 6. Mode produção (sem override de dev)

```bash
docker compose -f docker-compose.yml up --build
```

Diferenças visíveis:
- Sem `--reload` (uvicorn não monitora arquivos)
- `LOG_LEVEL=INFO` (sem mensagens DEBUG)
- Código fonte imutável (não monta `./src`)

### 7. Hot reload em dev

Com o override ativo, edite qualquer arquivo em `src/`:

```bash
# Em outro terminal:
echo "# comentario de teste" >> src/app.py
```

O uvicorn detecta a mudança e reinicia automaticamente — sem rebuild.

### 8. Encerre o pipeline

```bash
docker compose down
```

Para remover também o volume (e os modelos):
```bash
docker compose down -v
```

---

## Variáveis de ambiente: boas práticas

| Prática | Por quê |
|---|---|
| `.env` no `.gitignore` | Credenciais e configs locais não pertencem ao git |
| `.env.example` commitado | Template documenta quais variáveis são necessárias |
| Valores padrão no `docker-compose.yml` (`${VAR:-default}`) | Container funciona sem `.env` em CI |
| `LOG_LEVEL=WARNING` em prod | Menos ruído, logs mais acionáveis |
| Nunca hardcodar secrets no Dockerfile | Segredos em variáveis, não em camadas de imagem |

---

## Diferença: volume nomeado vs bind mount

| | Volume nomeado (Compose) | Bind mount (`-v ./models:/app/models`) |
|---|---|---|
| Gerenciado por | Docker | Sistema de arquivos do host |
| Portabilidade | Alta | Depende do caminho local |
| Inspeção | `docker volume inspect` | `ls ./models` |
| Uso típico | Produção | Desenvolvimento, depuração |

---

## Checklist de Entrega

- [ ] `cp .env.example .env` e `docker compose up --build` completa sem erros
- [ ] `docker compose ps` mostra `train` como `Exited (0)` e `serve` como `Up (healthy)`
- [ ] API responde em `http://localhost:8000/health`
- [ ] Hot reload funciona: editar `src/app.py` reinicia o servidor automaticamente
- [ ] Modo produção (`docker compose -f docker-compose.yml up`) funciona sem override
- [ ] Entendeu a diferença entre `docker-compose.yml` e `docker-compose.override.yml`
- [ ] Entendeu como o `HEALTHCHECK` funciona e onde aparece no `docker ps`
- [ ] `docker compose down -v` remove o pipeline e o volume

---
