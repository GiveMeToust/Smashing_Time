import pygame
import random
import copy
import os #for working with file paths
import sys #for quiting the game because python is stupid and for some reason doesn't have a quit function





pygame.init()
print("hello world")


#     Loading assets here:

Images = {}  # Dictionary to hold loaded imagvenv\Scripts\activatees

BASE_DIR = os.path.dirname(__file__)
ART_ASSETS_DIR = os.path.join(BASE_DIR, "Art_Assets")

def Load_Image(file_name): #a function to load images so that I don't always point at their file name but actually have them as a surface  
    full_path = os.path.join(ART_ASSETS_DIR, file_name)
    # Check existence first to provide a clear error and avoid crashing
    if not os.path.exists(full_path):
        print(f"Image not found: {full_path}")
        return None

    try:
        image = pygame.image.load(full_path)  # loads image, returns a Surface
        print(f"Successfully loaded image '{file_name}'")
        Images[file_name] = image  # Store the loaded image in the dictionary "Images" with the file name as the key
    
    except Exception as e:
        # Catch broader exceptions (including FileNotFoundError and pygame errors)
        print(f"Error loading image '{file_name}': {e}")
        return None

List_of_cards = [       # A list of all cards  
    "Defend.jpg",
    "Concentrate.jpeg", # for some reason when I coppied it from my phone it came out as jpg but also jpeg when I did it on my computer, both were from the same source so that's fun I guess
    "Deck_Out.jpg",
    "Enrage.jpg",
    "Fury.jpg",
    "Gamble.jpg",
    "Glare.jpeg",
    "Poison_Bomb.jpg",
    "Poison_Strike.jpg",
    "Pray.jpg",
    "SMASH!.jpg",
    "Smash.jpg",
    "Smite.jpg",
    "Power_Up.jpg",
    "Shrug_off.jpg",
    
]

list_of_map_icons = [
    "Enemy_Icon.png",
    "Enhanced_Enemy_Icon.png",
    "Start_Icon.png",
    "Boss_Icon.png",
    "Shop_Icon.png",
    "Rest_Icon.png",
]

list_of_ATK_and_DEF_icons = [
    "ATK_Icon.png",
    "DEF_Icon.png",
    "STRup_Icon.png",
    "DEFup_Icon.png",
]

List_of_backrounds = [
    "Battle_Background.png",
    "Rest_Backround.png",
    "Shop_Backround.png"
]

List_of_characters = [
    "Joe.png", # This guy is a stock photo that I did NOT pay for and I don't care. Sue me. /s Anyway it's probably from the stock photo company Alamy but it's hard to say for sure because this guy is a bit of a meme and circulating around the internet for at least a decade
    "Kori.png",
    "Repair_Man.png",
    "Extremely_Sucpicious_Barell.png",
    "Thug.png",
    "Construct.png",
]

list_of_paricles = [
    "Heal_Particle.png",
]

the_weird_ones = [ #these cards have different resolutions for some reason, I don't know why
    "Poison_Strike.jpg",
    "Enrage.jpg",
    "Poison_Bomb.jpg",
    "Glare.jpeg",
]


#loading all images:

for image_name in List_of_cards:
    Load_Image(image_name)

for image_name in List_of_characters:
    Load_Image(image_name)

for image_name in List_of_backrounds:
    Load_Image(image_name)

for image_name in list_of_map_icons:
    Load_Image(image_name)

for image_name in list_of_ATK_and_DEF_icons:
    Load_Image(image_name)

for image_name in list_of_paricles:
    Load_Image(image_name)
#transforming images sizes:

def transform_images(image_name, scale_factor):
    x , y = Images[image_name].get_size()
    Images[image_name] = pygame.transform.scale(Images[image_name], (x * scale_factor, y * scale_factor))

for character in List_of_characters: # the construct is a little taller than intended and then it overlaps with the hand and stuff
    if character == "Construct.png": 
        transform_images(character, 0.65)
    else:
        transform_images(character, 0.70)

for card in List_of_cards:
    if card in the_weird_ones: #some of the cards have different resolutions for some reason, so I had to scale them differently, I don't know why this happened since they should all be the same, but I am not getting paid enough to care
        transform_images(card, 0.1924) #compleately eyeballed it, but it looks identical to the other cards. If it's stupid but works, it's not stupid. Also I checked and they get scalled to the same width so it functionally works. 
    else:
        transform_images(card, 0.15)

#This is for when I used a placeholder because my art wasn't done yet.
#scale_for_place_holder = 2560/Images["Place_Holder_Rest_Background.jpg"].get_width() # the place holder background has a different resolution than the battle background, so I had to scale it differently to make it fit the screen, I don't know why this happened since they should all be the same, but I am not getting paid enough to care
#
#for background in List_of_backrounds:
#    if background == "Place_Holder_Rest_Background.jpg": # The place holder has worse resolution (not the same as vscreen) so it will scale badly as the pixels are partially stretched, but since it's a placeholder it's whatever
#        transform_images(background, scale_for_place_holder)
#    else:
#        transform_images(background, 1)

for icon in list_of_map_icons:
    if icon == "Start_Icon.png":
        transform_images(icon, 0.045)
    elif icon == "Boss_Icon.png":
        transform_images(icon, 0.10)
    else:
        transform_images(icon, 0.15)

for icon in list_of_ATK_and_DEF_icons:
    if icon == "DEFup_Icon.png" or icon == "DEF_Icon.png":  #The shields are a little bigger 
        transform_images(icon, 0.40)
    else:
        transform_images(icon, 0.48)

for particle in list_of_paricles:
    transform_images(particle, 0.5)

my_font = pygame.font.SysFont("Verdana", 36)  # 36 px Verdana

VIRTUAL_SIZE = (2560, 1440)
rscreen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  #this is the real screen that gets resized and actually shown (x,y) means starting dimiensions, 0,0 means full screen
vscreen = pygame.Surface(VIRTUAL_SIZE)  # virtual screen that we draw everything to, then scale to rscreen size

def transform_screen(): #scaling screen sizes so they work on any resolution no matter the device
    scaled = pygame.transform.scale(vscreen, rscreen.get_size())
    rscreen.blit(scaled, (0, 0))


vscreen_x, vscreen_y = VIRTUAL_SIZE
rscreen_x, rscreen_y = rscreen.get_size()

scale_x = vscreen_x / rscreen_x #calculated outside the function since I don't need it every frame
scale_y = vscreen_y / rscreen_y

def transform_mouse_pos(): # since I am drawing things on a virtual screen, the position of where objects are drawn and displayed aren't consistent (unless you have 2560px resolution), so I scaled the mouse position to match the virtual screen. Thank Jod you can override event.pos
    if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
        mouse_x, mouse_y = event.pos
        transformed_x = int(mouse_x * scale_x)
        transformed_y = int(mouse_y * scale_y)
        event.pos = (transformed_x, transformed_y)


pygame.display.set_caption("Smashing Time")

clock = pygame.time.Clock()

chance_of_branching = 0.5  # 50% chance to branch sideways in encounter map generation

encounter_types = ["enemy", "shop", "rest",]
weights =          [   90,      5,      5, ]  # might scrap events - Actually I did scrap them them, now is later



dev_mode = False # turns on shitty looking mode
hand = []    # list of all cards/moves/whatever that the player can play
turn_count =  1

game_state = "fight" # can be "fight", "choose_new_card", "shop", "rest", 
#game_states is the most important variable in the game, it controls what state the game is in everything in the main loop is governed by it

# Setting up some variables because python is stupid and not ran by genetically modified hamsters
settings =  False
spent_rest = False #flag for if you have spent time resting
particle_alpha = 255 #used for the heal animation, it controls the transparency of the heal particle, 
particle_y = 0 #used for the heal animation
particle_x = 0 #used for the heal animation
set_up_heal_animation = True #used for the heal animation
heal_animation_playing = False #flag to turn on/off the heal animation because I tried to set up something inteligent but failed

draw_upgrade_potential = False # flag whether you will draw how much a card could be upgraded on the position of the mouse
upgrade_potential = 0 # the value that says how much it could be upgraded
pre_upgrade_potential = 0 # I fricking hate python and that this is the best I could manage to actually do the thing I wanna do

