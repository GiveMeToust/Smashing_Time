import random
from tkinter import font
import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Pygame Test")

clock = pygame.time.Clock()








class move:
    def __init__(self, name, type, power):
        self.name = name
        self.type = type
        self.power = power

    def __repr__(self):
        return f"{self.name} (type: {self.type}, power: {self.power})"


Kori_pool = [
    move("Smash", 10, "attack"),
    move("Smash", 10, "attack"),
    move("Smash", 10, "attack"),
    move("Defend", 10, "defend"),
    move("Defend", 10, "defend"),
    move("Defend", 10, "defend"),
    move("SMASH!", 20, "attack"),
    move("Enrage", 5, "STR-up"),
    move("Concentrate", 5, "DEF-up")
]


Joe_pool = [
    move("punch", 15, "attack"),
    move("punch", 15, "attack"),
    move("cower", 20, "defend"),
    move("cower", 20, "defend"),
    move("Calm breath", 6, "DEF-up")
]





    



class champion:
    def __init__(self, name, maxHP, STR, DEF, pool, poolname):
        self.name = name
        self.maxHP = maxHP
        self.HP = maxHP
        self.STR = STR
        self.DEF = DEF
        self.alive = True
        self.pending_damage = 0
        self.pending_block = 0
        self.pool = pool
        self.poolname = poolname

    def __repr__(self):
        return f"{self.name} (maxHP: {self.maxHP}, HP: {self.HP}, STR: {self.STR}, DEF: {self.DEF}, pool: {self.poolname})"
    

    def take_damage(self):
        if not self.alive:
            print(f"{self.name} is fucking dead and cannot take more damage!")
            return

        damage_resolved =  self.pending_damage - self.pending_block
        if damage_resolved < 0:
            damage_resolved = 0
        
        if self.pending_block > self.pending_damage:
            self.pending_block = self.pending_damage #So that it would ONLY show how much damage was actually blocked

        self.HP -= damage_resolved
        self.pending_damage = 0
        if self.HP <= 0:
            self.alive = False  
            print(f"{self.name} has been defeated!") 

        print(f"{self.name} has received {damage_resolved} damage! ({self.pending_block} blocked)")

        self.pending_block -= self.pending_damage
        if self.pending_block < 0:
            self.pending_block = 0 







    # def TakeDamage (self):
    #     demage_resolved =  self.pending_damage - self.pending_block
    #     if demage_resolved < 0:
    #         demage_resolved = 0
        
    #     if self.pending_block > self.pending_damage:
    #         self.pending_block = self.pending_damage #So that it would only show how much demage was actually blocked

    #     self.HP -= demage_resolved 
    #     print(f"{self.name} has taken {self.pending_damage} demage! ({self.pending_block} blocked)")
    #     self.pending_damage = 0
    #     self.pending_block = 0

    #     if self.HP <= 0:
    #         self.alive = False
    #         print(f" {self.name} has been defeated!")

    #     if self.HP > self.maxHP:
    #         self.HP = self.maxHP
        
    # def PendMove (self, move):
    #     if move.type == "attack":
    #         if self.name == "player":
    #                  Joe.pending_damage += move.power + self.STR
    #         else:
    #                 player.pending_damage += move.power + self.STR

    #     elif move.type == "defend":
    #         self.pending_block += move.power + self.DEF
        
    #     elif move.type == "STR-up":
    #         self.STR += move.power
        
    #     elif move.type == "DEF-up":
    #         self.DEF += move.power






class player(champion):
    def __init__(self, name, maxHP, STR, DEF, pool, poolname, MaxEnergy, drawNum):
        super().__init__(name, maxHP, STR, DEF, pool, poolname)
        self.MaxEnergy = MaxEnergy
        self.Energy = MaxEnergy
        self.drawNum = drawNum

    def __repr__(self):
        return f"{self.name} (maxHP: {self.maxHP}, HP: {self.HP}, STR: {self.STR}, DEF: {self.DEF}, Energy: {self.Energy}, pool: {self.poolname})"

    def make_hand(self,):
       return random.choices(self.pool, k=self.drawNum) 
    
    def resolve_move(self, smash):


        if move.type == "attack": 
            Enemy.pending_damage += move.power + self.STR
        elif move.type == "defend":
            self.pending_block += move.power + self.DEF
        elif move.type == "STR-up":
            self.STR += move.power
        elif move.type == "DEF-up":
            self.DEF += move.power  
            









