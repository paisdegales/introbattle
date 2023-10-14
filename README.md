# Introbattle

This is a showcase of a game built using pygame

This project is originally part of Introcomp, a programming course of the Federal University of Espirito Santo (UFES)

You can found more about Introcomp on:
* instagram: [@introcompufes](https://www.instagram.com/introcompufes/?hl=en)
* web: [introcomp site](https://introcomp.pet.inf.ufes.br/)

---

## How to play

Clone this repo

```bash
git clone https://github.com/paisdegales/introbattle.git
```

Navigate to the project's folder

```bash
cd path/to/introbattle
```

Install all requirements

```bash
pip freeze -r requirements.txt
```

Run the game

```bash
python main.py
```

And voila! now you can play it! hooray!

---

## How the game looks

Include some cool images :)

---

## Folder structure

```bash
App/
├── Font
├── Object
├── Resource
│   ├── Background
│   ├── Character
│   │   ├── Enemy
│   │   └── Hero
│   ├── Fonts
│   │   ├── BricolageGrotesque
│   │   ├── Dosis
│   │   ├── Handjet
│   │   ├── OpenSans
│   │   └── SourceCodePro
│   └── UI
├── Scene
│   ├── Battle
│   │   └── Local
│   └── Menu
│       └── Local
└── Setup
```


---



# PLANO DE AÇÃO AGORA
1. Implementar exceções (talvez na classe Combat ou na propria BattleScene) que informem quando um personagem 'morre' e quando uma Band 'morre' completamente
2. Tentar corrigir o problema do black spot inicial do seletor com os objetos da classe CharacterBand
3. Padronizar a cena, de modo que seus objetos e ela propria utilize variáveis definidas no arquivo 'Globals.py' ou 'Locals.py'
4. Implemetar o botao que permite voltar para a escolha anterior na batalha
5. Trocar o botao que seleciona coisas na cena de batalha (<Enter> -> Z)
6. Fazer com que a velocidade dos herois influenciem na ordem com que as ações são tomadas


# BACKLOG

* reforçar uso de variaveis apenas definidas no arquivo Globals.py
* talvez implementar algo usando a biblioteca 'argparse'
* talvez investigar como está o uso de memoria ram usando a biblioteca 'tracemalloc'
* talvez usar json em vez de constantes soltas nos arquivos de config/setup
* melhorar a documentação do codigo (tentar aprender como sao documentadas funcoes pelo 'pydoc' e replicar)
* talvez usar mais o modulo 'doctest', que é muito util alias
* talvez melhorar as anotacoes que foram usadas usando o modulo 'typing'
* criar arquivo de log usando o modulo 'logging'
* Talvez ir destruindo alguns objetos com `del` para poupar ram
* Criar terceira e ultima cena do jogo: banner com "You win!" em verde ou "You lose!" em vermelho, com um moving character controlavel com pelas setas do teclado


# COISAS FEITAS
* a classe Selector passou por mudanças. O nome do metodo 'select' foi mudado para 'jump' para refletir melhor o que aquele metodo fazia. Agora, o nome 'select' foi apropriado por um novo metodo, que devolve o simbolo que é apontado pelo seletor atualmente. Alem disso, um novo metodo 'draw_upon_movement' é responsavel por repintar o seletor apos chamadas aos metodos 'up', 'down', 'left' e/ou 'right'
* TurnHandler removido; adicionava complexidade desnecessaria
* Combate primitivo implementado


# ANOTAÇÕES
Outra rotina corriqueira no codigo mas que acaba sendo implementada diversas maneiras um pouco diferente entre si
é o desenho/atualização na tela de um componente da classe CompoundObject. Em geral, a rotina envolve:
1. apagar e redesenhar a superficie do componente em questão na superficie do objeto raiz (CompoundObject)
2. retornar as areas que foram modificadas ao apagar e desenhar o componente
    * essas areas são da classe 'Rect' e utilizam coordenadas relativas em relação ponto topleft do objeto raiz
3. coletar as areas modificadas e chamar o metodo 'refresh' do objeto raiz para atualizar (na tela em que esta desenhado) aquelas regioes suas que sofreram modificacao
4. coletar a area modificada pelo metodo 'refresh' do passo anterior e adiciona-la a fila de atualizacoes pendentes na tela pelo metodo 'queue' da classe Tela

```python
    s, r = paladin.vibrate(screen.image)
    screen.queue(r)
    r = hunter.vibrate_component("character")
    screen.queue(r)
    r = portrait.vibrate_component("hero")
    screen.queue(r)
```
