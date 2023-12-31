from App.Scene.Battle.Local.Status import Status
from App.Screen import Screen
from App.Scene.Scene import Scene, EndOfScene
from App.Scene.Battle.Local.CharacterBand import HeroBand, EnemyBand
from App.Scene.Battle.Local.Box import Box
from App.Scene.Battle.Local.Combat import Combat
from App.Scene.Battle.Local.BattlePhase import BattlePhase
from App.Scene.Battle.Local.Choices import Choices
from App.Object.Ability import Ability
from App.Object.Fighter import Fighter
from App.Setup.Utils import battle_fight_logger, battle_scene_logger
from App.Setup.Globals import ANIMATE
from App.Scene.Battle.Local.Locals import *
from pygame.locals import K_x, K_z, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, MOUSEBUTTONDOWN, KEYDOWN
from pygame.event import Event
from pygame.mouse import get_pos
from random import choice


class Defeat(EndOfScene):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Victory(EndOfScene):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Battle(Scene):
    def __init__(self, screen: Screen):
        battle_scene_logger.info("Initializing the battle scene")
        super().__init__(screen)
        self.choices = Choices(3)
        self.combat = Combat()
        self.victory = False
        self.abilities_fallback: list[Ability] = list()


    def load_initial_frame(self, *args) -> None:
        battle_scene_logger.info("Creating the player's box")
        self.box = Box()
        battle_scene_logger.info("Moving the player's box")
        self.box.move(*BOX_POSITION)
        self.box.shift(*BOX_SHIFT)

        battle_scene_logger.info("Creating the hero band")
        heros: list[str] = list(args)
        self.heros = HeroBand(heros)
        battle_scene_logger.info("Moving the hero band")
        self.heros.move(*HEROBAND_POSITION)

        battle_scene_logger.info("Creating the enemy band")
        enemies = ENEMIES
        self.enemies = EnemyBand(enemies)
        battle_scene_logger.info("Moving the enemy band")
        self.enemies.move(*ENEMYBAND_POSITION)

        self.hero_status = Status(self.heros)
        self.hero_status.update()
        self.hero_status.move(*HERO_STATUS_POSITION)

        self.enemy_status = Status(self.enemies)
        self.enemy_status.update()
        self.enemy_status.move(*ENEMY_STATUS_POSITION)

        self.objects.pop()
        self.objects.append(self.box)
        self.objects.append(self.heros)
        self.objects.append(self.enemies)
        self.objects.append(self.hero_status)
        self.objects.append(self.enemy_status)

        battle_scene_logger.info("Drawing the box, heroband and enemyband to the Screen")
        self.screen.draw(*self.objects)


    def erase(self) -> None:
        battle_scene_logger.info("Erasing the box off the screen")
        r = self.box.erase()
        self.screen.queue(r)
        battle_scene_logger.info("Erasing the heroband off the screen")
        r = self.heros.erase()
        self.screen.queue(r)
        battle_scene_logger.info("Erasing the enemyband off the screen")
        r = self.enemies.erase()
        self.screen.queue(r)
        battle_scene_logger.info("Erasing hero status off the screen")
        r = self.hero_status.erase()
        self.screen.queue(r)
        battle_scene_logger.info("Erasing enemy status off the screen")
        r = self.enemy_status.erase()
        self.screen.queue(r)


    def check_event(self, event: Event) -> None:
        if event.type == QUIT:
            battle_scene_logger.info("QUIT event generated")
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            battle_scene_logger.info("MOUSEBUTTONDOWN event generated")
            if event.button == 1:
                x, y = get_pos()
                print(f"X: {x}, Y: {y}")
                return
        elif event.type == ANIMATE:
            battle_scene_logger.info("ANIMATE event generated")
            if self.box.state.value >= BattlePhase.SELECTING_HERO.value:
                hero: Fighter = self.heros.selector.select()
                vibrate_character(self, hero)
            if self.box.state.value == BattlePhase.SELECTING_ACTION.value:
                pass
            if self.box.state.value == BattlePhase.SELECTING_ABILITY.value:
                pass
            if self.box.state.value >= BattlePhase.SELECTING_ENEMY.value:
                enemy: Fighter = self.enemies.selector.select()
                vibrate_character(self, enemy)
        elif event.type == KEYDOWN:
            battle_scene_logger.info("KEYDOWN event generated")
            match self.box.state:
                case BattlePhase.SELECTING_HERO:
                    if event.key == K_z:
                        choose_hero(self)
                    elif event.key == K_UP:
                        move_hero_indicator(self, "up")
                    elif event.key == K_DOWN:
                        move_hero_indicator(self, "down")
                case BattlePhase.SELECTING_ACTION:
                    if event.key == K_z:
                        choose_action(self)
                    elif event.key == K_x:
                        change_phase(self, BattlePhase.SELECTING_HERO)
                    elif event.key == K_UP:
                        move_action_indicator(self, "up")
                    elif event.key == K_DOWN:
                        move_action_indicator(self, "down")
                    elif event.key == K_LEFT:
                        move_action_indicator(self, "left")
                    elif event.key == K_RIGHT:
                        move_action_indicator(self, "right")
                case BattlePhase.SELECTING_ABILITY:
                    if event.key == K_z:
                        choose_ability(self)
                    elif event.key == K_x:
                        change_phase(self, BattlePhase.SELECTING_ACTION, ACTION_LIST)
                    elif event.key == K_UP:
                        move_ability_indicator(self, "up")
                    elif event.key == K_DOWN:
                        move_ability_indicator(self, "down")
                    elif event.key == K_LEFT:
                        move_ability_indicator(self, "left")
                    elif event.key == K_RIGHT:
                        move_ability_indicator(self, "right")
                case BattlePhase.SELECTING_ENEMY:
                    if event.key == K_z:
                        choose_enemy(self)
                    elif event.key == K_x:
                        change_phase(self, BattlePhase.SELECTING_ABILITY, self.abilities_fallback)
                    elif event.key == K_UP:
                        move_enemy_indicator(self, "up")
                    elif event.key == K_DOWN:
                        move_enemy_indicator(self, "down")

        match self.box.state:
            case BattlePhase.SELECTING_HERO:
                pass
            case BattlePhase.SELECTING_ACTION:
                pass
            case BattlePhase.SELECTING_ABILITY:
                pass
            case BattlePhase.SELECTING_ENEMY:
                pass
            case BattlePhase.BATTLE_TIME:
                battle_scene_logger.info("It's time to battle!")
                self.choices.save()
                if self.choices.nothing_left_to_choose():
                    try:
                        fight(self)
                        update_status(self)
                    except (Defeat, Victory) as e:
                        raise e
                self.choices.clear()
                restart_round(self)


    def terminate(self) -> list[str]:
        battle_scene_logger.info("Terminating the battle scene")
        self.objects.pop() # enemy status out
        self.objects.pop() # hero status out
        self.objects.pop() # enemies out
        self.objects.pop() # heros out
        self.objects.pop() # box out
        return [VICTORY_TEXT] if self.victory else [DEFEAT_TEXT]


