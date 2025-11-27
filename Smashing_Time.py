import random
from tkinter import font
import copy
import pygame
import sys



pygame.init()

screen = pygame.display.set_mode((1400, 1120))
pygame.display.set_caption("Pygame Test")

clock = pygame.time.Clock()


hand = []
turn_count =  1
game_state = "fight"

print("hello world")

attack="attack"  #toying with the idea of defining move types as variables instead of strings
defend="defend"  #"Feeling like programing well, might delete later"
STR_up="STR-up"  
DEF_up="DEF-up" 




class move:
    def __init__(self, name, power, type, cost, tags):
        self.name = name
        self.power = power
        self.type = type
        self.cost = cost
        self.tags = tags

    def __repr__(self):
        return f"{self.name} (type: {self.type}, power: {self.power}, cost: {self.cost}, tags: {self.tags})"


Kori_pool = [
    move("Smash", 10, "attack", 1, tags={}),
    move("Smash", 10, "attack", 1, tags={}),
    move("Smash", 10, "attack", 1, tags={}),
    move("Defend", 10, "defend", 1, tags={}),
    move("Defend", 10, "defend", 1, tags={}),
    move("Defend", 10, "defend", 1, tags={}),
    move("SMASH!", 25, "attack", 2, tags={}),
    move("Enrage", 5, "STR-up", 1, tags={"enrage": None}),
    move("Gamble", 0, "spell", 1, tags={"redraw": True}),
    move("Deck out", 7, "defend", 1, tags={"draw": 2})
]


Joe_pool = [
    move("punch", 15, "attack", 999,  tags={}),
    move("punch", 15, "attack", 999,  tags={}),
    move("cower", 20, "defend", 999,  tags={}),
    move("cower", 20, "defend", 999,  tags={}),
    move("Calm breath", 5, "DEF-up", 999,  tags={})
]

Construct_pool = [
    move("slam", 30, "attack", 999,  tags={}),
    move("fortify", 30, "defend", 999,  tags={}),
    move("construct", 10, "STR-up", 999,  tags={})
]

Thug_pool = [
    move("poison strike", 10, "attack", 999, tags={"poison": 3}),
    move("smoke screen", 10, "defend", 999, tags={"blind": 1}),
    move("slash", 5, "attack", 999, tags={"multihit": 4}),
]


floor1_loot = [
    move("Smash", 10, "attack", 1, tags={}),
    move("Block", 4, "defend", 0, tags={}),
    move("Power Up", 5, "STR-up", 1, tags={}),
    move("poison strike", 7, "attack", 1, tags={"poison": 3}), #damages enemy at the end of turn
    move("Concentrate", 5, "DEF-up", 1, tags={}), 
    move("Shrug off", 20, "defend", 1, tags={}),
    move("Deck out", 7, "defend", 0, tags={"draw": 2}), #draw 2 cards
    move("Gamble", 0, "spell", 0, tags={"redraw": True}), #you draw a new hand, can only be used once per turn so you can't spam zero cost moves
    move("Smite" , 10, "attack", 1, tags={"blind": 2}), #makes enemy attacks do 75% damage
    move("Fury" , 6 , "attack", 1, tags={"multihit": 2}), #attack twice
    move("Glare", 5, "attack", 0, tags={"blind": 1}), #enemy attacks do 75% damage
    move("pray", 5, "defend", 1, tags={"energised":1, }), #I thought about making it heal but that would promote delaying kills, which is not fun, now it gives you +1 energy next turn
]



class champion:
    def __init__(self, name, maxHP, STR, DEF, pool, poolname):
        self.name = name
        self.maxHP = maxHP
        self.HP = maxHP
        self.start_STR = STR
        self.start_DEF = DEF
        self.STR = STR
        self.DEF = DEF
        self.alive = True
        self.pending_damage = 0
        self.block = 0
        self.pool = pool
        self.poolname = poolname
        self.status_effects = {}

    def __repr__(self):
        return f"{self.name} (maxHP: {self.maxHP}, HP: {self.HP}, STR: {self.STR}, DEF: {self.DEF}, pool: {self.poolname})"
    



