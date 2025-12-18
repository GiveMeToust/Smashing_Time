import random
import time
from tkinter import font
import copy
import pygame
import sys



pygame.init()

screen = pygame.display.set_mode((1400, 1120))
pygame.display.set_caption("Pygame Test")

clock = pygame.time.Clock()

chance_of_branching = 0.5  # 50% chance to branch sideways in encounter map generation

encounter_types = ["enemy", "shop", "rest", "event"]
weights =          [   80,      5,      5,      10   ]  # might scrap events

dramatic_pause = False #flag for dramatic pause before you get forwarded to an enemy encounter from the map, kinda silly but whatever
dramatic_pause_timer = 1.5  # seconds



hand = []
turn_count =  1
game_state = "fight"
rest_done = False

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

Repair_Man_pool = [
    move("weld", 20, "attack", 999, tags={}),
    move("empty magazine", 3, "attack", 999, tags={"multihit": 6}),
    move("brace", 20, "defend", 999, tags={}),
    move("patch up", 20, "defend", 999, tags={"heal": 15}),
    move("overclock", 10, "STR-up", 999, tags={}),
]


floor1_loot = [
    move("Smash", 10, "attack", 1, tags={}),
    move("Block", 4, "defend", 0, tags={}),
    move("Power Up", 5, "STR-up", 1, tags={}),
    move("poison strike", 7, "attack", 1, tags={"poison": 3}), #damages enemy at the end of turn, then loses 1 poison
    move("poison bomb", 2, "attack", 2, tags={"poison": 5}), 
    move("Concentrate", 5, "DEF-up", 1, tags={}), 
    move("Shrug off", 20, "defend", 1, tags={}),
    move("Deck out", 7, "defend", 0, tags={"draw": 2}), #draw 2 cards
    move("Gamble", 0, "spell", 0, tags={"redraw": True}), #you draw a new hand, can only be used once per turn so you can't spam zero cost moves
    move("Smite" , 10, "attack", 1, tags={"blind": 2}), #makes enemy attacks do 75% damage
    move("Fury" , 6 , "attack", 1, tags={"multihit": 2}), #attack twice
    move("Glare", 5, "attack", 0, tags={"blind": 1}), #enemy attacks do 75% damage for x turns
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
        self.current_node = None # player's current position on the map, current_node = layers[0][0] is not yet defined so I have to set it up later because coding is stupid and not a real person like it should be. Fucking moron. All my code should be run by genetically modified hamsters with PhDs in computer science, not by this piece of shit garbage that can't even remember to set a variable properly
        

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
        
        # Remove the played card from hand immediately
        hand.remove(move)
        
        multihit = 1
        for tag, tag_value in move.tags.items():
            if tag == "multihit":
                multihit = tag_value
                break
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

    



Joe=foe("Joe", 50 + random.randint(-5, 5) , 0, 0, Joe_pool, "Joe pool")
Construct = foe("Construct", 100, 0, 0, Construct_pool, "Construct pool")
Thug = foe("Thug", 80 + random.randint(-5, 5), 5 + random.randint(-1, 1), 0, Thug_pool, "Thug pool")
Repair_Man = foe("Repair Man", 90, 0, 0, Repair_Man_pool, "Repair Man pool")

Enemy = copy.deepcopy(Joe)







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
        Enemy = copy.deepcopy(random.choice(floor1_enemies))
        Enemy.maxHP = round(Enemy.maxHP*(1 + (Player.current_node.danger_level * 0.1)))
        Enemy.HP = Enemy.maxHP
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


    def apply_status_effects(self):
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




    def handle_basic_logic(self):
        global game_state
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

            elif force_map.collidepoint(event.pos):
                print()
                print("Force Map button clicked!")
                map_generation.prepare_map()

            elif force_rest.collidepoint(event.pos):
                print()
                print("Force Rest button clicked!")
                game_state = "rest"
                
            
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
                    map_generation.prepare_map()
                    return

    def start_game(self):
        None
    

#--------------------------- Generate Map ---------------------------


class node_generation_or_something_idk:
    def __init__(self, layer, layer_index, encounter_type):
        self.layer = layer
        self.layer_index = layer_index
        self.encounter_type = encounter_type
        self.danger_level = 0
        self.escpecially_dangerous = False
        self.connections = []
        self.node_x = 0
        self.node_y = 0

    
    
    def generate_layers(self, layer_width=4, layer_depth=8):
        # layer_width: number of nodes per layer
        # layer_depth: number of layers

        layers = []  # this will hold all the layers



        for layer_count in range(layer_depth):
            layers.append([])  

            for node_count in range(layer_width):
                if layer_count == 0:
                    if node_count == 0:
                        encounter_type = "start"
                    else:
                        continue  # only one start node
                elif layer_count == layer_depth - 1:
                    if node_count == 0:
                        encounter_type = "boss"
                    else:
                        continue  # only one boss node
                else:
                    encounter_type = random.choices(encounter_types, weights=weights, k=1)[0]

                node = node_generation_or_something_idk(layer_count, node_count, encounter_type)
                layers[layer_count].append(node)

        return layers

    
    

    def connect_layers(self, layers):
        num_layers = len(layers)
        if num_layers < 2:
            return layers

        for layer_idx in range(num_layers - 1):
            cur = layers[layer_idx]
            nxt = layers[layer_idx + 1]

            # fast skip if current or next layer empty (shouldn't occur normally)
            if not cur or not nxt:
                continue

            # 1) Primary pass: ensure every current node has at least one outgoing
            for node in cur:
                idx = node.layer_index

                # clamp index to valid range of next layer so we always have a target
                straight_idx = max(0, min(idx, len(nxt) - 1))
                straight_target = nxt[straight_idx]
                # add straight connection if not already there
                if straight_target not in node.connections:
                    node.connections.append(straight_target)

                # optional sideways: left or right neighbor in next layer
                if random.random() < chance_of_branching:
                    direction = random.choice([-1, 1])  # -1 => left, +1 => right
                    sideways_idx = idx + direction
                    if 0 <= sideways_idx < len(nxt):
                        sideways_target = nxt[sideways_idx]
                        if sideways_target not in node.connections:
                            node.connections.append(sideways_target)

            # 2) Secondary pass: guarantee each node in next layer has >= 1 incoming
            # Build incoming counts
            incoming_map = {t: 0 for t in nxt}
            for parent in cur:
                for t in parent.connections:
                    if t in incoming_map:
                        incoming_map[t] += 1

            # For any target with 0 incoming, pick a random parent and connect it
            no_incoming = [t for t, cnt in incoming_map.items() if cnt == 0]
            for target in no_incoming:
                parent = random.choice(cur)
                if target not in parent.connections:
                    parent.connections.append(target)

        return layers

    def assign_node_positions(self):
        if self.encounter_type == "start":
            self.node_x = 500 # middle of the row of nodes, subject to change but I don't want to bother with calculating it
            self.node_y = 100 + self.layer * 120 #self.layer is zero
        elif self.encounter_type == "boss":
            self.node_x = 500
            self.node_y = 100 + self.layer * 120 #self.layer is not zero
        else:
            self.node_x = 200 + self.layer_index * 200
            self.node_y = 100 + self.layer * 120

    def assign_node_danger_level(self):
       if self.encounter_type == "enemy":
            self.danger_level = self.layer * 1
            if random.random() < 0.2:  # 20% chance to increase danger level
                self.danger_level += 3
                self.escpecially_dangerous = True


    def __repr__(self):
        return f"{self.encounter_type} {self.layer}, {self.layer_index}"
    

    def prepare_map(self): # So this is pretty much useless
        global game_state
        game_state = "map"

    
    def draw_map(self):
        for layer in layers:
            for node in layer:
                
                # Draw connections
                for target in node.connections:
                    pygame.draw.line(screen, (255, 255, 255), (node.node_x, node.node_y), (target.node_x, target.node_y), 2) # white , width 2
                    #I have literally no idea why this works. And I mean LITERALLY no idea. But it does. Like, what the hell is even "target"???
                    # Nevermind, I am just sleep deprived. It's extremely obvious what target is. I am an idiot.


                if node.encounter_type == "start":
                    pygame.draw.circle(screen, (0, 255, 0), (node.node_x, node.node_y), 30)  # Green for start
                    font = pygame.font.SysFont(None, 24)
                    text_surface = font.render(node.encounter_type, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(node.node_x, node.node_y))
                    screen.blit(text_surface, text_rect)


                elif node.encounter_type == "boss":
                    pygame.draw.circle(screen, (255, 0, 0), (node.node_x, node.node_y), 30)  # Red for boss
                    font = pygame.font.SysFont(None, 24)
                    text_surface = font.render(node.encounter_type, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(node.node_x, node.node_y))
                    screen.blit(text_surface, text_rect)

                elif node.encounter_type == "enemy":
                    if node.escpecially_dangerous == False:
                        pygame.draw.circle(screen, (255, 255, 255), (node.node_x, node.node_y), 30) # red, green, blue - x, y - radius
                    else:
                        pygame.draw.circle(screen, (255, 0, 255), (node.node_x, node.node_y), 30) # magenta for especially dangerous enemies
                    font = pygame.font.SysFont(None, 15) # default font, size 15
                    text_surface = font.render(f"{node.encounter_type} {node.layer}, {node.layer_index}", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(node.node_x, node.node_y))
                    screen.blit(text_surface, text_rect)

                elif node.encounter_type == "rest":
                    pygame.draw.circle(screen, (210, 180, 140), (node.node_x, node.node_y), 30)  # Brown for rest
                    font = pygame.font.SysFont(None, 15) # default font, size 15
                    text_surface = font.render(f"{node.encounter_type} {node.layer}, {node.layer_index}", True, (255, 255, 255))
                    text_rect = text_surface.get_rect(center=(node.node_x, node.node_y))
                    screen.blit(text_surface, text_rect)    

               

                else:
                    pygame.draw.circle(screen, (255, 255, 255), (node.node_x, node.node_y), 30) # red, green, blue - x, y - radius
                    font = pygame.font.SysFont(None, 15) # default font, size 15
                    text_surface = font.render(f"{node.encounter_type} {node.layer}, {node.layer_index}", True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(node.node_x, node.node_y))
                    screen.blit(text_surface, text_rect)

                if node is Player.current_node: # if the node and the player's current node are the same
                    pygame.draw.circle(screen, (255, 215, 0), (node.node_x, node.node_y), 35, 3)  # highlighted with yellow
        
    def handle_map_logic(self):
        global game_state
        global Enemy
        global Player
        global dramatic_pause
        global dramatic_pause_timer

        

        

        for layer in layers:
            for node in layer:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    distance = ((event.pos[0] - node.node_x) ** 2 + (event.pos[1] - node.node_y) ** 2) ** 0.5
                    if distance <= 30:  # node radius is 30, at least for now
                        if node in Player.current_node.connections:

                            print(f"Moving to node: {node}")
                            Player.current_node = node
                            if node.encounter_type == "enemy":
                                game.assign_new_enemy()
                                Player.make_hand()
                                game_state = "fight"

                            elif node.encounter_type == "boss":
                                print("I don't have boss yer, sorry")
                                print("I guess you win?")
                            
                            elif node.encounter_type == "rest":
                                game_state = "rest"

                                


                        else:
                            print("You can't move to that node from your current position.")



    def draw_rest(self):
        x=Player.maxHP * 0.2
        x = round(x)


        pygame.draw.rect(screen, (0, 255, 0), (500, 500, 400, 100))  # Big green heal button
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(f"heal for 20% of max HP({x})", True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(700, 540))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (255, 255, 255), (600, 650, 200, 80))  # White continue button
        text_surface = font.render("continue", True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(700, 690))
        screen.blit(text_surface, text_rect)

        pygame.draw.rect(screen, (0, 128, 255), (0, 0, 800, 40))  # blue player info button
        font = pygame.font.SysFont(None, 20)
        text_surface = font.render(f"{Player}", True, (255, 255, 255))  # White text
        screen.blit(text_surface, (10, 10))

        pygame.draw.rect(screen, (255, 255, 255), (550, 800, 300, 50))  # White upgrade button - so far not implemented
        font = pygame.font.SysFont(None, 18)
        text_surface = font.render("Upgrade- PLACEHOLDER, NOT IMPLEMENTED", True, (0, 0, 0))  # black text
        screen.blit(text_surface, (560, 810))


    def handle_rest_logic(self):
        global game_state
        global rest_done # False by default

        if event.type == pygame.MOUSEBUTTONDOWN:
            heal_button_rect = pygame.Rect(500, 500, 400, 100)
            continue_button_rect = pygame.Rect(600, 650, 200, 80)

            if heal_button_rect.collidepoint(event.pos):
                x = Player.maxHP * 0.2
                x = round(x)
                Player.HP += x
                if Player.HP > Player.maxHP:
                    Player.HP = Player.maxHP
                print(f"{Player.name} healed for {x} HP! Current HP: {Player.HP}")

                rest_done = True

            elif continue_button_rect.collidepoint(event.pos):
                if rest_done == False:
                    print("It would be a shame to waste this rest, take another action before continuing the journey.")
                else:
                    print("Continuing the journey...")
                    game_state = "map"
                    rest_done = False