def change_phase(scene: Battle, phase: BattlePhase, *opts) -> None:
    battle_scene_logger.info("A new state will be loaded")
    rects = scene.box.set_state(phase, *opts)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)


def choose_hero(scene: Battle) -> None:
    hero = scene.heros.select()
    chosen_heros = map(lambda x: x[0], scene.choices.history)

    if hero in chosen_heros:
        print(REPEATED_HERO_WARNING)
        return
    elif hero.dead:
        print(DEAD_HERO_WARNING)
        return

    #battle_scene_logger.info("%s was chosen", hero.name)
    scene.choices.hero = hero
    change_phase(scene, BattlePhase.SELECTING_ACTION, ACTION_LIST)



def move_hero_indicator(scene: Battle, direction: str) -> None:
    rects = scene.heros.go(direction)
    for rect in rects:
        _, rect = scene.heros.refresh(rect)
        scene.screen.queue(rect)



def choose_action(scene: Battle) -> None:
    if scene.choices.hero is None:
        return

    scene.choices.action = scene.box.select()

    if scene.choices.action == ATTACK_ACTION:
        #battle_scene_logger.info("Attack action selected for hero %s", scene.choices.hero.name)
        abilities = scene.choices.hero.attacks.values()
    elif scene.choices.action == DEFEND_ACTION:
        #battle_fight_logger.info("Defend action selected for hero %s", scene.choices.hero.name)
        abilities = scene.choices.hero.defenses.values()
    elif scene.choices.action == PASS_ACTION:
        #battle_fight_logger.info("Pass action selected for hero %s", scene.choices.hero.name)
        change_phase(scene, BattlePhase.BATTLE_TIME)
        return
    else:
        raise Exception(f"'{scene.choices.action}' action was not yet implemented")

    scene.abilities_fallback = list(abilities)
    change_phase(scene, BattlePhase.SELECTING_ABILITY, abilities)