class player(champion):
    def __init__(self, name, maxHP, STR, DEF, pool, poolname, MaxEnergy, drawNum):
        super().__init__(name, maxHP, STR, DEF, pool, poolname)
        self.MaxEnergy = MaxEnergy
        self.Energy = MaxEnergy
        self.drawNum = drawNum
        

    def __repr__(self):
        return f"{self.name} (HP: {self.HP}/{self.maxHP}, STR: {self.STR}, DEF: {self.DEF}, Energy: {self.Energy}, P.DMG: {self.pending_damage}, Block: {self.block}, pool: {self.poolname})"

    def make_hand(self):
        global hand
        global Player
        hand.clear()
        hand = random.sample(Player.pool, k=Player.drawNum)
        
    
    def resolve_move(self, move):
        global turn_count
        


        if self.Energy < move.cost:
            print("Not enough energy to play this move!")
            return 
        self.Energy -= move.cost
        
        multihit = 1
        for tag, tag_value in move.tags.items():
            if tag == "multihit":
                multihit = tag_value
                break

          # Remove the played card from hand
        while multihit >= 1:

            if move.type == "attack":
                if Enemy.alive == False:
                    print(f"{Enemy.name} is already dead! Talk about beating a dead horse.")
                    return

                given_damage = (move.power + self.STR) - (Enemy.block + Enemy.DEF)
                if given_damage < 0:
                    given_damage = 0

                Enemy.HP = Enemy.HP - given_damage

                x=(f"{Enemy.name} took {given_damage} ({Enemy.block} block")
                Enemy.block = Enemy.block - (move.power + self.STR)
                if Enemy.block > 0:
                    x += f" {Enemy.block} block remaining!)"
                else:
                    x += ")"
                    Enemy.block = 0

                print(x)
                given_damage = 0
                x = ""

            elif move.type == "defend":
                self.block += move.power + self.DEF
            elif move.type == "STR-up":
                self.STR += move.power
            elif move.type == "DEF-up":
                self.DEF += move.power 
            elif move.type == "spell": #all these moves are handled by tags
                pass
            else:
                print("What the fuck kind of move is that? What is happening?! I am going insane! AAARRRGH!!!")
                return
            

            for tag, tag_value in move.tags.items():
                if tag == "enrage":
                    x = move.power / 2
                    x = round(x)
                    print(f"Applying 'enrage' effect! DEF before: {self.DEF}, reducing by {x}")
                    self.DEF -= x
                
                

                elif tag == "energised":
                    if "energised" in self.status_effects:
                        self.status_effects["energised"] += tag_value
                    else:
                        self.status_effects["energised"] = tag_value

                elif tag == "blind":
                    if "blind" in Enemy.status_effects:
                        Enemy.status_effects["blind"] += tag_value  # Add to existing blind
                        print(f"Blind stacked! Total blind effect: {Enemy.status_effects['blind']}")
                    else:
                        Enemy.status_effects["blind"] = tag_value # Initial blind application
                        x = Player.pending_damage*0.75
                        x = round(x)
                        Player.pending_damage = x
                
                elif tag == "poison":
                    if "poison" in Enemy.status_effects:
                        Enemy.status_effects["poison"] += tag_value  # Add to existing poison
                        print(f"Poison stacked! Total poison damage: {Enemy.status_effects['poison']}")
                    else: # now we give it poison
                        Enemy.status_effects["poison"] = tag_value # Initial poison application
                    
                elif tag == "draw":
                    new_cards = random.sample(self.pool, k=tag_value)
                    hand.extend(new_cards)
                    print(f"Drew {tag_value} cards: {[card.name for card in new_cards]}")

                elif tag == "redraw":
                    Player.make_hand()
                    print(f"Redrew hand: {[card.name for card in hand]}")
            
            multihit -= 1

        if Enemy.HP <= 0:
            Enemy.alive = False
        game.kill_enemy()
        


        hand.remove(move)





    def take_damage(self):
        if not self.alive:
            print(f"{self.name} is fucking dead and cannot take more damage!")
            return

        damage_resolved = (self.pending_damage + Enemy.STR) - (self.block + self.DEF)
        if damage_resolved < 0:
            damage_resolved = 0

        self.HP = self.HP - damage_resolved

        x = (f"{self.name} took {damage_resolved} damage ({self.block} block")
        self.block = self.block - (self.pending_damage + Enemy.STR)
        if self.block > 0:
            x += f" {self.block} block remaining!)"
        else:
            x += ")"
            self.block = 0

        print(x)
        self.pending_damage = 0
        damage_resolved = 0
        x = ""




        if self.HP <= 0:
            self.alive = False  
            print(f"{self.name} has been defeated!") 

            












