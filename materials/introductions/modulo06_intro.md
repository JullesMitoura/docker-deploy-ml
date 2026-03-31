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

## Módulo 06: CI com GitHub Actions
> **Entrega**: pipeline de integração contínua funcionando

---

Até aqui, todo o processo de build e teste era manual. Este módulo automatiza isso com **Integração Contínua (CI)**: a cada push ou pull request, o GitHub Actions executa automaticamente o build das imagens e os testes de integração  sem intervenção humana.

CI é a prática de integrar e validar mudanças de código de forma frequente e automatizada. Em projetos de ML, isso significa garantir que o código de treino e inferência continua funcionando após cada alteração, e que as imagens Docker continuam sendo construídas corretamente.

### O que você vai aprender

- Como escrever um workflow YAML para GitHub Actions
- Estruturar jobs paralelos para otimizar o tempo de execução do CI
- Passar artefatos entre jobs (ex: modelo treinado em um job, testado em outro)
- Usar cache do GitHub Actions para acelerar instalação de dependências

### Conceitos centrais

| Conceito | O que é |
|----------|---------|
| Workflow YAML | Arquivo de configuração do pipeline em `.github/workflows/` |
| Job | Unidade de execução dentro do workflow (roda em uma VM isolada) |
| Jobs paralelos | Múltiplos jobs rodando ao mesmo tempo para reduzir o tempo total |
| Artefatos entre jobs | Mecanismo para passar arquivos (ex: `model.pkl`) de um job para outro |
| Cache GHA | Reaproveitamento de dependências instaladas em execuções anteriores |

### A mudança de mentalidade

Com CI, a pergunta deixa de ser "funcionou na minha máquina?" e passa a ser "passou no pipeline?". O pipeline é a fonte da verdade. Qualquer mudança que quebre o build ou os testes é detectada automaticamente, antes de chegar à branch principal.