map_generation = node_generation_or_something_idk(layer=0, layer_index=0, encounter_type="start")



layers = map_generation.generate_layers(layer_width=4, layer_depth=8)
layers = map_generation.connect_layers(layers)

Player.current_node = layers[0][0]  # start at the start node

# Assign positions and danger levels to all nodes
for layer in layers:
    for node in layer:
        node.assign_node_positions()
        node.assign_node_danger_level()

print("Generated Encounter Map:")
for layer in layers:
    for node in layer:
        connections = [f"Layer {n.layer} Index {n.layer_index}" for n in node.connections]
        print(f"Node (Layer {node.layer}, Index {node.layer_index}, Type: {node.encounter_type}) -> Connections: {connections}")
    
game = gameloop(Player, Enemy)





Kori = player("Kori", 100, 0, 0, Kori_pool, "Kori pool", 3, 5)
Player = copy.deepcopy(Kori)
Player.current_node = layers[0][0]


Enemy = copy.deepcopy(Joe)
floor1_enemies = [Joe, Construct, Repair_Man, Thug]




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

# Bottom-left force map and rest buttons, 1 pixel apart
force_map = pygame.Rect(1250, 959, 150, 80)
force_rest = pygame.Rect(1250, 1040, 150, 80)

Eror_screen = pygame.Rect(0, 0, 1400, 1120)


Player.make_hand()


def basic_draw_fight():
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
    game.draw_button(screen, force_map, "Force Map")
    game.draw_button(screen, force_rest, "Force Rest")

def draw_error_screen():
    game.draw_button(screen, Eror_screen, "ERROR: Invalid Game State")

hand_start_x = 200
hand_start_y = 500
hand_card_width = 100
hand_card_height = 150 
end_x= 800




enemy_move = Enemy.make_enemy_move()

#------------------------------- Main Pygame Loop -------------------------------

while True:
    screen.fill((0, 0, 0))

    if game_state == "fight":
        basic_draw_fight()

    elif game_state == "choose_new_card":
        game.make_choice_new_card()

    elif game_state == "map":
        map_generation.draw_map()

    elif game_state == "rest":
        map_generation.draw_rest()

    else:
        draw_error_screen()
        
        




    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()

        if game_state == "fight":
            game.handle_basic_logic()
        

        if game_state == "choose_new_card":
            game.handle_choice_new_card()
        
        if game_state == "map":
            map_generation.handle_map_logic()
        
        if game_state == "rest":
            map_generation.handle_rest_logic()





    pygame.display.flip()
    clock.tick(60)
