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
│   │   └── Locals
│   └── Menu
│       └── Local
├── Screen
└── Setup
```


---

# TODO

* criar todos os objetos capazes de se automanipularem (ou seja, atualizarem suas 'images')
    * refazer todos objetos de todas as cenas (fazer objetos completos, que consigam gerar superficies novas sob demanda)
    * exemplo: fighter tem vida, mana e energia. Quando gasta uma habilidade, automaticamente a superficie da vida, da mana e da energia são atualizadas.
        * isso vai requerer que o fighter em si seja um objeto e que vai ter outros objetos como atributos (poderao ser controlados pela propria classe), que irao ser acionados para gerarem suas superficies de novo (sob demanda)
* fazer objeto que seja capaz de renderizar textos
* reforçar uso de variaveis apenas definidas no arquivo Globals.py
* remover Setup/FolderNavigation.py e prover na verdade caminhos até todas as pastas de recursos do projeto no arquivo Globals.py
* talvez a nova classe 'Pen' deveria ficar na pasta Object

# MUDANÇAS
* classe objeto completamente repensada
    * sem addons, ideia porca removida
    * objetos são bem mais simples agora
    * nome do atributo 'surface' trocado para 'image' para se comunicar com a terminologia usada pelos sprites
    * a classe BaseObject só aceita agora surfaces prontas no seu construtor. É necessário especializar subclasses de BaseObject que gerem surfaces de maneira especifica (metodos como 'Surface', 'load', 'font.render')
    * classe 'Objeto' serve apenas para desenhar em outra superficie. Caso a superficie a ser desenhadapertença a outro objeto, voila! temos objetos aninhados (ou addons)
    * metodo 'draw' agora retorna o que é necessario para apagar o que acabou de ser desenhado (superficie apagadora e posicao onde foi desenhado na superficie)
* classe 'Screen' agora representa a superficie da tela do jogo. Todas subclasses de 'BaseObject' que apareceram na tela do jogo deve ser adicionados pelo metodo 'draw'.
* a classe 'Screen' se encarrega de apagar corretamente tudo que foi desenhado nela, no entanto é necessário se atentar a ordem com que os objetos foram desenhados, pois a 'Screen' nao cuida disso e isso pode causar efeitos indesejados caso uma superficie que esteja embaixo de outra seja apagada primeiro

# MUDANÇAS SENDO REPENSADAS
* talvez seria interessante o objeto guardar o superficie em que foi desenhado, a posicao e o que estava ali antes dele aparecer