attack="ATK"  #toying with the idea of defining move types as variables instead of strings
defend="DEF"  #"Feeling like programing well, might delete later"
STR_up="STRup"  
DEF_up="DEFup" #I am a dysgrace to programing, that's who I am. Spaghetti code harder than thought possible. This isn't even the most usless part of the code. Be glad I actually removed the two "dramatic_timer" variables that didn't do anything but were called 4 times




settings_grey_out = pygame.Surface((2560, 1440)) # over the whole screen
settings_grey_out.fill((0, 0, 0))  # Black color
settings_grey_out.set_alpha(128)  # Set transparency level (0-255) 0=transparent, 255=opaque

death_red_out = pygame.Surface((2560, 1440)) # over the whole screen
death_red_out.fill((255, 0, 0))  # Red color
death_red_out.set_alpha(20)  # Set transparency level (0-255) 0=transparent, 255=opaque


quit_from_settings = pygame.Rect(1180, 700, 200, 100)  # x, y, width, height
settings_dev_mode_toggle = pygame.Rect(1180, 850, 200, 100)  # x, y, width, height

cost_of_cards = 30 
cost_of_supplies = 20

frame_delay = False # used to prevent you from immidietly closing the defeat screen


class move:
    def __init__(self, name, image_name, power, type, cost, tags):
        self.name = name
        self.image_name = image_name
        self.power = power
        self.type = type
        self.cost = cost
        self.tags = tags
    
    def upgrade(self):
        if self.type == "ATK" or self.type == "DEF":
            upgrade_amount = 4 + self.power*0.2
            upgrade_amount = round(upgrade_amount)
        elif self.type == "STRup" or self.type == "DEFup":
            upgrade_amount = 1 + self.power*0.2
            upgrade_amount = round(upgrade_amount)
        elif self.type == "spell":
            upgrade_amount = 0 #spells only cary tags and don't do anything, so upgrading their power is pointless
    
        print(f"Upgrading {self.name} from {self.power} to {self.power + upgrade_amount} power!")
        self.power += upgrade_amount


    def __repr__(self):
        return f"{self.name} (type: {self.type}, power: {self.power}, cost: {self.cost}, tags: {self.tags}, image: {self.image_name})"

Kori_pool = [
    move("Smash", "Smash.jpg", 10, "ATK", 1, tags={}),
    move("Smash", "Smash.jpg", 10, "ATK", 1, tags={}),
    move("Smash", "Smash.jpg", 10, "ATK", 1, tags={}),
    move("Defend", "Defend.jpg", 10, "DEF", 1, tags={}),
    move("Defend", "Defend.jpg", 10, "DEF", 1, tags={}),
    move("Defend", "Defend.jpg", 10, "DEF", 1, tags={}),
    move("SMASH!", "SMASH!.jpg", 25, "ATK", 2, tags={}),
    move("Enrage", "Enrage.jpg", 5, "STRup", 1, tags={"enrage": None}),
    move("Gamble", "Gamble.jpg", 0, "spell", 1, tags={"redraw": True}),
    move("Deck Out", "Deck_Out.jpg", 7, "DEF", 1, tags={"draw": 2}),
    move("Poison Strike", "Poison_Strike.jpg", 7, "ATK", 1, tags={"poison": 3}),
    move("Fury" , "Fury.jpg", 6 , "ATK", 1, tags={"multihit": 2}),
]


Joe_pool = [
    move("punch", "", 15, "ATK", 999,  tags={}),
    move("punch", "", 15, "ATK", 999,  tags={}),
    move("cower", "", 20, "DEF", 999,  tags={}),
    move("cower", "", 20, "DEF", 999,  tags={}),
    move("Calm breath", "", 5, "DEFup", 999,  tags={})
]

Construct_pool = [
    move("slam", "", 30, "ATK", 999,  tags={}),
    move("fortify", "", 30, "DEF", 999,  tags={}),
    move("construct", "", 10, "STRup", 999,  tags={})
]

Thug_pool = [
    move("Poison Strike", "", 10, "ATK", 999, tags={"poison": 3}),
    move("Smoke Screen", "", 10, "DEF", 999, tags={"blind": 1}),
    move("Slash", "", 5, "ATK", 999, tags={"multihit": 4}),
]

Repair_Man_pool = [
    move("weld", "", 20, "ATK", 999, tags={}),
    move("empty magazine", "", 3, "ATK", 999, tags={"multihit": 6}),
    move("brace", "", 20, "DEF", 999, tags={}),
    move("patch up", "", 20, "DEF", 999, tags={"heal": 15}),
    move("overclock", "", 10, "STRup", 999, tags={}),
]

Extremely_Sucpicious_Barell_pool = [
    move("do nothing", "", 40, "DEF", 999, tags={}),
    move("do nothing", "", 40, "DEF", 999, tags={}),
    move("sucpicious sounds", "", 20, "ATK", 999, tags={}),
]

explode_move = move("explode", "", 9999, "ATK", 0, tags={}) #that's a suprise tool that will help us later
                                                                #I think I forgot to actually use this suprise tool, I think I meant to have the barrel use it when it explodes
floor1_loot = [
    move("Smash", "Smash.jpg", 10, "ATK", 1, tags={}), #
  #  move("Block", "Block.jpg", 4, "DEF", 0, tags={}), # ---------------------------------- missing texture, messes up the code without it
    move("Power Up", "Power_Up.jpg", 5, "STRup", 1, tags={}), #
    move("Poison Strike", "Poison_Strike.jpg", 7, "ATK", 1, tags={"poison": 3}), ##damages enemy at the end of turn, then loses 1 poison
    move("Poison Bomb", "Poison_Bomb.jpg", 2, "ATK", 2, tags={"poison": 5}), #
    move("Concentrate", "Concentrate.jpeg", 5, "DEFup", 1, tags={}), #
    move("Shrug off", "Shrug_off.jpg", 20, "DEF", 1, tags={}),
    move("Deck Out", "Deck_Out.jpg", 7, "DEF", 0, tags={"draw": 2}), ##draw 2 cards 
    move("Gamble", "Gamble.jpg", 0, "spell", 0, tags={"redraw": True}), ##you draw a new hand, can only be used once per turn so you can't spam zero cost moves
    move("Smite" , "Smite.jpg", 10, "ATK", 1, tags={"blind": 2}), ##makes enemy attacks do 75% damage
    move("Fury" , "Fury.jpg", 6 , "ATK", 1, tags={"multihit": 2}), ##attack twice
    move("Glare", "Glare.jpeg", 5, "ATK", 0, tags={"blind": 1}), #enemy attacks do 75% damage for x turns
    move("Pray", "Pray.jpg", 5, "DEF", 1, tags={"energised":1, }), #I thought about making it heal but that would promote delaying kills, which is not fun, now it gives you +1 energy next turn
]



class champion:
    def __init__(self, name, maxHP, STR, DEF, pool, poolname, status_effects, image_name):
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
        self.status_effects = status_effects 
        self.image_name = image_name

    def __repr__(self):
        return f"{self.name} (maxHP: {self.maxHP}, HP: {self.HP}, STR: {self.STR}, DEF: {self.DEF}, pool: {self.poolname})"
    



