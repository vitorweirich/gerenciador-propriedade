# Gerenciador de Propriedade
Este projeto consiste em uma API que calcula datas relacionadas a gerenciar uma propriedade leiteira e uma aplicação simples em python que simplesmente consome a API e cria uma interface gráfica.

Tratando-se de um experimênto muitas coisas ainda estão fora do pdarão e não respeitam as boas práticas, por exemplo, todos os endpoints usam o método get, incluindo os de cadastro e exclusão.

## Endpoints
Existem endpoints para todas as operações básicas de CRUD e um para de fato calcular as datas:
> Buscar todas as vacas: http://localhost8080/vacas esse endpoint ainda pode receber um parâmetro opcional indicando qual cor você deseja busar(para objetivos de entendimento da API o que as cores significam são irrelevantes por esse motivo caso seja passado uma cor inesistente o sistema irá simplesmente ignora-lo e retornar todas as vacas), por exemplo para buscar todas as vacas de amarela basta passar nessa url um parâmetro cor=amarela: http://localhost8080/vacas?cor=amarela

> Calcular: http://localhost8080/vacas/calcular/{numero}/{data}

> Cadastrar: http://localhost8080/vacas/cadastrar/{numero}/{nome}

> Alterar: http://localhost8080/vacas/alterar/{numero}/{nome}

> deletar: http://localhost8080/vacas/deletar/{numero}

### Autor: Vitor Mateus Weirich