Kori = player("Kori", 100, 0, 0, Kori_pool, "Kori pool", 3, 5)
Player = Kori



class enemy(champion):
    def __init__(self, name, maxHP, STR, DEF, pool, poolname):
        super().__init__(name, maxHP, STR, DEF, pool, poolname)  

    def __repr__(self):
        return f"{self.name} (maxHP: {self.maxHP}, HP: {self.HP}, STR: {self.STR}, DEF: {self.DEF}, pool: {self.poolname})"

    def make_enemy_move(self):
        enemy_move = random.choice(self.pool)
        if enemy_move.type == "attack": 
            Player.pending_damage += enemy_move.power + self.STR
        elif enemy_move.type == "defend":
            self.pending_block += enemy_move.power + self.DEF
        elif enemy_move.type == "STR-up":
            self.STR += enemy_move.power
        elif enemy_move.type == "DEF-up":
            self.DEF += enemy_move.power


Joe=enemy("Joe", 50, 0, 0, Joe_pool, "Joe pool")
Enemy = Joe







class gameloop:
    def __init__(self, Player, enemy):
        self.Player = Player
        self.enemy = enemy

    def __repr__(self):
        return f"Game Loop (Player: {self.Player}, Enemy: {self.enemy})"

def draw_button(screen, button_rect, text):     #button function
    pygame.draw.rect(screen, (0, 128, 255), button_rect)  # color: blue
    font = pygame.font.SysFont(None, 18)    #default font, size 18
    text_surface = font.render(text, True, (255, 255, 255)) # text, anti-aliased, white
    screen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))   


def draw_hand(screen, hand, start_x, start_y, card_width, card_height, spacing):
    for i, card in enumerate(hand):
        card_rect = pygame.Rect(start_x + i * (card_width + spacing), start_y, card_width, card_height)
        pygame.draw.rect(screen, (255, 255, 255), card_rect)  # White card background
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(card.name, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=card_rect.center)
        screen.blit(text_surface, text_rect)










# Define your squares: x, y, width, height
player_square = pygame.Rect(0, 100, 430, 50)
enemy_square = pygame.Rect(650, 100, 330, 50)
player_attack_square = pygame.Rect(0, 200, 430, 50)
enemy_attack_square = pygame.Rect(650, 200, 330, 50)
resolve_square = pygame.Rect(300, 300, 200, 50)
draw_square = pygame.Rect(300, 400, 200, 50)


hand = Player.make_hand()



hand_start_x = 50
hand_start_y = 450
hand_card_width = 100
hand_card_height = 150 
hand_spacing = 10




while True:
    screen.fill((0, 0, 0))
    draw_button(screen, player_square, Player.__repr__())
    draw_button(screen, enemy_square, Enemy.__repr__())
    draw_button(screen, player_attack_square, "Player Attack") 
    draw_button(screen, enemy_attack_square, "Enemy Attack")
    draw_button(screen, resolve_square, "Resolve Damage")
    draw_button(screen, draw_square, "Draw")
    draw_hand(screen, hand, hand_start_x, hand_start_y, hand_card_width, hand_card_height, hand_spacing)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player_attack_square.collidepoint(event.pos):
                print()
                print("Player Attack button clicked!")
                Enemy.pending_damage += 10  # Example action
                print(f"Enemy.pending_damage: {Enemy.pending_damage}")

            elif enemy_attack_square.collidepoint(event.pos):
                print()
                print("Enemy Attack button clicked!")
                Player.pending_damage += 10  # Example action
                print(f"Player.pending_damage: {Player.pending_damage}")

            elif resolve_square.collidepoint(event.pos):
                print()
                print("Resolve Damage button clicked!")
                Player.take_damage()
                Enemy.take_damage()

            elif draw_square.collidepoint(event.pos):
                print()
                print("Draw button clicked!")
                hand = Player.make_hand()
                print(f"New hand: {hand}")
            
            for i, card in enumerate(hand):
                card_rect = pygame.Rect(hand_start_x + i * (hand_card_width + hand_spacing), hand_start_y, hand_card_width, hand_card_height)
                if card_rect.collidepoint(event.pos):
                    print()
                    print(f"Card {card.name} clicked!")
                    Player.resolve_move(card)
                    hand.remove(card)  # Remove the played card from hand
                    print(f"Played {card}. New hand: {hand}")
                    print(f"Enemy pending_damage: {Enemy.pending_damage}, Player pending_block: {Player.pending_block}")
                    break  # Exit loop after playing one card





    pygame.display.flip()
    clock.tick(60)

