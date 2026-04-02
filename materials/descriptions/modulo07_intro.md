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

## Módulo 07: Publicando no Docker Hub
> **Entrega**: imagem publicada e reutilizável em registro público

---

Construir uma imagem Docker localmente é útil para desenvolvimento. Mas para que outros times, servidores de produção ou pipelines de CD possam usar a imagem, ela precisa estar em um **registro de imagens** acessível remotamente. Este módulo completa o ciclo CI/CD publicando a imagem no Docker Hub automaticamente via GitHub Actions.

O resultado prático: qualquer máquina com Docker instalado poderá baixar e rodar a imagem com um único `docker pull`  sem precisar ter o código-fonte ou recompilar nada.

### O que você vai aprender

- Como autenticar o GitHub Actions no Docker Hub com segurança (sem expor credenciais)
- Usar `docker/login-action` e `docker/metadata-action` para automatizar o processo
- Estratégia de tags: quando usar `latest`, tags de versão e tags de branch
- A diferença entre CI (integrar e validar) e CD (entregar para um destino)

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| Registro de imagens | Repositório remoto para armazenar e distribuir imagens Docker |
| `docker/login-action` | Action oficial para autenticar no Docker Hub dentro do workflow |
| `docker/metadata-action` | Gera automaticamente tags e labels para a imagem baseado no contexto do git |
| Estratégia de branches e tags | Regras para decidir o que vai para `latest`, `v1.0`, `main`, etc. |
| Secrets do GitHub | Forma segura de armazenar credenciais sem expô-las no código |

### CI vs CD

O módulo anterior implementou CI: build + teste automático. Este módulo adiciona o CD: após passar nos testes, a imagem é entregue automaticamente ao Docker Hub. Juntos, eles formam o pipeline CI/CD  a espinha dorsal de um workflow de entrega moderno.
