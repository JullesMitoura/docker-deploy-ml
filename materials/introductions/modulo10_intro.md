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
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/githubactions/githubactions-original.svg"
     alt="GitHub Actions"
     width="80"
     height="80"/>

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)

<img width="80%" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"/>

</div>

## Módulo 10: Workflow End-to-End
> **Entrega**: pipeline completo de treino → build → push → serving

---

Este é o módulo de fechamento. Todos os blocos construídos ao longo do curso  estrutura de projeto, containers, separação de responsabilidades, otimização de imagens, versionamento de artefatos, CI/CD e serving via API  são integrados em um **pipeline end-to-end funcional**.

O objetivo não é aprender algo novo, mas consolidar: fazer o pipeline completo rodar de ponta a ponta, de forma automatizada e confiável. Um push na branch principal dispara o CI, que treina o modelo, constrói as imagens, publica no Docker Hub, sobe o ambiente de produção e valida a API com um smoke test.

### O que você vai aprender

- Como usar um `Makefile` para centralizar os comandos do projeto (build, train, serve, test)
- Implementar um smoke test no CI para validar que a API responde corretamente após o deploy
- Compor um pipeline completo no GitHub Actions: treino → build → push → serving
- Revisar o checklist de produção: o que verificar antes de considerar um modelo "em produção"

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| `Makefile` | Arquivo de automação com targets para os comandos mais usados no projeto |
| Smoke test | Teste mínimo que valida se o sistema está de pé e respondendo (não testa lógica, testa disponibilidade) |
| Pipeline end-to-end | Sequência automatizada desde o treino do modelo até a validação do serving em produção |
| Checklist de produção | Lista de verificações antes de considerar um deploy pronto |

### O resultado final

Ao terminar este módulo, o projeto cobre o ciclo completo de um modelo de ML em produção:

```
código → treino → artefato versionado → imagem otimizada → registro → serving via API → validação automatizada
```

Esse é o workflow que times de engenharia de ML usam no dia a dia  e agora você tem a base para replicá-lo em qualquer projeto.