def move_action_indicator(scene: Battle, direction: str) -> None:
    rects = scene.box.go(direction)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def choose_ability(scene: Battle) -> None:
    ability_name = scene.box.select()

    hero = scene.choices.hero
    if hero is None:
        return

    if scene.choices.action == ATTACK_ACTION:
        ability = hero.attacks[ability_name]
    elif scene.choices.action == DEFEND_ACTION: 
        ability = hero.defenses[ability_name]
    else:
        raise NotImplementedError()

    if hero.mp.value < ability.cost:
        print(INSUFFICIENT_MANA_WARNING)
        return

    #battle_scene_logger.info("'%s' was chosen for %s", ability_name, scene.choices.hero.name)
    scene.choices.ability = ability_name
    if scene.choices.action == ATTACK_ACTION:
        change_phase(scene, BattlePhase.SELECTING_ENEMY)
    elif scene.choices.action == DEFEND_ACTION:
        scene.choices.target = None
        change_phase(scene, BattlePhase.BATTLE_TIME)
    else:
        raise Exception(f"{scene.choices.action} has no abilities available!")



def move_ability_indicator(scene: Battle, direction: str) -> None:
    rects = scene.box.go(direction)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)



def choose_enemy(scene: Battle) -> None:
    enemy = scene.enemies.select()
    if enemy.dead:
        print(DEAD_ENEMY_WARNING)
        return
    #battle_scene_logger.info("'%s' will be attacked by %s", enemy, scene.choices.hero.name)
    scene.choices.target = enemy
    scene.box.set_state(BattlePhase.BATTLE_TIME)



def move_enemy_indicator(scene: Battle, direction: str) -> None:
    rects = scene.enemies.go(direction)
    for rect in rects:
        _, rect = scene.enemies.refresh(rect)
        scene.screen.queue(rect)


def fight(scene: Battle) -> None:
    ordered_choices = sorted(scene.choices.history, key=lambda x: x[0].speed, reverse=True)
        
    battle_fight_logger.info("=== The fight has begun ===")
    battle_fight_logger.info("Attack order: %s", list(map(lambda x: x[0].name, ordered_choices)))
    battle_fight_logger.info("Speed order: %s", list(map(lambda x: x[0].speed, ordered_choices)))

    # heros always attack first :)
    for choices in ordered_choices:
        hero, action, ability, enemy = choices
        if ability is None:
            continue
        if enemy is not None:
            character_attacks(scene, hero, enemy, ability)
            if enemy.dead:
                rip_character(scene, enemy)
                if all_enemies_dead(scene):
                    battle_fight_logger.info("All enemies are dead. You've just won!")
                    scene.victory = True
                    raise Victory()
        else:
            character_defends(scene, hero, ability)

    # bad guys attack now
    for enemy in scene.enemies.fighters:
        if not enemy.alive:
            continue
        random_target = choice(scene.heros.fighters)
        random_ability = choice(list(enemy.attacks.values()))
        character_attacks(scene, enemy, random_target, random_ability.name)
        if random_target.dead:
            rip_character(scene, random_target)
            scene.choices.limit -= 1
            if scene.choices.limit == 0:
                battle_fight_logger.info("All heros are dead. You've been defeated!")
                scene.victory = False
                raise Defeat()

    restore_original_resistance(ordered_choices)
    regenerate_some_mp(scene)

    scene.choices.clear_history()



