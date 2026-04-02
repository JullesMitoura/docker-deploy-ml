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

## Módulo 02: Containerizando o Projeto
> **Entrega**: projeto rodando em container

---

Com o projeto funcionando localmente, o próximo passo é empacotá-lo em um container Docker. Este módulo apresenta os fundamentos da containerização aplicados diretamente ao projeto de ML: como escrever um `Dockerfile`, escolher a imagem base certa e garantir que o ambiente seja reproduzível em qualquer máquina.

O conceito-chave aqui é que uma imagem Docker é uma **fotografia do ambiente de execução**  sistema operacional, interpretador Python, bibliotecas e código fonte. Quem rodar essa imagem terá exatamente o mesmo ambiente, independentemente do sistema operacional do host.

### O que você vai aprender

- Como escrever um `Dockerfile` para um projeto Python de ML
- Escolha de imagem base: `python:3.11-slim` vs alternativas
- Uso de variáveis de ambiente para configuração do container
- Como o cache de layers do Docker acelera o build e deve guiar a ordem das instruções

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| `Dockerfile` | Receita de construção da imagem |
| Imagem base | Ponto de partida do ambiente (ex: `python:3.11-slim`) |
| Layer cache | Reaproveitamento de etapas já construídas em builds subsequentes |
| Variáveis de ambiente | Configuração externalizada via `ENV` / `-e` |

### Por que isso importa para ML

Sem Docker, o clássico "funciona na minha máquina" é um risco real em projetos de ML  versões de bibliotecas como `scikit-learn` ou `numpy` podem produzir resultados diferentes entre ambientes. Containerizar o projeto elimina essa variável e é o primeiro passo para um pipeline de ML confiável.
