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

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 04: Otimizando Imagens Docker
> **Entrega**: imagens menores e mais rápidas

---

Ter um container funcional é o ponto de partida. Ter um container **eficiente** é o que diferencia um ambiente de desenvolvimento de um ambiente de produção. Este módulo foca em duas frentes: reduzir o tamanho das imagens e acelerar o processo de build  dois fatores com impacto direto em custo, velocidade de deploy e segurança.

Imagens grandes demoram mais para fazer push/pull, consomem mais espaço em registro e em disco, e carregam mais superfície de ataque potencial. O multi-stage build e o `.dockerignore` são as principais ferramentas para atacar esse problema.

### O que você vai aprender

- Como usar **multi-stage build** para separar ambiente de build do ambiente de execução
- O papel do `.dockerignore` em excluir arquivos desnecessários da imagem
- Estratégias de ordenação de instruções para maximizar o reaproveitamento do cache
- Como medir e comparar o tamanho de imagens antes e depois das otimizações

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| Multi-stage build | Usar múltiplos estágios no `Dockerfile`; apenas o necessário vai para a imagem final |
| `.dockerignore` | Lista de arquivos/diretórios excluídos do contexto de build |
| Cache de layers | Reaproveitamento de etapas que não mudaram desde o último build |
| Imagem enxuta | Imagem com apenas o necessário para executar  sem ferramentas de build, docs ou testes |

### Por que tamanho de imagem importa em ML

Projetos de ML tendem a acumular dependências pesadas (numpy, pandas, scikit-learn, torch). Uma imagem de treino pode facilmente ultrapassar 1 GB. Com multi-stage build, é possível usar uma imagem completa para instalar e compilar dependências e copiar apenas os binários necessários para uma imagem final `slim`  reduzindo significativamente o tamanho sem abrir mão de nada em execução.