def rip_character(scene: Battle, hero: Fighter) -> None:
    """ takes a character out of combat """

    rect = hero.die()
    log = "{} died".format(hero.name)
    battle_fight_logger.info(log)
    if hero in scene.heros.fighters:
        _, rect = scene.heros.refresh(rect)
    else:
        _, rect = scene.enemies.refresh(rect)
    scene.screen.queue(rect)



def character_attacks(scene: Battle, attacker: Fighter, target: Fighter, ability: str) -> None:
    if not attacker.alive or not target.alive:
        return

    log = "{} will attack {} with {}".format(attacker.name, target.name, ability)
    battle_fight_logger.info(log)

    rects = scene.combat.attack(attacker, target, ability)  

    if attacker in scene.heros.fighters:
        _, rect = scene.heros.refresh(rects[0])
    else:
        _, rect = scene.enemies.refresh(rects[0])
    scene.screen.queue(rect)

    if target in scene.enemies.fighters:
        _, rect = scene.enemies.refresh(rects[1])
    else:
        _, rect = scene.heros.refresh(rects[1])
    scene.screen.queue(rect)



def character_defends(scene: Battle, character: Fighter, ability: str) -> None:
    if not character.alive:
        return
    log = "{} will defend by using {}".format(character.name, ability)
    battle_fight_logger.info(log)
    rect = scene.combat.defend(character, ability)
    if character in scene.heros.fighters:
        _, rect = scene.heros.refresh(rect)
    else:
        _, rect = scene.enemies.refresh(rect)
    scene.screen.queue(rect)



def restore_original_resistance(choices: list[tuple[Fighter, str, str | None, Fighter | None]]) -> None:
    for choice in choices:
        hero, action, ability, enemy = choice
        if hero.alive and action == DEFEND_ACTION:
            hero.resistance //= 2
            log = "{} had its resistance restored after defending by using {}".format(hero.name, ability)
            battle_fight_logger.info(log)



def all_enemies_dead(scene: Battle) -> bool:
    enemies_dead = list(map(lambda x: x.dead, scene.enemies.fighters))
    return all(enemies_dead)



def restart_round(scene: Battle) -> None:
    log = "=== A new round is starting ==="
    battle_scene_logger.info(log)

    rects = scene.box.set_state(BattlePhase.SELECTING_HERO)
    for rect in rects:
        _, rect = scene.box.refresh(rect)
        scene.screen.queue(rect)


def regenerate_some_mp(scene: Battle) -> None:
    """ regenerates a bit of the mana spent by each character """

    characters: list[Fighter] = list()
    characters.extend(scene.heros.fighters)
    characters.extend(scene.enemies.fighters)

    for character in characters:
        if character.dead:
            continue

        log = "{} will regenerate {} mana".format(character.name, character.mp.regen)
        battle_fight_logger.info(log)

        r = character.regen_attribute('mp')
        if character in scene.heros.fighters:
            _, r = scene.heros.refresh(r)
        else:
            _, r = scene.enemies.refresh(r)
        scene.screen.queue(r)


def vibrate_character(scene: Battle, fighter: Fighter) -> None:
    if fighter.character is None:
        return
    if fighter.dead:
        return

    battle_scene_logger.info("%s is currently being selected and will now vibrate", fighter.name)

    _, rect = fighter.character.vibrate(fighter.image)
    _, rect = fighter.refresh(rect)
    if fighter in scene.heros.fighters:
        _, rect = scene.heros.refresh(rect)
    elif fighter in scene.enemies.fighters:
        _, rect = scene.enemies.refresh(rect)
    scene.screen.queue(rect)


def update_status(scene: Battle) -> None:
    r = scene.hero_status.update()
    _, r = scene.hero_status.refresh(r)
    scene.screen.queue(r)

    r = scene.enemy_status.update()
    _, r = scene.enemy_status.refresh(r)
    scene.screen.queue(r)
        
