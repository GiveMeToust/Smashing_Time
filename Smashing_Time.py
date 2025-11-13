import random
from tkinter import font
import copy
import pygame
import sys



pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Pygame Test")

clock = pygame.time.Clock()


hand = []
turn_count =  1
game_state = "fight"

print("hello world")






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
    move("Concentrate", 5, "DEF-up", 1, tags={}),
    move("poison strike", 7, "attack", 1, tags={"poison": 3, "placeholder": 3})
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



floor1_loot = [
    move("Smash", 10, "attack", 1, tags={}),
    move("Block", 4, "defend", 0, tags={}),
    move("Power Up", 5, "STR-up", 1, tags={}),
    move("poison strike", 7, "attack", 1, tags={"poison": 3, "placeholder": 3}),
    move("pray", 5, "defend", 1, tags={"energised":1, }) #I thought about making it heal but that would promote delaying kills, which is not fun
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

    def make_hand(self,):
       return random.sample(self.pool, k=self.drawNum) 
    
    def resolve_move(self, move):
        global turn_count
        


        if self.Energy < 1:
            print("Not enough energy to play this move!")
            return 
        self.Energy -= 1
        
          # Remove the played card from hand

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
        else:
            print("What the fuck kind of move is that? What is happening?! I am going insane! AAARRRGH!!!")
            return
        global tags
        for tag, tag_value in move.tags.items():
            if tag == "enrage":
                x = move.power / 2
                x = round(x)
                print(f"Applying 'enrage' effect! DEF before: {self.DEF}, reducing by {x}")
                self.DEF -= x
            
            elif tag == "poison":
                if "poison" in Enemy.status_effects:
                    Enemy.status_effects["poison"] += tag_value  # Add to existing poison
                    print(f"Poison stacked! Total poison damage: {Enemy.status_effects['poison']}")
                else:
                    Enemy.status_effects["poison"] = tag_value  # Apply new poison
                    print(f"Enemy poisoned! Poison damage: {tag_value}")
            
            elif tag == "heal":
                self.HP += tag_value
                if self.HP > self.maxHP:
                    self.HP = self.maxHP
                print(f"{self.name} healed for {tag_value} HP! Current HP: {self.HP}")

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
        if enemy_move.type == "attack": 
            Player.pending_damage += enemy_move.power + self.STR
        elif enemy_move.type == "defend":
            self.block += enemy_move.power + self.DEF
        elif enemy_move.type == "STR-up":
            self.STR += enemy_move.power
        elif enemy_move.type == "DEF-up":
            self.DEF += enemy_move.power

        print(f"{self.name} used {enemy_move.name}!")

    



Joe=foe("Joe", 50, 0, 0, Joe_pool, "Joe pool")
construct = foe("Construct", 100, 0, 0, Construct_pool, "Construct pool")
Enemy = copy.deepcopy(Joe)
floor1_enemies = [Joe, construct]





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

        Player.take_damage() 

        Enemy.make_enemy_move()
        Player.Energy = Player.MaxEnergy


        hand = Player.make_hand()

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

    
game = gameloop(Player, Enemy)


    




# Define your squares: x, y, width, height
player_square = pygame.Rect(0, 100, 430, 50)
enemy_square = pygame.Rect(650, 100, 330, 50)
player_attack_square = pygame.Rect(0, 200, 430, 50)
enemy_attack_square = pygame.Rect(650, 200, 330, 50)
resolve_square = pygame.Rect(400, 300, 200, 50)
end_turn_square = pygame.Rect(400, 400, 200, 50)
enemy_intent = pygame.Rect(650, 300, 330, 50)
turn_count_square = pygame.Rect(450, 0, 100, 50)
choose_new_card_square = pygame.Rect(400, 700, 100, 50)
enemy_status_square = pygame.Rect(650, 400, 330, 50)



hand = Player.make_hand()


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
