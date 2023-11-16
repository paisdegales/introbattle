# Introbattle

This is a showcase of a game built using pygame

This project is originally part of Introcomp, a programming course of the
Federal University of Espirito Santo (UFES)

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
1. Padronizar a cena, de modo que seus objetos e ela propria utilize variáveis
   definidas no arquivo 'Globals.py' ou 'Locals.py'
2. Implemetar o botao que permite voltar para a escolha anterior na batalha
   são tomadas
3. Dar um jeito de regenerar a mana dos herois/inimigos de vez em quando
4. Criar caixa de status dos personagens
5. Criar terceira e ultima cena do jogo: banner com "You win!" em
   verde ou "You lose!" em vermelho, com um moving character
controlado pelas setas do teclado
6. Melhorar arquivo de log, com mais coverage sobre a cena de Batalha
7. Balancear os bonecos


# BACKLOG

* reforçar uso de variaveis apenas definidas no arquivo Globals.py
* talvez implementar algo usando a biblioteca 'argparse'
* talvez investigar como está o uso de memoria ram usando a biblioteca
  'tracemalloc'
* talvez usar json em vez de constantes soltas nos arquivos de config/setup
* melhorar a documentação do codigo (tentar aprender como sao documentadas
  funcoes pelo 'pydoc' e replicar)
* talvez usar mais o modulo 'doctest', que é muito util alias
* talvez melhorar as anotacoes que foram usadas usando o modulo 'typing'
* Talvez ir destruindo alguns objetos com `del` para poupar ram


# ANOTAÇÕES
Outra rotina corriqueira no codigo mas que acaba sendo implementada diversas
maneiras um pouco diferente entre si é o desenho/atualização na tela de um
componente da classe CompoundObject. Em geral, a rotina envolve:
1. apagar e redesenhar a superficie do componente em questão na superficie do
   objeto raiz (CompoundObject)
2. retornar as areas que foram modificadas ao apagar e desenhar o componente
    * essas areas são da classe 'Rect' e utilizam coordenadas relativas em
      relação ponto topleft do objeto raiz
3. coletar as areas modificadas e chamar o metodo 'refresh' do objeto raiz para
atualizar (na tela em que esta desenhado) aquelas regioes suas que sofreram
modificacao
4. coletar a area modificada pelo metodo 'refresh' do passo anterior e
adiciona-la a fila de atualizacoes pendentes na tela pelo metodo 'queue' da
classe Tela

```python
    s, r = paladin.vibrate(screen.image)
    screen.queue(r)
    r = hunter.vibrate_component("character")
    screen.queue(r)
    r = portrait.vibrate_component("hero")
    screen.queue(r)
```

Uma coisa que poderia ter sido feita é uma classe que abstrai o conceito de
Surface do pygame. Essa nova classe poderia ser usada para identificar com
facilidade que superficie um objeto eh desenhado sobre. Alem disso, uma
subclasse dessa classe poderia representar a superficie da tela, que é uma
superficie 'especial' no meu ponto de vista.

A classe Grid poderia ser uma classe que gera coordenadas em tempo real,
em vez de armazenar um dicionario com todos os grid que possui e gerar
as coordenadas baseando-se nesse dicionario
* Essa ideia é impraticável, porque ficaria dificil gerar coordenadas de um 
grid nao regular (com algumas linhas e colunas shiftadas, por exemplo)
