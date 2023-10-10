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

# TODO

* criar todos os objetos capazes de se automanipularem (ou seja, atualizarem suas 'images')
    * refazer todos objetos de todas as cenas (fazer objetos completos, que consigam gerar superficies novas sob demanda)
* reforçar uso de variaveis apenas definidas no arquivo Globals.py
* talvez implementar algo usando a biblioteca 'argparse'
* talvez investigar como está o uso de memoria ram usando a biblioteca 'tracemalloc'
* talvez usar json em vez de constantes soltas nos arquivos de config/setup
* melhorar a documentação do codigo (tentar aprender como sao documentadas funcoes pelo 'pydoc' e replicar)
* talvez usar mais o modulo 'doctest', que é muito util alias
* talvez melhorar as anotacoes que foram usadas usando o modulo 'typing'
* criar arquivo de log usando o modulo 'logging'

# Fazendo agora
1. SISTEMA DE COMBATE
* criar a classe de ability, attack, defense para todos os herois
    * essa classe tera que receber um objeto da classe Fighter (um Fighter tem uma Ability)
* criar ataques e defesas para todos os herois e inimigos
* fazer sistema de combate
    * provavelmente uma classe (talvez chamada Combat) que consiga fazer um Fighter atacar outro Fighter, ambos usando uma habilidade
    * ao conseguir fazer um fighter atacar outro, fazer um metodo que permita um conjunto de fighters (baseado no atributo speed) atacar um outro conjunto de enemies

2. CENAS
* a cena de Battle precisa ser reconstruida do zero
* sistema de eventos, objetos locais


Eu acho que a classe seletor poderia ser melhorada de alguma forma.
Isso porque diferentes objetos da classe CompoundObject (que alias ainda não existe,
mas que seria uma subclasse de BaseObject especifica para conter outras instancias
de BaseObject enquanto atributos) e que tem um objeto da classe 'Selector'
acabam implementando metodos relacionados varias vezes para conseguir:
atualizar o desenho do seletor em suas imagens, obter uma referencia ao que o seletor aponta e etc


Isso faz com que metodos como 'go' e 'select' sejam implementados na classe CompoundObject varias vezes
Isso é bem chato e introduz muitos problemas de manuntenção do código, pois diferentes maneiras de se fazer
uma mesma coisa acabam coexistindo de maneira silenciosa no codigo.
Exemplos de classes que implementam esses metodos são: 'Box', 'CharacterBand', 'GuildOptions' and maybe more


Outra reclamação: o metodo 'select' da classe CompoundObject apresenta um pessimo nome, isso porque a classe Selector
tambem implementa um metodo com o mesmo nome mas com semantica diferente. Na class CompoundObject
esse metodo serve para devolver o que a seta está apontando atualmente na tela. Ja na classe Selector esse metodo
serve para atualizar a posicao do seletor apos multiplas chamadas dos metodos 'up', 'down', 'left' e 'right'


Outra rotina corriqueira no codigo mas que acaba sendo implementada diversas maneiras um pouco diferente entre si
é o desenho/atualização na tela de um componente da classe CompoundObject. Em geral, a rotina envolve:
1. apagar e redesenhar a superficie do componente em questão na superficie do objeto raiz (CompoundObject)
2. retornar as areas que foram modificadas ao apagar e desenhar o componente
    * essas areas são da classe 'Rect' e utilizam coordenadas relativas em relação ponto topleft do objeto raiz
3. coletar as areas modificadas e chamar o metodo 'refresh' do objeto raiz para atualizar (na tela em que esta desenhado) aquelas regioes suas que sofreram modificacao
4. coletar a area modificada pelo metodo 'refresh' do passo anterior e adiciona-la a fila de atualizacoes pendentes na tela pelo metodo 'queue' da classe Tela


# PLANO DE AÇÃO
1. Implementar o método 'go' para a classe Selector, que tomara conta de
  apagar/redesenhar o seletor após ter sido movido por chamadas a um dos
  metodos 'up', 'down', 'left' ou 'right', seguido de uma chamada ao metodo
  'select'
    * Testar o seletor novo na main
    * Apagar o boiler plate code contido nas classes que implementavam o metodo 'go' elas mesmas
2. Voltar a implementar a classe 'TurnHandler'
    * se encarrega de atualizar todos os componentes necessarios da cena de batalha após o jogador escolher o heroi, ação, habilidade e alvo
