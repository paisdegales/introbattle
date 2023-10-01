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
* padronizar o nome das pastas local para Local
* sistema de eventos, objetos locais


O DESENHO DO 'BOX' MAIS ESPECIFICAMENTE DO CHOOSE ACTION N ESTA 100%:
    EH PRECISO PENSAR MELHOR SOBRE OS RETANGULOS QUE ESTAO SENDO RETORNADOS PARA SEREM ATUALIZADOS
    ESSES RETANGULOS SAO RELATIVOS A SURFACE DO 'BOX' EM SI, NAO A DA TELA
    ISSO SIGNIFICA QUE DEVERIAM TER QUE SER 'rect.move(box.rect.topleft)' PARA VIRAREM RELATIVOS A ORIGEM DA TELA