Kori = player("Kori", 100, 0, 0, Kori_pool, "Kori pool", 3, 5)
Player = copy.deepcopy(Kori)



class foe(champion):
    def __init__(self, name, maxHP, STR, DEF, pool, poolname):
        super().__init__(name, maxHP, STR, DEF, pool, poolname)  
    


    def __repr__(self):
        return f"{self.name} (HP: {self.HP}/{self.maxHP}, STR: {self.STR}, DEF: {self.DEF}, pool: {self.poolname}, P.DMG: {self.pending_damage}, Block: {self.block})"

    def make_enemy_move(self):
        enemy_move = random.choice(self.pool)
        self.enemy_move = enemy_move
        
        multihit = 1
        for tag, tag_value in enemy_move.tags.items():
            if tag == "multihit":
                multihit = tag_value
                break


        while multihit >= 1:
            if enemy_move.type == "attack": 
                if "blind" in Player.status_effects:
                    x = (enemy_move.power + self.STR)*0.75
                    x = round(x)
                    Player.pending_damage += x
                else:
                    Player.pending_damage += enemy_move.power + self.STR
            elif enemy_move.type == "defend":
                self.block += enemy_move.power + self.DEF
            elif enemy_move.type == "STR-up":
                self.STR += enemy_move.power
            elif enemy_move.type == "DEF-up":
                self.DEF += enemy_move.power
            elif enemy_move.type == "spell": #all these moves are handled by tags
                pass

            for tag, tag_value in enemy_move.tags.items():
                if tag == "poison":
                    Player.status_effects["poison"] += tag_value  
                    print(f"Poison stacked! Total poison damage: {Player.status_effects['poison']}")
                elif tag == "blind":
                    if "blind" in Player.status_effects:
                        Player.status_effects["blind"] += tag_value  # Add to existing blind
                        print(f"Blind stacked! Total blind effect: {Player.status_effects['blind']}")
                    else:
                        Player.status_effects["blind"] = tag_value # Initial blind application
                elif tag == "heal":
                    self.HP += tag_value
                    if self.HP > self.maxHP:
                        self.HP = self.maxHP
                    print(f"{self.name} healed for {tag_value} HP! Current HP: {self.HP}")   
                
            multihit -= 1
 

        print(f"{self.name} used {enemy_move.name}!")

    



Joe=foe("Joe", 50 + random.randint(-5, 5), 0, 0, Joe_pool, "Joe pool")
Construct = foe("Construct", 100, 0, 0, Construct_pool, "Construct pool")
Thug = foe("Thug", 80 + random.randint(-5, 5), 5 + random.randint(-1, 1), 0, Thug_pool, "Thug pool")

Enemy = copy.deepcopy(Joe)
floor1_enemies = [Joe, Construct]




