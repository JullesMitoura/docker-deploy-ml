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
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 09: Ambiente de Produção com Docker Compose
> **Entrega**: pipeline completo rodando localmente com orquestração

---

Com treino, inferência e serving como containers separados, coordená-los manualmente via `docker run` começa a se tornar impraticável. Este módulo introduz o **Docker Compose**  a ferramenta para declarar e orquestrar múltiplos containers como um ambiente coeso.

Além da orquestração, o módulo aborda a diferença entre ambiente de desenvolvimento e produção: como usar `docker-compose.override.yml` para sobrescrever configurações localmente sem alterar o arquivo de produção, e como garantir que o container de serving só suba após o modelo estar disponível.

### O que você vai aprender

- Como declarar múltiplos serviços em um único `docker-compose.yml`
- Usar `depends_on` para controlar a ordem de inicialização dos containers
- Adicionar `HEALTHCHECK` para monitorar a saúde da API de serving
- Diferenciar configuração de desenvolvimento e produção com `override`
- Gerenciar variáveis de ambiente com arquivo `.env`

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| `docker-compose.yml` | Arquivo declarativo que define os serviços, volumes e redes do ambiente |
| `depends_on` | Garante que um serviço só inicia após outro estar pronto |
| `HEALTHCHECK` | Instrução Docker que monitora se o container está funcionando corretamente |
| `docker-compose.override.yml` | Arquivo de sobrescrita para configurações locais de desenvolvimento |
| `.env` | Arquivo com variáveis de ambiente carregadas automaticamente pelo Compose |

### Dev vs Prod

Um dos aprendizados centrais deste módulo é que desenvolvimento e produção têm necessidades diferentes: em dev, queremos logs verbosos, hot-reload e volumes montados para edição ao vivo; em prod, queremos imagens fixas, recursos limitados e nenhum dado sensível no código. O padrão `compose.yml` + `compose.override.yml` é a forma idiomática de gerenciar essa diferença.