class player(champion):
    def __init__(self, name, maxHP, STR, DEF, pool, poolname, status_effects, image_name, MaxEnergy, drawNum,):
        super().__init__(name, maxHP, STR, DEF, pool, poolname, status_effects, image_name)
        self.MaxEnergy = MaxEnergy
        self.Energy = MaxEnergy
        self.drawNum = drawNum
        self.current_node = None # player's current position on the map, current_node = layers[0][0] is not yet defined so I have to set it up later because coding is stupid and not a real person like it should be. Fucking moron. All my code should be run by genetically modified hamsters with PhDs in computer science, not by this piece of shit garbage that can't even remember to set a variable properly
        self.money = 0
        

    def __repr__(self):
        return f"{self.name} (HP: {self.HP}/{self.maxHP}, STR: {self.STR}, DEF: {self.DEF}, Energy: {self.Energy}, P.DMG: {self.pending_damage}, Block: {self.block}, pool: {self.poolname}, $: {self.money})"

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

            if move.type == "ATK":
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
                

            elif move.type == "DEF":
                self.block += move.power + self.DEF
            elif move.type == "STRup":
                self.STR += move.power
            elif move.type == "DEFup":
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

        damage_resolved = (self.pending_damage) - (self.block + self.DEF)
        if damage_resolved < 0:
            damage_resolved = 0

        self.HP = self.HP - damage_resolved

        x = (f"{self.name} took {damage_resolved} damage ({self.block} block")
        self.block = self.block - (self.pending_damage)
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
            

    def draw_defeat_screen(self): # tints the screen red and displays "GAME OVER"
        vscreen.blit(death_red_out, (0, 0))  # Reded out background
        vscreen.blit(settings_grey_out, (0, 0)) # further darkened background, reused from settings because I am a lazy bastard
        pygame.draw.rect(vscreen, (200, 0, 0), quit_from_settings)  # Red quit button

        my_fontfont = pygame.font.SysFont(None, 46) # system font cause I think that's neat for the death screen
        text_surface = my_fontfont.render("GAME OVER", True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=(vscreen.get_width() // 2, vscreen.get_height() // 2 - 100))

        my_font = pygame.font.SysFont("Verdana", 36)  # 36 px Verdana
        text_rect = text_surface.get_rect(center=quit_from_settings.center)

        vscreen.blit(text_surface, text_rect)
        

    def handle_defeat_screen_click(self):
        global frame_delay

        if frame_delay == True: # this happens on the same frame as you hit the end turn button, so you would immidietly also quit from the game. I added this one frame delay to prevent this
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Quitting game from defeat screen...")
                pygame.quit() #Just closes the window, technically not required
                sys.exit() #kill the program. EXTERMINATE. EXTERMINATE. EXTERMINATE.
                
        frame_delay = True    

Kori = player("Kori", 100, 0, 0, Kori_pool, "Kori pool", {}, "Kori.png", 3, 5)
Player = copy.deepcopy(Kori)







class foe(champion):
    def __init__(self, name, maxHP, STR, DEF, pool, poolname, status_effects, image_name):
        super().__init__(name, maxHP, STR, DEF, pool, poolname, status_effects, image_name)  
        self.pending_block = 0


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
            if enemy_move.type == "ATK": 
                if "blind" in Player.status_effects:
                    x = (enemy_move.power + self.STR)*0.75
                    x = round(x)
                    Player.pending_damage += x
                else:
                    Player.pending_damage += enemy_move.power + self.STR
            elif enemy_move.type == "DEF":
                self.pending_block += enemy_move.power + self.DEF
            elif enemy_move.type == "STRup":
                self.STR += enemy_move.power
            elif enemy_move.type == "DEFup":
                self.DEF += enemy_move.power
            elif enemy_move.type == "spell": #all these moves are handled by tags
                pass

            for tag, tag_value in enemy_move.tags.items():
                if tag == "poison":
                    if "poison" in Player.status_effects:
                        Player.status_effects["poison"] += tag_value
                    else:
                        Player.status_effects["poison"] = tag_value
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

    def get_block(self):
        self.block = self.pending_block
    



Joe=foe("Joe", 50 + random.randint(-5, 5) , 0, 0, Joe_pool, "Joe pool", {}, "Joe.png")
Construct = foe("Construct", 100, 0, 0, Construct_pool, "Construct pool", {}, "Construct.png")
Thug = foe("Thug", 80 + random.randint(-5, 5), 5 + random.randint(-1, 1), 0, Thug_pool, "Thug pool", {}, "Thug.png")
Repair_Man = foe("Repair Man", 200, 0, 0, Repair_Man_pool, "Repair Man pool", {}, "Repair_Man.png")
Extremely_Sucpicious_Barell = foe("Extremely Sucpicious Barell", 80 + random.randint(-5, 5), 0, 0, Extremely_Sucpicious_Barell_pool, "Extremely Sucpicious Barell pool",  {"explosive": 5}, "Extremely_Sucpicious_Barell.png") #explodes after x turns, gains 2*x block every turn
Enemy = copy.deepcopy(Joe)

floor1_enemies = [Joe, Construct, Thug, Extremely_Sucpicious_Barell]
boss_enemies = [Repair_Man]
















class gameloop:
    def __init__(self, Player, enemy):
        self.Player = Player
        self.enemy = enemy

    def __repr__(self):
        return f"Game Loop (Player: {self.Player}, Enemy: {self.enemy})"

    def draw_button(self, vscreen, button_rect, text):     #button function
        pygame.draw.rect(vscreen, (0, 128, 255), button_rect)  # color: blue
        font = pygame.font.SysFont(None, 18)    #default font, size 18
        text_surface = font.render(text, True, (255, 255, 255)) # text, anti-aliased, white
        vscreen.blit(text_surface, (button_rect.x + 10, button_rect.y + 10))


    def dev_draw_hand(self,vscreen, hand, start_x, start_y, end_x,  card_width, card_height):

        L = end_x - start_x
        
        spacing = (L - len(hand)*card_width) / (len(hand) + 1)

        for i, card in enumerate(hand):
            card_rect = pygame.Rect(start_x + i * (card_width + spacing), start_y, card_width, card_height)
            pygame.draw.rect(vscreen, (255, 255, 255), card_rect)  # White card background
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(card.name, True, (0, 0, 0))  # Black text
            text_rect = text_surface.get_rect(center=card_rect.center)
            vscreen.blit(text_surface, text_rect) # Draw card name centered on the card


    def assign_new_enemy(self):
        global Enemy
        global is_boss_fight
        if Player.current_node.encounter_type == "boss":
            is_boss_fight = True
            Enemy = copy.deepcopy(random.choice(boss_enemies))
            print(f"The boss {Enemy.name} appears!")
            Enemy.make_enemy_move()  
        else:
            Enemy = copy.deepcopy(random.choice(floor1_enemies))
            self.adjust_enemy_difficulty()
            print(f"A wild {Enemy.name} appears!")
            Enemy.make_enemy_move()
    
    def adjust_enemy_difficulty(self): #makes the enemy stronger the further you go down
        global Enemy

        Enemy.maxHP = round(Enemy.maxHP*(1 + (Player.current_node.danger_level * 0.05)))
        Enemy.HP = Enemy.maxHP
        for move in Enemy.pool:
            move.power = round(move.power*(1 + (Player.current_node.danger_level * 0.06))) # Honnestly, I am really not sure about the balance of this 



        print(f"Adjusted {Enemy.name}'s stats for danger level {Player.current_node.danger_level}!")
        

    def kill_enemy(self):
        global turn_count
        global Enemy
        global Player
        global is_boss_fight

        if Enemy.HP <= 0:
            Enemy.alive = False
            print(f"{Enemy.name} has been defeated! A new enemy approaches!")
            game.start_new_card_selection()
            game.end_turn()
            turn_count = 0

            money_earned = random.randint(1, 10) + (Player.current_node.danger_level * 2)
            Player.money += money_earned
            print(f"{Player.name} earned {money_earned} money! Total money: {Player.money}")

            if is_boss_fight:
                print("Boss defeated! You (kinda) win the game! Get ready for round 2, I guess. God this game is so bad.")
                prepare_map() #restart the map for now
                is_boss_fight = False
                Player.money += 50 #big money reward for beating the boss
        


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

                

        if "energised" in Player.status_effects:
            Player.Energy += Player.status_effects["energised"]
            print(f"{Player.name} is energised and gains {Player.status_effects['energised']} extra energy this turn!")
            del Player.status_effects["energised"]

        if "explosive" in Enemy.status_effects:
            Enemy.status_effects["explosive"] -= 1
            Enemy.block += Enemy.status_effects["explosive"] * 2
            print(f"{Enemy.name} gains {Enemy.status_effects['explosive'] * 2} block from being explosive!")
            if Enemy.status_effects["explosive"] <= 0:
                print(f"{Enemy.name} explodes!")
                Enemy.HP = 0
                game.kill_enemy()
                del Enemy.status_effects["explosive"]




    def dev_handle_basic_logic(self):
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
                game_states.prepare_map()

            elif force_rest.collidepoint(event.pos):
                print()
                print("Force Rest button clicked!")
                game_state = "rest"

            elif exit_button.collidepoint(event.pos):
                print()
                print("Exit button clicked!")
                pygame.quit() #Just closes the window, technically not required
                sys.exit() #kill the program. EXTERMINATE. EXTERMINATE. EXTERMINATE.
                
            
            elif gimme_money.collidepoint(event.pos):
                print()
                print("Gimme Money button clicked!")
                Player.money += 10
                print(f"Player money: {Player.money}")

            elif force_shop.collidepoint(event.pos):
                print()
                print("Force Shop button clicked!")
                game_states.prepare_shop()

            elif force_new_card.collidepoint(event.pos):
                print()
                print("Force New Card button clicked!")
                game.start_new_card_selection()
                
            
            for i, card in enumerate(hand):
                # Calculate spacing exactly like dev_draw_hand so the clickable rect matches drawn position
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

        Player.Energy = Player.MaxEnergy

        game.apply_status_effects()

        Player.take_damage() 

        Enemy.get_block() #from pending block into real block

        Enemy.make_enemy_move()

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



        
        


    def handle_choice_new_card(self):
        global game_state
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(current_choices)):
                choice_rect = pygame.Rect(200 + i * 200, 300, 150, 50)
                if choice_rect.collidepoint(event.pos):
                    chosen_card = current_choices[i]
                    Player.pool.append(chosen_card)
                    print(f"You chose {chosen_card.name} to add to your pool!")
                    game_states.prepare_map()
                    return

    def draw_settings(self):
        vscreen.blit(settings_grey_out, (0, 0))  # Greyed out background
        pygame.draw.rect(vscreen, (200, 0, 0), quit_from_settings)  # Red quit button

        font = pygame.font.SysFont(None, 33)
        text_surface = font.render("Quit game", True, (255, 255, 255))
        vscreen.blit(text_surface, (1190, 720))  # Centered text on the button

        pygame.draw.rect(vscreen, (200, 200, 200), settings_dev_mode_toggle)  # Grey toggle button
        text_surface = font.render("Dev Mode: " + str(dev_mode), True, (0, 0, 0))
        vscreen.blit(text_surface, (1190, 890))  # Centered text on the toggle button


    def handle_settings(self):
        global dev_mode
        global game_state
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_from_settings.collidepoint(event.pos):
                print("Quitting game from settings...")
                pygame.quit() #Just closes the window, technically not required
                sys.exit() #kill the program. EXTERMINATE! EXTERMINATE! EXTERMINATE!
                
                
            elif settings_dev_mode_toggle.collidepoint(event.pos):
                dev_mode = not dev_mode

                print(f"Dev Mode toggled to {dev_mode}!")
                


    
    def go_to_settings(self):
        global settings
        if event.type == pygame.KEYDOWN:
            if settings == False:
                if event.key == pygame.K_ESCAPE:
                    settings = True
            else:
                if event.key == pygame.K_ESCAPE:
                    settings = False


    def start_game(self):
        None
    

#--------------------------- Generate Map and stuff (mostly drawing different states) ----------------------------------------------------------------


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
                self.danger_level = self.danger_level*1.2 + 2
                self.escpecially_dangerous = True


    def __repr__(self):
        return f"{self.encounter_type} {self.layer}, {self.layer_index}"
    

    def prepare_map(self): # So this is pretty much useless
        global game_state
        game_state = "map"

    
    def draw_map(self):
        # Compute centered layout and larger node sizes

        num_layers = len(layers)
        center_x = vscreen.get_width() // 2
        center_y = vscreen.get_height() // 2

        # Map area: use 75% of width to give margins
        map_width = int(vscreen.get_width() * 0.75)
        layer_spacing_y = 160
        map_height = (num_layers - 1) * layer_spacing_y if num_layers > 1 else 0

        start_x = center_x - map_width // 2
        start_y = center_y - map_height // 2 - 40

        # Assign positions for each node in a layer (evenly spaced horizontally)
        for layer_idx, layer in enumerate(layers):
            n = len(layer)
            if n == 0:
                continue
            spacing_x = map_width / (n + 1)
            for i, node in enumerate(layer):
                node.node_x = int(start_x + (i + 1) * spacing_x)
                node.node_y = int(start_y + layer_idx * layer_spacing_y)

        # Draw connections (behind nodes)
        for layer in layers:
            for node in layer:
                for target in node.connections:
                    pygame.draw.line(vscreen, (255, 255, 255), (node.node_x, node.node_y), (target.node_x, target.node_y), 4)

        # Draw nodes 
        node_radius = 40
        for layer in layers:
            for node in layer:
                x, y = node.node_x, node.node_y
                if node.encounter_type == "start":
                    icon = Images["Start_Icon.png"]

                elif node.encounter_type == "boss":
                    icon = Images["Boss_Icon.png"]

                elif node.encounter_type == "enemy":
                    if node.escpecially_dangerous:
                        icon = Images["Enhanced_Enemy_Icon.png"]
                    else:
                        icon = Images["Enemy_Icon.png"]

                elif node.encounter_type == "rest":
                    icon = Images["Rest_Icon.png"]

                elif node.encounter_type == "shop":
                    icon = Images["Shop_Icon.png"]

                #difference_from_origin_point_to_center_of_icon:
                #origin_point_to_center = (2*node_radius*node_radius)**0.5 #since the node is a cricle but drawn from the corner, I had to do some pythagorean theorem to figure out how much I need to shift the icon
                #Yeah, so that didn't fucking work. I am leaving it here as a monument to my own overthinkingness


                pygame.draw.circle(vscreen, (50, 158, 255), (x, y), node_radius)
                vscreen.blit(icon, (x - icon.get_width() // 2, y - icon.get_height() // 2))  # Center the icon on the node

                #font = pygame.font.SysFont(None, 16)
                #label = node.encounter_type if node.encounter_type in ("start", "boss") else f"{node.encounter_type} {node.layer}, {node.layer_index}"
                #text_surface = font.render(label, True, text_color)
                #text_rect = text_surface.get_rect(center=(x, y))
                #vscreen.blit(text_surface, text_rect)

                if node is Player.current_node:
                    pygame.draw.circle(vscreen, (255, 215, 0), (x, y), node_radius + 6, 4)

    def draw_hand(self,vscreen, hand, start_x, start_y, end_x): # reused from dev_draw_hand, that's why there is card_width even though I don't set it.
        card_width = 230 #I checked and that is the width of the images once transformed, and since I don't plan to ever change how big the cards will be it's okay to just set it here instead of passing it as a parameter like dev_draw_hand

        L = end_x - start_x # total length
        
        spacing = (L - len(hand)*card_width) / (len(hand) + 1) # adaptive spacing based on number of cards

        for i, card in enumerate(hand):
            my_font = pygame.font.SysFont("Verdana", 36)  # 36 px Verdana

            vscreen.blit(Images[card.image_name],(start_x + i * (card_width + spacing), start_y))  # Draw card image at calculated position

            move_name_surface = my_font.render(card.name, True, (255, 255, 255))  # White text
            vscreen.blit(move_name_surface, (4 + start_x + i * (card_width + spacing), start_y - 41))  # Draw move name below the card


            my_font = pygame.font.SysFont("Verdana", 38)  # setting it slightly bigger for the outline, only works on single characters because math or something, idk I guess you could do it if you individually rendered each character, but it's not like It's all that important for anything aside from the stuff drawn on the moves themselves
            #Actually, I think it's still offset because pygame renders stuff from the top left corner and not the center, but it still gives it a "shade" if the "outline" isn't too much bigger

            move_cost_surface_outline = my_font.render(f"{card.cost}", True, (0, 0, 0))  # black outline
            vscreen.blit(move_cost_surface_outline, (206 + start_x + i * (card_width + spacing), start_y - 8))  

            my_font = pygame.font.SysFont("Verdana", 36)  # setting back to normal

            move_cost_surface = my_font.render(f"{card.cost}", True, (245, 215, 125))  # tan-yellow text
            vscreen.blit(move_cost_surface, (206 + start_x + i * (card_width + spacing), start_y - 8))  # Draw move cost below the move name

            move_stats_surface = my_font.render(f"{card.type}-{card.power}", True, (255, 255, 255))  # White text
            vscreen.blit(move_stats_surface, (4 + start_x + i * (card_width + spacing), start_y + 303))  # Draw move type and power bellow cards
            
            if card.tags:
                if "multihit" in card.tags:
                    move_tags_surface = my_font.render(f"Multihit: {card.tags['multihit']}", True, (255, 255, 255))  # White text
                    vscreen.blit(move_tags_surface, (4 + start_x + i * (card_width + spacing), start_y + 343))  # Draw move tags below type and power
                
                elif "poison" in card.tags:
                    move_tags_surface = my_font.render(f"Poison: {card.tags['poison']}", True, (255, 255, 255))  # White text
                    vscreen.blit(move_tags_surface, (4 + start_x + i * (card_width + spacing), start_y + 343))  # Draw move tags below type and power

                elif "draw" in card.tags:
                    move_tags_surface = my_font.render(f"Draw: {card.tags['draw']}", True, (255, 255, 255))  # White text
                    vscreen.blit(move_tags_surface, (4 + start_x + i * (card_width + spacing), start_y + 343))  # Draw move tags below type and power
                
                elif "redraw" in card.tags:
                    move_tags_surface = my_font.render(f"Redraw", True, (255, 255, 255))  # White text
                    vscreen.blit(move_tags_surface, (4 + start_x + i * (card_width + spacing), start_y + 343))  # Draw move tags below type and power
               
                elif "energise" in card.tags:
                    move_tags_surface = my_font.render(f"Energise: {card.tags['energise']}", True, (255, 255, 255))  # White text
                    vscreen.blit(move_tags_surface, (4 + start_x + i * (card_width + spacing), start_y + 343))  # Draw move tags below type and power

                elif "enrage" in card.tags:
                    move_tags_surface = my_font.render(f"Enrage", True, (255, 255, 255))  # White text
                    vscreen.blit(move_tags_surface, (4 + start_x + i * (card_width + spacing), start_y + 343))  # Draw move tags below type and power
                
                
            


    def draw_fight(self): 
        # This is where I will actually draw the fight with images and stuff
        my_font = pygame.font.SysFont("Verdana", 30)

        vscreen.blit(Images["Battle_Background.png"], (0, 0))  # Draw fight background

        vscreen.blit(Images[Player.image_name], (200, 400))  # Draw player image

        vscreen.blit(Images[Enemy.image_name], (2000, 400))  # Draw enemy image


        my_font = pygame.font.SysFont("Verdana", 25)
        Enemy_status_surface = my_font.render(f"{Enemy.name}) HP:{Enemy.HP}/{Enemy.maxHP} STR:{Enemy.STR} DEF:{Enemy.DEF} Block:{Enemy.block}", True, (255, 255, 255))  # White text
        my_font = pygame.font.SysFont("Verdana", 23)
        Enemy_status_effects_surface = my_font.render(f"Effects: {Enemy.status_effects}", True, (0, 0, 0))  # Black text

        Enemy_center_x = (Images[Enemy.image_name].get_width() / 2)
        Enemy_status_center_x = Enemy_status_surface.get_width() / 2

        Status_backround = pygame.Rect(2000 + Enemy_center_x - Enemy_status_center_x, 320, Enemy_status_surface.get_width(), 70)  # x, y, width, height
        pygame.draw.rect(vscreen, (128, 128, 128), Status_backround) #backround for enemy status

        vscreen.blit(Enemy_status_surface, (2000 + Enemy_center_x - Enemy_status_center_x, 320))  # Draw enemy status  -  I genuenly stared at the wall for like 3 minutes trying to figure out how to make it so both of their centers are on the same x coordinate
        vscreen.blit(Enemy_status_effects_surface, (2000 + Enemy_center_x - Enemy_status_center_x, 355))  # Draw enemy status effects  -  Status effects are not actually centered, but they begin at the same x as status so I think it's okay

        my_font = pygame.font.SysFont("Verdana", 33)
        Enemy_move_surface = my_font.render(f"Enemy Move: {Enemy.enemy_move.name}, {Enemy.enemy_move.type}-{Enemy.enemy_move.power}", True, (255, 255, 255))  # White text
        my_font = pygame.font.SysFont("Verdana", 30)
        Enemy_move_Effects_surface = my_font.render(f"Effects: {Enemy.enemy_move.tags}", True, (0, 0, 0))  # Black text
        
        move_offset = Images[Enemy.image_name].get_height() + 20
        Enemy_move_center_x = Enemy_move_surface.get_width() / 2

        move_backround = pygame.Rect(2000 + Enemy_center_x - Enemy_move_center_x, 400 + move_offset, Enemy_move_surface.get_width(), 75)  # x, y, width, height
        pygame.draw.rect(vscreen, (130, 130, 200), move_backround) #blue backround for enemy move

        vscreen.blit(Enemy_move_surface, (2000 + Enemy_center_x - Enemy_move_center_x, 400 + move_offset))  # Draw enemy move
        vscreen.blit(Enemy_move_Effects_surface, (2000 + Enemy_center_x - Enemy_move_center_x, 435 + move_offset))  # Draw enemy move effects

        Player_status_box = pygame.Rect(1, 1400, 2560, 50)  # x, y, width, height
        pygame.draw.rect(vscreen, (128, 128, 128), Player_status_box)  #backround for player status

        my_font = pygame.font.SysFont("Verdana", 30)
        Player_status_surface = my_font.render(f"{Player.name}) HP:{Player.HP}/{Player.maxHP} STR:{Player.STR} DEF:{Player.DEF} Block:{Player.block} Pending Damage:{Player.pending_damage} Energy:{Player.Energy}/{Player.MaxEnergy} Effects:{Player.status_effects}", True, (255, 255, 255))  # White text
        vscreen.blit(Player_status_surface, (10, 1403))  # Draw player status

        pygame.draw.circle(vscreen, (0, 0, 0), (1280, 1311), 54) # border for energy count circle

        pygame.draw.circle(vscreen, (130, 130, 200), (1280, 1311), 50)  # energy count circle

        my_font = pygame.font.SysFont("Verdana", 70) #  draw a count of you energy
        energy_count = my_font.render(f"{Player.Energy}", True, (0, 0, 255)) 
        x=energy_count.get_width()/2    # Hell yeah, baby, now this is what I call programming, even though it's really just centering a surface, but I did it all by myself
        y=energy_count.get_height()/2   # okay, technically I guess calculating it every frame is a little inefficient but whatever

        my_font = pygame.font.SysFont("Verdana", 72) # shading for energy count
        energy_count_shade = my_font.render(f"{Player.Energy}", True, (0, 0, 5))

        vscreen.blit(energy_count_shade, (1280-x, 1309-y)) # Draws a shade to make it pop a little, plus it looks a little better
        vscreen.blit(energy_count, (1280-x, 1309-y))  # Draw Player.energy, made it a little higher since it looked a little off even though it isn't centered
        
        my_font = pygame.font.SysFont("Verdana", 30) # draw a count of your money
        money_count = my_font.render(f"{Player.money}$", True, (255,255,0))
        vscreen.blit(money_count, (10, 10)) # Draw Player.money in the top left corner, and this time the fact pygame renders from the left corner actually helps since it as the width grows it just goes more to the right where it's supposed to go

        pygame.draw.circle(vscreen, (0, 0, 0), (2250, 1230), 104) # ouline for end turn button
        pygame.draw.circle(vscreen, (200, 210, 0), (2250, 1230), 100) # end turn button

        my_font = pygame.font.SysFont("Verdana", 35)
        end_turn_label = my_font.render("END TURN", True, (0, 0, 0))
        vscreen.blit(end_turn_label, (2250 - end_turn_label.get_width() / 2, 1230 - end_turn_label.get_height() / 2)) # Draw end turn button, centered on the circle

        
        my_font = pygame.font.SysFont("Verdana", 50)  #displaying the raw strenght of the enemy move since that's pretty much the only thing the player needs to care about
        if "ATK" == Enemy.enemy_move.type:
            Enemy_move_strenght = Enemy.enemy_move.power + Enemy.DEF
            Enemy_move_strenght = str(Enemy_move_strenght) # converting to a string because pythone is stupid and won't convert it automattically when it needs to render it. Like I said before, code should be executed by genetically modified hamsters
            
            Enemy_strenght_label = my_font.render(Enemy_move_strenght, True, (255, 0, 0))  # Red text

            if "multihit" in Enemy.enemy_move.tags:
                Enemy_strenght_label = my_font.render(f"{Enemy_move_strenght} x{Enemy.enemy_move.tags['multihit']}", True, (255, 0, 0))  # Red text with multihit multiplier

            vscreen.blit(Enemy_strenght_label, (1810 , 710)) 
            vscreen.blit(Images["ATK_Icon.png"], (1810 + Enemy_strenght_label.get_width(), 712)) 

        elif "DEF" == Enemy.enemy_move.type:
            Enemy_move_strenght = Enemy.enemy_move.power + Enemy.STR
            Enemy_move_strenght = str(Enemy_move_strenght)

            Enemy_strenght_label = my_font.render(Enemy_move_strenght, True, (255, 0, 0))  # Red text

            vscreen.blit(Enemy_strenght_label, (1810 , 710)) 
            vscreen.blit(Images["DEF_Icon.png"], (1810 + Enemy_strenght_label.get_width(), 712)) 

        elif "STRup" == Enemy.enemy_move.type:
            Enemy_move_strenght = Enemy.enemy_move.power
            Enemy_move_strenght = str(Enemy_move_strenght)

            Enemy_strenght_label = my_font.render(Enemy_move_strenght, True, (255, 0, 0))  # Red text

            vscreen.blit(Enemy_strenght_label, (1810 , 710)) 
            vscreen.blit(Images["STRup_Icon.png"], (1810 + Enemy_strenght_label.get_width(), 712)) 

        elif "DEFup" == Enemy.enemy_move.type:
            Enemy_move_strenght = Enemy.enemy_move.power
            Enemy_move_strenght = str(Enemy_move_strenght)

            Enemy_strenght_label = my_font.render(Enemy_move_strenght, True, (255, 0, 0))  # Red text

            vscreen.blit(Enemy_strenght_label, (1810 , 710)) 
            vscreen.blit(Images["DEFup_Icon.png"], (1810 + Enemy_strenght_label.get_width(), 712))  

        player_block_label = my_font.render(f"{Player.block}", True, (0, 0, 250))  # Blue text for player block
        vscreen.blit(player_block_label, (200 + Images[Player.image_name].get_width() + 20, 710)) 

        my_font = pygame.font.SysFont("Verdana", 30)

        player_hp_label = my_font.render(f"{Player.HP}/{Player.maxHP}", True, (250, 0, 0))  # Green text for player HP
        vscreen.blit(player_hp_label, (200 + Images[Player.image_name].get_width()/2 - player_hp_label.get_width()/2, 370))

      



        game_states.draw_hand(vscreen, hand, 400, 900, 2160)  # Draw player's hand - start x, start y, width, height - vscreen resolustion: (2560x1440)




    def handle_fight_logic(self): # vscreen.blit(Images[card.image_name],(start_x + i * (card_width + spacing), start_y)) 
                                # game_states.draw_hand(vscreen, hand, 400, 900, 2160, 100)
                              # draw_hand(self,vscreen, hand, start_x, start_y, end_x,  card_width)
        start_x = 400
        end_x = 2160
        card_width = 230

        L = end_x - start_x # total length
    
        spacing = (L - len(hand)*card_width) / (len(hand) + 1) # adaptive spacing based on number of cards
                            
        for i, card in enumerate(hand): #Completaly forgot how this worked in dev_fight, so in case I forget again, the card variable coresponds to the move in hand that you are drawing in each instance/go of the loop/whatever since it's going directly from the hand
            L = end_x - start_x # total length
        
            spacing = (L - len(hand)*card_width) / (len(hand) + 1) # adaptive spacing based on number of cards

            clicking_rect = pygame.Rect(400 + i *(230 + spacing), 900, 230, 307)  # x, y, width, height - matches the position and size of the card images drawn in draw_fight
            
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if clicking_rect.collidepoint(event.pos):
                    print(f"Clicked on card: {card.name}")
                    Player.resolve_move(card)
                    print(f"Played {card}. New hand: {hand}")
                    print(f"Enemy pending_damage: {Enemy.pending_damage}, Player block: {Player.block}")
                    break  # Exit loop after playing one card
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            distance = ((event.pos[0] - 2250) ** 2 + (event.pos[1] - 1230) ** 2) ** 0.5 # distance from coordinates 2250, 1230 (center of the end_turn_circle) **05 = ²√
            if distance <= 100:  # Radius of the circle
                print("End Turn button clicked!")
                game.end_turn()


    def draw_card_choice(self):
        pygame.draw.rect(vscreen, (20, 20, 20), (0, 0, 2560, 1440))  

        my_font = pygame.font.SysFont("Verdana", 50)
        label_surface = my_font.render("Choose a new card to add to your pool", True, (255, 255, 255))  # White text

        vscreen.blit(label_surface, (1280 - label_surface.get_width() / 2, 500))  # Centered at the top of the screen

        game_states.draw_hand(vscreen, current_choices, 500, 720, 2700) # start x, start y, end x - vscreen resolustion: (2560x1440)

    
    def handle_card_choice_logic(self):
        start_x = 500
        end_x = 2700
        card_width = 230

        for i, card in enumerate(current_choices): 
            L = end_x - start_x # total length
        
            spacing = (L - len(current_choices)*card_width) / (len(current_choices) + 1) # adaptive spacing based on number of cards

            clicking_rect = pygame.Rect(start_x + i *(230 + spacing), 720, 230, 307)  # x, y, width, height - matches the position and size of the card images drawn in draw_fight
            if event.type == pygame.MOUSEBUTTONDOWN:
                if clicking_rect.collidepoint(event.pos):
                    print(f"Clicked on card: {card.name}")
                    Player.pool.append(card)
                    print(f"You chose {card.name} to add to your pool!")
                    game_states.prepare_map()
                    break  # Exit loop after choosing one card
        

    






    def handle_map_logic(self):
        global game_state
        global Enemy
        global Player


        

        

        for layer in layers:
            for node in layer:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    distance = ((event.pos[0] - node.node_x) ** 2 + (event.pos[1] - node.node_y) ** 2) ** 0.5
                    if distance <= 30:  # node radius is 30, at least for now
                        if node in Player.current_node.connections:

                            print(f"Moving to node: {node}")
                            Player.current_node = node
                            if node.encounter_type == "enemy" or node.encounter_type == "boss": #assigning a boss is handled in assign_new_enemy
                                game.assign_new_enemy()
                                Player.make_hand()
                                

                                game_state = "fight"
                            
                            elif node.encounter_type == "rest":
                                game_state = "rest"
                            
                            elif node.encounter_type == "shop":
                                game_states.prepare_shop()
                                


                        else:
                            print("You can't move to that node from your current position.")


    def draw_rest(self):
        heal_by = Player.maxHP * 0.2
        heal_by = round(heal_by)
        if heal_by + Player.HP > Player.maxHP:
            heal_by = Player.maxHP - Player.HP

        vscreen.blit(Images["Rest_Backround.png"], (0, 0))  # Draw rest background. So far a placeholder. And a shitty one at that

        my_font = pygame.font.SysFont(None, 36)
        
        pygame.draw.rect(vscreen, (5, 222, 5), (500, 500, 400, 100))  # Big green heal button
        text_surface = my_font.render(f"heal for 20% of max HP({heal_by})", True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(700, 540))
        vscreen.blit(text_surface, text_rect)

        pygame.draw.rect(vscreen, (240, 240, 240), (500, 650, 400, 100))  # White upgrade button
        text_surface = my_font.render("Upgrade", True, (0, 0, 0))  # black text
        text_rect = text_surface.get_rect(center=(700, 690))
        vscreen.blit(text_surface, text_rect)

        my_font = pygame.font.SysFont(None, 80)
        pygame.draw.rect(vscreen, (255, 255, 255), (2560 -500 -400, 500, 400, 250))  # White continue button (2560x1440), same distance from the edge as the other two buttons
        text_surface = my_font.render("Continue", True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(2560 -500 -400//2, 500 + 250//2))
        vscreen.blit(text_surface, text_rect)


        Player_status_box = pygame.Rect(1, 1400, 2560, 50)  # x, y, width, height
        pygame.draw.rect(vscreen, (128, 128, 128), Player_status_box)  #backround for player status

        my_font = pygame.font.SysFont("Verdana", 30)
        Player_status_surface = my_font.render(f"{Player.name}) HP:{Player.HP}/{Player.maxHP} STR:{Player.STR} DEF:{Player.DEF} Block:{Player.block} Pending Damage:{Player.pending_damage} Energy:{Player.Energy}/{Player.MaxEnergy} Effects:{Player.status_effects}", True, (255, 255, 255))  # White text
        vscreen.blit(Player_status_surface, (10, 1403))  # Draw player status


        # Only run the heal animation if it's playing
        if heal_animation_playing:
            game_states.draw_heal_animation()


    def handle_rest_logic(self):
        global spent_rest, game_state

        if event.type == pygame.MOUSEBUTTONDOWN:
            heal_button_rect = pygame.Rect(500, 500, 400, 100)
            upgrade_button_rect = pygame.Rect(500, 650, 400, 100)
            continue_button_rect = pygame.Rect(2560 -500 -400, 500, 400, 250)

            if heal_button_rect.collidepoint(event.pos):
                if spent_rest == False:
                    x = Player.maxHP * 0.2
                    x = round(x)
                    Player.HP += x
                    if Player.HP > Player.maxHP:
                        Player.HP = Player.maxHP
                    print(f"{Player.name} healed for {x} HP! Current HP: {Player.HP}")
                    spent_rest = True
                    # start heal animation (modify the module-level flag)
                    global heal_animation_playing, particle_alpha, set_up_heal_animation
                    heal_animation_playing = True
                    set_up_heal_animation = True
                    particle_alpha = 255
                else:
                    print("You have already healed at this rest stop.")


            elif upgrade_button_rect.collidepoint(event.pos):
                if spent_rest == False:
                    self.prepare_rest_upgrade()

            elif continue_button_rect.collidepoint(event.pos):
                print("Continuing the journey...")
                spent_rest = False
                heal_animation_playing = False
                game_state = "map"
            
    def draw_heal_animation(self): #Spawns a heal parcticle that progresively moves down and more transparent
        global particle_alpha
        global set_up_heal_animation
        global particle_x
        global particle_y
        global heal_animation_playing


        if heal_animation_playing == True: # animate while playing
            if set_up_heal_animation == True:
                # Spawn the particle at the heal button center instead of relying on event.pos
                particle_x, particle_y = event.pos
                particle_x -= Images["Heal_Particle.png"].get_width() // 2
                particle_y -= Images["Heal_Particle.png"].get_height() // 2
                set_up_heal_animation = False
            particle_y += 1.5  # Move the particle downwards
            particle_alpha -= 6  # Decrease alpha to make it more transparent
            heal_particle = Images["Heal_Particle.png"].copy()
            heal_particle.set_alpha(int(particle_alpha))
            vscreen.blit(heal_particle, (particle_x, particle_y))  # Draw the heal particle
            if particle_alpha <= 0:
                particle_alpha = 255  # Reset alpha for the next time the animation is triggered
                set_up_heal_animation = True  # Reset setup for the next time the animation is triggered
                heal_animation_playing = False  # End the animation

    def prepare_rest_upgrade(self):
        global rest_upgrade_choices
        global game_state

        print("Preparing rest upgrade choices...")
        rest_upgrade_choices = random.sample(Kori_pool, 3)

        game_state = "rest_upgrade"

    def draw_rest_upgrade(self):
        game_states.draw_hand(vscreen, rest_upgrade_choices, 500, 720, 2700) # start x, start y, end x - vscreen resolustion: (2560x1440)

        my_font = pygame.font.SysFont("Verdana", 50)
        label_surface = my_font.render("Choose a card to upgrade", True, (255, 255, 255))  # White text
        vscreen.blit(label_surface, (1280 - label_surface.get_width() / 2, 500))  # Centered at the top of the screen

        if draw_upgrade_potential == True:
            potential_surface = my_font.render(f"{pre_upgrade_potential} -> {upgrade_potential}", True, (255, 255, 255))  # White text
            vscreen.blit(potential_surface, (upgrade_potential_pos))  # Draw potential near the mouse cursor
            


    def handle_rest_upgrade_logic(self):
        global draw_upgrade_potential 
        global upgrade_potential
        global pre_upgrade_potential
        global upgrade_potential_pos
        global game_state
        global spent_rest

        start_x = 500
        end_x = 2700
        card_width = 230

        for i, card in enumerate(rest_upgrade_choices): 
            L = end_x - start_x # total length
        
            spacing = (L - len(rest_upgrade_choices)*card_width) / (len(rest_upgrade_choices) + 1) # adaptive spacing based on number of cards

            clicking_rect = pygame.Rect(start_x + i *(230 + spacing), 720, 230, 307)  # x, y, width, height - matches the position and size of the card images drawn in draw_fight


            if event.type == pygame.MOUSEBUTTONDOWN:
                if clicking_rect.collidepoint(event.pos):
                    print(f"Clicked on card: {card.name}")
                    print(f"upgrading {card.name}...")
                    card.upgrade()
                    print(f"{card.name} has been upgraded! New stats: {card.type}-{card.power}")
                    game_state = "rest"
                    spent_rest = True # so that you can't heal after upgrading, since that would be pretty busted ngl
                    


            if event.type == pygame.MOUSEMOTION:  # Check for mouse movement because pygame is stupid and will cry like a little baby if you try to get position of a keypress
                
                if clicking_rect.collidepoint(event.pos):
                    draw_upgrade_potential = True
                    pre_upgrade_potential = card.power

                    if "spell" == card.type:
                        upgrade_potential = 0 #spells only cary tags and don't do anything, so upgrading their power is pointless
                    else:
                        upgrade_potential = card.power + 4 + card.power*0.2 #how much the card could be upgraded
                        upgrade_potential = round(upgrade_potential)
                        
                    upgrade_potential_pos = event.pos
                    
                    break # That break has to be here because otherwise it would go check the next card and go "Oh, I am not coliding, I will proceed to set the "am I colliding" to False. I am very good at this job and shouldn't be replaced by a genetically modified hamster, thank you very much"
                else:
                    draw_upgrade_potential = False
                         
                
    


    def prepare_shop(self): # only once per shop visit, makes inventory
        global shop_offers
        global game_state
        global shop_prices

        shop_offers = random.sample(floor1_loot, 7) # More than the number displayed in the shop, but as you buy one and remove it from there, the 7th one will get revealed and replace the mising one
        shop_prices = { 0 : 0 }

        for card in shop_offers:
            cost = random.randint(3,6)
            cost = 5*cost
            shop_prices[card] = cost


        game_state = "shop"



    def draw_shop(self):
        global shop_offers
        global shop_prices

        vscreen.blit(Images["Shop_Backround.png"], (0, 0))
        for i, card in enumerate(shop_offers): 
            if i == 0:
                game_states.draw_individual_card(330, 830, card) # The coordinates are kinda eyeballed since the backround is irregular
            elif i == 1:
                game_states.draw_individual_card(270, 390, card)
            elif i == 2:
                game_states.draw_individual_card(695, 385, card)
            elif i == 3:
                game_states.draw_individual_card(1100, 365, card)
            elif i == 4:
                game_states.draw_individual_card(1480, 354, card)
            elif i == 5:
                game_states.draw_individual_card(1419, 795, card) #Had to have the backround redrawn a little since the cards overlapped a little (this one was the trouble maker)

    def draw_individual_card(self,x,y,card): # Modified draw_hand for only 1 card, only used in draw_shop since it has iregular placment of purchusable cards (Thanks Adela, no really I think it looks better)

        my_font = pygame.font.SysFont("Verdana", 36)  # 36 px Verdana

        vscreen.blit(Images[card.image_name],(x, y))  # Draw card image at calculated position

        move_name_surface = my_font.render(card.name, True, (255, 255, 255))  # White text
        vscreen.blit(move_name_surface, (4 + x, y - 41))  # Draw move name above the card

        my_font = pygame.font.SysFont("Verdana", 38)  # setting it slightly bigger for the outline, only works on single characters because math or something, idk I guess you could do it if you individually rendered each character, but it's not like It's all that important for anything aside from the stuff drawn on the moves themselves
        #Actually, I think it's still offset because pygame renders stuff from the top left corner and not the center, but it still gives it a "shade" if the "outline" isn't too much bigger

        move_cost_surface_outline = my_font.render(f"{card.cost}", True, (0, 0, 0))  # black outline
        vscreen.blit(move_cost_surface_outline, (206 + x, y - 8))  

        my_font = pygame.font.SysFont("Verdana", 36)  # setting back to normal

        move_cost_surface = my_font.render(f"{card.cost}", True, (245, 215, 125))  # tan-yellow text
        vscreen.blit(move_cost_surface, (206 + x, y - 8))  # Draw move cost below the move name

        move_stats_surface = my_font.render(f"{card.type}-{card.power}", True, (255, 255, 255))  # White text
        vscreen.blit(move_stats_surface, (4 + x, y + 303))  # Draw move type and power bellow cards
        

        my_font = pygame.font.SysFont("Verdana", 100) #drawing the price
        card_cost_surface = my_font.render(str(shop_prices[card]), True, (255, 255, 100))
        
        image = Images[card.image_name]

        vscreen.blit(card_cost_surface, (x + image.get_width() / 2 - card_cost_surface.get_width() / 2, y + image.get_height() / 2 - card_cost_surface.get_height()/2 )) # the cost of a card in a shop

        my_font = pygame.font.SysFont("Verdana", 36)

        if card.tags:
            if "multihit" in card.tags:
                move_tags_surface = my_font.render(f"Multihit: {card.tags['multihit']}", True, (255, 255, 255))  # White text
                vscreen.blit(move_tags_surface, (4 + x, y + 343))  # Draw move tags below type and power
            
            elif "poison" in card.tags:
                move_tags_surface = my_font.render(f"Poison: {card.tags['poison']}", True, (255, 255, 255))  # White text
                vscreen.blit(move_tags_surface, (4 + x, y + 343))  # Draw move tags below type and power

            elif "draw" in card.tags:
                move_tags_surface = my_font.render(f"Draw: {card.tags['draw']}", True, (255, 255, 255))  # White text
                vscreen.blit(move_tags_surface, (4 + x, y + 343))  # Draw move tags below type and power
            
            elif "redraw" in card.tags:
                move_tags_surface = my_font.render(f"Redraw", True, (255, 255, 255))  # White text
                vscreen.blit(move_tags_surface, (4 + x, y + 343))  # Draw move tags below type and power
            
            elif "energise" in card.tags:
                move_tags_surface = my_font.render(f"Energise: {card.tags['energise']}", True, (255, 255, 255))  # White text
                vscreen.blit(move_tags_surface, (4 + x, y + 343))  # Draw move tags below type and power

            elif "enrage" in card.tags:
                move_tags_surface = my_font.render(f"Enrage", True, (255, 255, 255))  # White text
                vscreen.blit(move_tags_surface, (4 + x, y + 343))  # Draw move tags below type and power
            



    def handle_shop_logic(self):
        global shop_offers
        global shop_prices

        card_dimensions = 230, 307 #dimensions of a card so I don't have to type it all individually, have to put a * before it to "unpack" it or something 

        for i, card in enumerate(shop_offers):
            if i == 0:
                individual_card_clicking_surface = pygame.Rect(330, 830, *card_dimensions)
            elif i == 1:
                individual_card_clicking_surface = pygame.Rect(270, 390, *card_dimensions)
            elif i == 2:
                individual_card_clicking_surface = pygame.Rect(695, 385, *card_dimensions)
            elif i == 3:
                individual_card_clicking_surface = pygame.Rect(1100, 365, *card_dimensions)
            elif i == 4:
                individual_card_clicking_surface = pygame.Rect(1480, 354, *card_dimensions)
            elif i == 5:
                individual_card_clicking_surface = pygame.Rect(1419, 795, *card_dimensions)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if individual_card_clicking_surface.collidepoint(event.pos):
                    if Player.money >= shop_prices[card]:
                        Player.pool.append(card)
                        shop_offers.remove(card)
                        Player.money -= shop_prices[card]
                        print(f"Just bought {card} for {shop_prices[card]}, yepee! Current money: {Player.money}")
                    else:
                        print("not enough money, try again later, sucker")



game_states = node_generation_or_something_idk(layer=0, layer_index=0, encounter_type="start")


def prepare_map():
    global layers
        

    layers = game_states.generate_layers(layer_width=4, layer_depth=8)
    layers = game_states.connect_layers(layers)

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


prepare_map() #sets it up for the first time
    
game = gameloop(Player, Enemy)






Player.current_node = layers[0][0]






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
force_shop = pygame.Rect(1250, 1121, 150, 80)
force_new_card = pygame.Rect(1250, 1202, 150, 80)

    
gimme_money = pygame.Rect(1250, 1283, 150, 80)


exit_button = pygame.Rect(1300, 20, 80, 40)

money_square = pygame.Rect(50, 0, 200, 60)

Eror_screen = pygame.Rect(0, 0, 9999, 9999)


Player.make_hand()


def dev_draw_fight():
    game.draw_button(vscreen, player_square, Player.__repr__())
    game.draw_button(vscreen, enemy_square, Enemy.__repr__())
    game.draw_button(vscreen, player_attack_square, "Player Attack")    
    game.draw_button(vscreen, enemy_attack_square, "Enemy Attack")
    game.draw_button(vscreen, resolve_square, "Resolve Damage")
    game.draw_button(vscreen, end_turn_square, "End Turn")
    game.dev_draw_hand(vscreen, hand, hand_start_x, hand_start_y, end_x, hand_card_width, hand_card_height)
    game.draw_button(vscreen, enemy_intent, f"Enemy Intent: {Enemy.enemy_move if hasattr(Enemy, 'enemy_move') else 'None'}")
    game.draw_button(vscreen, turn_count_square, f"Turn: {turn_count}")
    game.draw_button(vscreen, choose_new_card_square, "Choose New Card")
    game.draw_button(vscreen, enemy_status_square, f"Enemy Status: {Enemy.status_effects}")
    game.draw_button(vscreen, player_status_square, f"Player Status: {Player.status_effects}")
    game.draw_button(vscreen, force_map, "Force Map")
    game.draw_button(vscreen, force_rest, "Force Rest")
    game.draw_button(vscreen, exit_button, "X")
    game.draw_button(vscreen, money_square, f"Money: {Player.money}")
    game.draw_button(vscreen, gimme_money, "Gimme 10 Money")
    game.draw_button(vscreen, force_shop, "Force Shop")
    game.draw_button(vscreen, force_new_card, "Force New Card")

def draw_error_screen(): 
    game.draw_button(vscreen, Eror_screen, "ERROR: Invalid Game State")

def handle_error_screen_logic(): #If you click, it exits the game since there is nothng else to do
    if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.quit() #Just closes the window, technically not required
        sys.exit() #kill the program. EXTERMINATE. EXTERMINATE. EXTERMINATE.
        

hand_start_x = 200
hand_start_y = 500
hand_card_width = 100
hand_card_height = 150 
end_x= 800


enemy_move = Enemy.make_enemy_move()

#game_states.prepare_shop()

#------------------------------- Main Loop -------------------------------

while True:
    vscreen.fill((0, 0, 0))

    if game_state == "fight":
        if dev_mode == True:
            dev_draw_fight()

        elif dev_mode == False:
            game_states.draw_fight()

    elif game_state == "choose_new_card":
        game_states.draw_card_choice()

    elif game_state == "map":
        game_states.draw_map()

    elif game_state == "rest":
        game_states.draw_rest()

    elif game_state == "rest_upgrade":
        game_states.draw_rest_upgrade()

    elif game_state == "shop":
        game_states.draw_shop()


    

    else:
        draw_error_screen()


    
    if settings == True:
        game.draw_settings()

    if Player.alive == False: 
        Player.draw_defeat_screen()




    for event in pygame.event.get():
        transform_mouse_pos()
        if event.type == pygame.QUIT:  
            pygame.quit() #Just closes the window, technically not required
            sys.exit() #kill the program. EXTERMINATE. EXTERMINATE. EXTERMINATE.
            

        game.go_to_settings()



        if game_state == "fight":
            if dev_mode == True:
                game.dev_handle_basic_logic()
            elif dev_mode == False:
                if Player.alive == False: #disables logic if you are dead
                    pass
                else:
                    game_states.handle_fight_logic()


        elif game_state == "choose_new_card":
            game_states.handle_card_choice_logic()
        
        elif game_state == "map":
            game_states.handle_map_logic()
        
        elif game_state == "rest":
            game_states.handle_rest_logic()

        elif game_state == "rest_upgrade":
            game_states.handle_rest_upgrade_logic()
        
        elif game_state == "shop":
            game_states.handle_shop_logic()



        else: 
            handle_error_screen_logic()


        #overlays on top of everything else:
        if settings == True: 
            game.handle_settings()

        if Player.alive == False:
            Player.handle_defeat_screen_click()

    




    transform_screen()
    pygame.display.flip()
    clock.tick(60)






print("I was *this* close to getting 2k lines of code. This close!") #Not that having a bloated line count is a good think but I think it's a cool milestone