class gameloop:
    def __init__(self, Player, enemy):
        self.Player = Player
        self.enemy = enemy

    def __repr__(self):
        return f"Game Loop (Player: {self.Player}, Enemy: {self.enemy})"

    def draw_button(self, screen, button_rect, text):     #button function
        pygame.draw.rect(screen, (0, 128, 255), button_rect)  # color: blue
        font = pygame.font.SysFont(None, 18)    #default font, size 18
        text_surface = font.render(text, True, (255, 255, 255)) # text, anti-aliased, white
        screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))


    def draw_hand(self,screen, hand, start_x, start_y, end_x,  card_width, card_height):

        L = end_x - start_x
        
        spacing = (L - len(hand)*card_width) / (len(hand) + 1)

        for i, card in enumerate(hand):
            card_rect = pygame.Rect(start_x + i * (card_width + spacing), start_y, card_width, card_height)
            pygame.draw.rect(screen, (255, 255, 255), card_rect)  # White card background
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(card.name, True, (0, 0, 0))  # Black text
            text_rect = text_surface.get_rect(center=card_rect.center)
            screen.blit(text_surface, text_rect) # Draw card name centered on the card


    def assign_new_enemy(self):
        global Enemy
        if Enemy.alive == False:
            print(f"{Enemy.name} has been defeated! A new enemy approaches!")
            Enemy = copy.deepcopy(random.choice(floor1_enemies))
            print(f"A wild {Enemy.name} appears!")
        
    def kill_enemy(self):
        global turn_count
        global Enemy
        if Enemy.HP <= 0:
            Enemy.alive = False
            print(f"{Enemy.name} has been defeated! A new enemy approaches!")
            game.start_new_card_selection()
            game.assign_new_enemy()
            game.end_turn()
            turn_count = 0

    def end_turn(self):
        global turn_count
        global hand
        global Player
        global Enemy

        print()
        print(f"New turn, {turn_count}")
        turn_count += 1

        Player.block = 0
        Enemy.block = 0

        if "poison" in Enemy.status_effects:
            poison_damage = Enemy.status_effects["poison"]
            Enemy.HP -= poison_damage
            print(f"{Enemy.name} takes {poison_damage} poison damage!")
            Enemy.status_effects["poison"] -= 1
            if Enemy.status_effects["poison"] <= 0:
                del Enemy.status_effects["poison"]
            game.kill_enemy()
        
        if "poison" in Player.status_effects:
            poison_damage = Player.status_effects["poison"]
            Player.HP -= poison_damage
            print(f"{Player.name} takes {poison_damage} poison damage!")
            Player.status_effects["poison"] -= 1
            if Player.status_effects["poison"] <= 0:
                del Player.status_effects["poison"]
        
        if "blind" in Player.status_effects:
            Player.status_effects["blind"] -= 1
            if Player.status_effects["blind"] <= 0:
                del Player.status_effects["blind"]

        if "blind" in Enemy.status_effects:
            Enemy.status_effects["blind"] -= 1
            if Enemy.status_effects["blind"] <= 0:
                del Enemy.status_effects["blind"]

        Player.take_damage() 

        Enemy.make_enemy_move()

        Player.Energy = Player.MaxEnergy
        if "energised" in Player.status_effects:
            Player.Energy += Player.status_effects["energised"]
            print(f"{Player.name} is energised and gains {Player.status_effects['energised']} extra energy this turn!")
            del Player.status_effects["energised"]


        Player.make_hand()

        print(f"New hand: {hand}")
        print()

    def start_new_card_selection(self):
        global floor1_loot
        global game_state
        global current_choices

        game_state = "choose_new_card"

        current_choices = random.sample(floor1_loot, 3)

        print("Choose a new card to add to your pool:")
        for i, card in enumerate(current_choices):
            print(f"{i + 1}: {card.name}")

    def make_choice_new_card(self):
        global current_choices

        for i, card in enumerate(current_choices):
            pygame.draw.rect(screen, (255, 255, 255), (200 + i * 200, 300, 150, 50))
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(card.name, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(200 + i * 200 + 75, 300 + 25))
            screen.blit(text_surface, text_rect)


    def handle_choice_new_card(self):
        global game_state
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(current_choices)):
                choice_rect = pygame.Rect(200 + i * 200, 300, 150, 50)
                if choice_rect.collidepoint(event.pos):
                    chosen_card = current_choices[i]
                    Player.pool.append(chosen_card)
                    print(f"You chose {chosen_card.name} to add to your pool!")
                    game_state = "fight"
                    return

    def start_game(self):
        None
    
    #MAP GENERATING MAP HERE:
    import random

    def create_layers(num_layers=6, width_range=(2, 4)):
        layers = []

        for layer_index in range(num_layers):
            layer_width = random.randint(*width_range)

            layer = []
            for node_index in range(layer_width):
                node = Encounter_node(id=f"{layer_index}-{node_index}")
                layer.append(node)

            layers.append(layer)
      
        
    def assign_encounters(layers):
        encounter_types = ["battle", "elite", "shop", "rest", "event"]

        for layer in layers:
            for node in layer:
                node.encounter_type = random.choice(encounter_types)
                node.danger = random.randint(1, 5) #AI randomly generated me this, but I actually think this is a pretty good idea. It gives you a nice piece of risk and reward "do I go into the more dangerous place with a shop or the safer one without it"


        return layers






class Encounter_node:
    def __init__(self, node_id, encounter_type, data=None):
        self.id = node_id
        self.encounter_type = encounter_type   # "battle", "shop", "elite", etc.
        self.data = data or {}                 # loot, enemies, modifiers…
        self.next_nodes = []                   # list of IDs or direct object refs

    
