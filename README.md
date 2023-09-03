# Introbattle

This is a showcase of a game built using pygame

This project is originally part of Introcomp, a programming course of the Federal University of Espirito Santo (UFES)

You can found more about Introcomp on instagram: @introcompufes

---

## How to play

Clone this repo
`git clone https://github.com/paisdegales/introbattle.git`

Navigate to the project's folder
`cd path/to/introbattle`

Install all requirements
`pip freeze -r requirements.txt`

Run the game
`python main.py`

And voila! now you can play it! hooray!

---

## How the game looks

Include some cool images :)

---

## Folder structure

* App 
    * Font
    * Resource
        > all images, font files, game sounds are here
        * Background
            > background art
        * Character
            > hero art
        * Fonts
            > fonts (zipped from [Google Fonts](https://fonts.google.com/))
        * UI
            > ui art
    * Scene
        > all game scenes
        * Battle
            > the scene where the player actually plays the game
            * Locals
                > specifics of the battle scene
        * Menu
            > the scene where the player chooses its heros
            * Local
                > specifics of the menu scene
    * Screen
        > display screen management
    * Setup
        > configuration and miscellaneous

---

# TODO

* parei implementando a box de status
    * precisarei implementar o metodo __getitem__ na classe de fighterattributes para conseguir ter acesso ao dicionario dela? q
* talvez repensar num modo mais pratico para localizar recursos no projeto, em vez de usar o 'folders'. Talvez usar strings estaticas mesmo (usando as funcoes dispobilizados pelo os.path para operar entre diretorios eh claro)
