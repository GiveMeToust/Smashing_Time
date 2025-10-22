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

print("hello world 5")







class move:
    def __init__(self, name, power, type, cost):
        self.name = name
        self.power = power
        self.type = type
        self.cost = cost

    def __repr__(self):
        return f"{self.name} (type: {self.type}, power: {self.power}, cost: {self.cost})"


Kori_pool = [
    move("Smash", 10, "attack", 1),
    move("Smash", 10, "attack", 1),
    move("Smash", 10, "attack", 1),
    move("Defend", 10, "defend", 1),
    move("Defend", 10, "defend", 1),
    move("Defend", 10, "defend", 1),
    move("SMASH!", 25, "attack", 2),
    move("Enrage", 5, "STR-up", 1),
    move("Concentrate", 5, "DEF-up", 1)
]


Joe_pool = [
    move("punch", 15, "attack", 999),
    move("punch", 15, "attack", 999),
    move("cower", 20, "defend", 999),
    move("cower", 20, "defend", 999),
    move("Calm breath", 5, "DEF-up", 999)
]

Construct_pool = [
    move("slam", 30, "attack", 999),
    move("fortify", 30, "defend", 999),
    move("construct", 10, "STR-up", 999),
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
       return random.choices(self.pool, k=self.drawNum) 
    
    def resolve_move(self, move):

        if self.Energy < 1:
            print("Not enough energy to play this move!")
            return 
        self.Energy -= 1
        
        hand.remove(card)  # Remove the played card from hand

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
            print("What the fuck kind of move is that? What is happening?! I am going insane!")
            return
        
        if Enemy.HP <= 0:
            Enemy.alive = False
        if Enemy.alive == False:
            print(f"{Enemy.name} has been defeated!")
            game.assign_new_enemy()
            game.end_turn()

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



class enemy(champion):
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

    



Joe=enemy("Joe", 50, 0, 0, Joe_pool, "Joe pool")
construct = enemy("Construct", 100, 0, 0, Construct_pool, "Construct pool")
Enemy = copy.deepcopy(Joe)

floor1 = [Joe, construct]










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


    def draw_hand(self,screen, hand, start_x, start_y, card_width, card_height, spacing):
        for i, card in enumerate(hand):
            card_rect = pygame.Rect(start_x + i * (card_width + spacing), start_y, card_width, card_height)
            pygame.draw.rect(screen, (255, 255, 255), card_rect)  # White card background
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(card.name, True, (0, 0, 0))  # Black text
            text_rect = text_surface.get_rect(center=card_rect.center)
            screen.blit(text_surface, text_rect)


    def assign_new_enemy(self):
        global Enemy
        if Enemy.alive == False:
            print(f"{Enemy.name} has been defeated! A new enemy approaches!")
            Enemy = copy.deepcopy(random.choice(floor1))
            print(f"A wild {Enemy.name} appears!")


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


        hand = Player.make_hand()

        print(f"New hand: {hand}")
        print()

    
game = gameloop(Player, Enemy)


    




# Define your squares: x, y, width, height
player_square = pygame.Rect(0, 100, 430, 50)
enemy_square = pygame.Rect(550, 100, 330, 50)
player_attack_square = pygame.Rect(0, 200, 430, 50)
enemy_attack_square = pygame.Rect(550, 200, 330, 50)
resolve_square = pygame.Rect(300, 300, 200, 50)
end_turn_square = pygame.Rect(300, 400, 200, 50)
enemy_intent = pygame.Rect(550, 300, 330, 50)
turn_count_square = pygame.Rect(450, 0, 100, 50)



hand = Player.make_hand()



hand_start_x = 50
hand_start_y = 450
hand_card_width = 100
hand_card_height = 150 
hand_spacing = 10



enemy_move = Enemy.make_enemy_move()

while True:
    screen.fill((0, 0, 0))
    game.draw_button(screen, player_square, Player.__repr__())
    game.draw_button(screen, enemy_square, Enemy.__repr__())
    game.draw_button(screen, player_attack_square, "Player Attack") 
    game.draw_button(screen, enemy_attack_square, "Enemy Attack")
    game.draw_button(screen, resolve_square, "Resolve Damage")
    game.draw_button(screen, end_turn_square, "End Turn")
    game.draw_hand(screen, hand, hand_start_x, hand_start_y, hand_card_width, hand_card_height, hand_spacing)
    game.draw_button(screen, enemy_intent, f"Enemy Intent: {Enemy.enemy_move.name if hasattr(Enemy, 'enemy_move') else 'None'}")
    game.draw_button(screen, turn_count_square, f"Turn: {turn_count}")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_attack_square.collidepoint(event.pos):
                print()
                print("Player Attack button clicked!")
                Enemy.HP -= 10  # Example action
                print(f"Enemy.HP: {Enemy.HP}")

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
                card_rect = pygame.Rect(hand_start_x + i * (hand_card_width + hand_spacing), hand_start_y, hand_card_width, hand_card_height)
                if card_rect.collidepoint(event.pos):
                    print()
                    print(f"Card {card.name} clicked!")
                    Player.resolve_move(card)
                    print(f"Played {card}. New hand: {hand}")
                    print(f"Enemy pending_damage: {Enemy.pending_damage}, Player block: {Player.block}")
                    break  # Exit loop after playing one card





    pygame.display.flip()
    clock.tick(60)