game = gameloop(Player, Enemy)







# Define your squares: x, y, width, height (rearranged for 1400x1120 window)
# Left column: player info and actions; Right column: enemy info and actions
player_square = pygame.Rect(50, 100, 500, 80)
enemy_square = pygame.Rect(850, 100, 500, 80)

# Action buttons under each character panel
player_attack_square = pygame.Rect(50, 220, 500, 80)
enemy_attack_square = pygame.Rect(850, 220, 500, 80)

# Center control buttons
resolve_square = pygame.Rect(600, 720, 200, 80)
end_turn_square = pygame.Rect(600, 830, 200, 80)

# Intent and status panels
enemy_intent = pygame.Rect(850, 320, 500, 80)
player_status_square = pygame.Rect(50, 320, 500, 80)
enemy_status_square = pygame.Rect(850, 420, 500, 80)

# Top-center turn counter
turn_count_square = pygame.Rect(600, 0, 200, 60)

# Bottom-center new card chooser
choose_new_card_square = pygame.Rect(600, 980, 200, 80)


Player.make_hand()


def basic_draw():
    game.draw_button(screen, player_square, Player.__repr__())
    game.draw_button(screen, enemy_square, Enemy.__repr__())
    game.draw_button(screen, player_attack_square, "Player Attack")    
    game.draw_button(screen, enemy_attack_square, "Enemy Attack")
    game.draw_button(screen, resolve_square, "Resolve Damage")
    game.draw_button(screen, end_turn_square, "End Turn")
    game.draw_hand(screen, hand, hand_start_x, hand_start_y, end_x, hand_card_width, hand_card_height)
    game.draw_button(screen, enemy_intent, f"Enemy Intent: {Enemy.enemy_move if hasattr(Enemy, 'enemy_move') else 'None'}")
    game.draw_button(screen, turn_count_square, f"Turn: {turn_count}")
    game.draw_button(screen, choose_new_card_square, "Choose New Card")
    game.draw_button(screen, enemy_status_square, f"Enemy Status: {Enemy.status_effects}")
    game.draw_button(screen, player_status_square, f"Player Status: {Player.status_effects}")


hand_start_x = 200
hand_start_y = 500
hand_card_width = 100
hand_card_height = 150 
end_x= 800




enemy_move = Enemy.make_enemy_move()

while True:
    screen.fill((0, 0, 0))

    if game_state == "fight":
        basic_draw()
    if game_state == "choose_new_card":
        game.make_choice_new_card()
        




    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()

        if game_state == "fight":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_attack_square.collidepoint(event.pos):
                    print()
                    print("Player Attack button clicked!")
                    Enemy.HP -= 10  # Example action
                    print(f"Enemy.HP: {Enemy.HP}")

                elif choose_new_card_square.collidepoint(event.pos):
                    print()
                    print("Choose New Card button clicked!")
                    game.start_new_card_selection()

                elif enemy_attack_square.collidepoint(event.pos):
                    print()
                    print("Enemy Attack button clicked!")
                    Player.pending_damage += 10  # Example action
                    print(f"Player.pending_damage: {Player.pending_damage}")

                elif resolve_square.collidepoint(event.pos):
                    print()
                    print("Resolve Damage button clicked!")
                    Player.take_damage()

                elif end_turn_square.collidepoint(event.pos):
                    print()
                    print("End Turn button clicked!")
                    game.end_turn()

                
                for i, card in enumerate(hand):
                    # Calculate spacing exactly like draw_hand so the clickable rect matches drawn position
                    spacing = (end_x - hand_start_x - len(hand) * hand_card_width) / (len(hand) + 1) if (len(hand) + 1) > 0 else 0
                    card_x = hand_start_x + i * (hand_card_width + spacing)
                    card_rect = pygame.Rect(card_x, hand_start_y, hand_card_width, hand_card_height)
                    if card_rect.collidepoint(event.pos):
                        print()
                        print(f"Card {card.name} clicked!")
                        Player.resolve_move(card)
                        print(f"Played {card}. New hand: {hand}")
                        print(f"Enemy pending_damage: {Enemy.pending_damage}, Player block: {Player.block}")
                        break  # Exit loop after playing one card
        
        if game_state == "choose_new_card":
            game.handle_choice_new_card()





    pygame.display.flip()
    clock.tick(60)
