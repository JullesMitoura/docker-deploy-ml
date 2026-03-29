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
![Docker Hub](https://img.shields.io/badge/Docker_Hub-2496ED?style=flat-square&logo=docker&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Modulo 07: Publicação da imagem
> Entrega: imagem publicada e reutilizável

---

## O problema do módulo anterior

No módulo 06, o CI builda e testa as imagens  mas elas existem apenas na VM efêmera do GitHub Actions. Quando o job termina, as imagens somem.

Para que outro time puxe a imagem, ou para que a inferência rode em qualquer servidor, a imagem precisa estar **publicada em um registry**.

---

## A solução: Docker Hub + CD automático

```
Developer                GitHub Actions               Docker Hub
──────────               ──────────────────           ──────────────────────
git push main   ──►     build-train    ──────────►  username/heat-exchanger-train:latest
                         build-inference ──────────►  username/heat-exchanger-inference:latest
                         test ✓                        username/heat-exchanger-train:main-abc1234
```

O Docker Hub é o registry público mais comum. Qualquer máquina com Docker pode fazer `docker pull` sem precisar do repositório Git.

---

## Configuração: Docker Hub + Secrets

### 1. Crie uma conta no Docker Hub

Acesse [hub.docker.com](https://hub.docker.com) e crie uma conta gratuita.

### 2. Gere um Access Token

1. Docker Hub → canto superior direito → **Account Settings**
2. **Security** → **New Access Token**
3. Nome: `github-actions-heat-exchanger`
4. Permissões: **Read, Write, Delete**
5. Copie o token gerado  ele não será exibido novamente

### 3. Configure os Secrets no GitHub

No repositório GitHub:
**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Valor |
|--------|-------|
| `DOCKERHUB_USERNAME` | Seu usuário do Docker Hub |
| `DOCKERHUB_TOKEN` | O Access Token gerado no passo anterior |

---

## Estratégia de tags

O workflow usa `docker/metadata-action` para gerar tags automaticamente:

| Evento | Tags geradas |
|--------|-------------|
| Push em `main` | `:latest` `:main` `:{sha}` |
| Pull Request #42 | `:pr-42` `:sha-{hash}` (sem push) |
| Git tag `v1.2.3` | `:v1.2.3` `:1.2` `:1` `:latest` `:{sha}` |
| Push em `feature/xyz` | `:feature-xyz` `:{sha}` (sem push) |

### Por que `:latest` não é suficiente em produção?

`:latest` é mutável  ele aponta para a versão mais recente. Em produção, é preciso saber **exatamente** qual versão está rodando:

```bash
# Ruim em produção  pode mudar sem você saber
docker pull username/heat-exchanger-train:latest

# Bom em produção  imutável, rastreável
docker pull username/heat-exchanger-train:v1.2.3
docker pull username/heat-exchanger-train:abc1234
```

---

## Estratégia de branches

```
feature/* ──► build + test              (sem push ao Docker Hub)
    │
    └──► PR ──► build + test           (sem push ao Docker Hub)
                    │
                    └──► merge em main ──► build + test + push :latest + :main-{sha}

tag v*.*.* ──────────────────────────► build + test + push :v1.2.3 + :1.2 + :1 + :latest
```

**Por que não publicar em feature branches?**
- Evita poluir o registry com imagens de desenvolvimento
- Garante que apenas código revisado e aprovado vai para o Docker Hub
- Pull requests de forks não têm acesso a secrets  não podem autenticar

---

## Estrutura do workflow

O arquivo `.github/workflows/modulo7-cd.yml` estende o módulo 06 com:

```yaml
# Login no Docker Hub (apenas fora de PRs)
- uses: docker/login-action@v3
  if: github.event_name != 'pull_request'
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

# Geração automática de tags
- uses: docker/metadata-action@v5
  with:
    images: username/heat-exchanger-train
    tags: |
      type=ref,event=branch
      type=semver,pattern={{version}}
      type=sha,prefix=
      type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

# Build + push condicional
- uses: docker/build-push-action@v5
  with:
    push: ${{ github.event_name != 'pull_request' }}
    tags: ${{ steps.meta.outputs.tags }}
```

A diferença central: `push: true` apenas quando não é PR. O `outputs: type=docker,dest=/tmp/train.tar` garante que a imagem fica disponível para os testes mesmo em PRs (onde não há push).

---

## Estrutura dos arquivos deste módulo

```
.github/
└── workflows/
    ├── modulo6-ci.yml      # módulo anterior (apenas CI)
    └── modulo7-cd.yml      # CI/CD com push ao Docker Hub

modulo7/
├── Dockerfile.train        # mesmo do módulo 05/06
├── Dockerfile.inference    # mesmo do módulo 05/06
├── .dockerignore
├── requirements-train.txt
├── requirements-inference.txt
├── src/                    # mesmo do módulo 05/06 (com versionamento)
├── data/
│   └── heat_exchanger.db
└── models/
    └── .gitkeep
```

---

## Passo a Passo

### 1. Configure os secrets (pré-requisito)

Siga os passos da seção **Configuração: Docker Hub + Secrets** acima.

### 2. Faça push para main

```bash
git add modulo7/ .github/workflows/modulo7-cd.yml
git commit -m "feat: modulo 7  publicação no Docker Hub"
git push origin main
```

### 3. Acompanhe o pipeline

**Actions → Modulo 7  CI/CD + Docker Hub**

```
✓ build-train     (2m 45s)  → pushed username/heat-exchanger-train:latest
✓ build-inference (2m 10s)  → pushed username/heat-exchanger-inference:latest
✓ test            (1m 20s)
```

### 4. Verifique no Docker Hub

```
hub.docker.com/r/username/heat-exchanger-train/tags
hub.docker.com/r/username/heat-exchanger-inference/tags
```

Você verá: `latest`, `main`, `{sha}`

### 5. Puxe a imagem publicada

Em qualquer máquina com Docker:

```bash
docker pull username/heat-exchanger-train:latest
docker run -v $(pwd)/models:/app/models username/heat-exchanger-train:latest
```

### 6. Crie uma git tag para versão semver

```bash
git tag v1.0.0
git push origin v1.0.0
```

O workflow dispara novamente e publica `:v1.0.0`, `:1.0`, `:1`, `:latest`.

### 7. Teste o fluxo de PR

Crie um branch, abra um PR. O pipeline builda e testa  mas **não** faz push. Somente após o merge em main a imagem é publicada.

---

## Comparação: módulo 06 vs módulo 07

| | Módulo 06 (CI) | Módulo 07 (CI/CD) |
|---|---|---|
| Build automático | Sim | Sim |
| Testes automáticos | Sim | Sim |
| Publicação no registry | Não | Sim (main e tags) |
| PRs publicam imagem? | Não se aplica | Não (segurança) |
| Tags automáticas | Não | Sim (metadata-action) |
| Imagem reutilizável | Não | Sim (Docker Hub público) |

---

## Checklist de Entrega

- [ ] Secrets `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN` configurados no GitHub
- [ ] Push em `main` disparou o workflow e publicou as imagens no Docker Hub
- [ ] Tags `:latest`, `:main` e `:{sha}` visíveis em `hub.docker.com/r/...`
- [ ] `docker pull username/heat-exchanger-train:latest` funciona em outra máquina
- [ ] PR não publicou imagens (apenas buildou e testou)
- [ ] Git tag `v1.0.0` gerou tags semver no Docker Hub
- [ ] Entendeu por que `:latest` não é suficiente em produção

---
