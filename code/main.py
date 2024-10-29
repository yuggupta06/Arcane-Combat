from settings import *
from sprites import *
from groups import *
from support import *
class Game:
    def __init__(self):
        pygame.init()
        self.display_surface=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.running=True
        self.clock=pygame.time.Clock()
        # groups
        self.player_surf=import_image("graphics","player1","Char_1")
        self.opponent_surf=import_image("graphics","player1","Char_2")
        self.all_sprites=AllSprites()
        self.collision_sprites=pygame.sprite.Group()
        self.start=False
        self.end_round=False
        self.round=1

        self.game_audio=audio_importer("sound")
        self.game_audio["game"].play(loops=-1)
        self.load_assets()
        self.setup()
    
    def font_name(self,title,font_size,pos,colour,path):
        font=pygame.font.Font(get_absolute_path("font",path),font_size)
        player_name=font.render(title,True,colour)
        player_rect=player_name.get_frect(center=pos)
        self.display_surface.blit(player_name,player_rect)

    def roundBar(self):
        
        if self.player.health<=0:
                self.opponent.win+=1
                self.player.health=0
                self.font_name("Verock WINS",140,(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),"#FF7F11","Oxanium-Bold.ttf")
        elif self.opponent.health<=0:
                self.player.win+=1 
                self.opponent.health=0
                self.font_name("Zenith WINS",140,(WINDOW_WIDTH/2,WINDOW_HEIGHT/2),"#FF7F11","Oxanium-Bold.ttf")
        if not self.end_round:
            self.font_name(f'ROUND {self.round}' if self.round!=3 else "FINAL ROUND" ,130,(WINDOW_WIDTH/2,200),"grey","Oxanium-Bold.ttf")
            self.font_name("START?",120,(WINDOW_WIDTH/2,WINDOW_HEIGHT/1.8),"#FF7F11","Oxanium-Bold.ttf")

    def health_bar(self):
        if pygame.key.get_just_pressed()[pygame.K_RETURN]:
            if self.end_round:
                print(self.player.win)
                if self.player.win==2 or self.opponent.win==2:
                    self.running=False
                if self.round==3:
                    self.running=False
                for sprite in self.all_sprites:
                    sprite.kill()
                self.load_assets()
                self.setup()
                self.end_round=False
                self.start=False
                self.round+=1
            elif not self.start:
                self.start=True
                self.game_audio["fight"].play()
        if (self.player.health<=0 or self.opponent.health<=0):
                self.end_round=True
                self.start=False
               
        pygame.draw.rect(self.display_surface,"red",pygame.FRect((20,40),(600,40)),border_radius=3)
        pygame.draw.rect(self.display_surface,"grey",pygame.FRect((20,40),(self.player.health,40)),border_radius=3)
        self.font_name("ZENITH",50,(100,110),"white","Red Blood.otf")
        pygame.draw.rect(self.display_surface,"red",pygame.FRect((920,40),(600,42)),border_radius=3)
        pygame.draw.rect(self.display_surface,"grey",pygame.FRect((920,40),(self.opponent.health,42)),border_radius=3)
        self.font_name("VEROCK",50,(WINDOW_WIDTH-100,110),"white","Red Blood.otf")


    def load_assets(self):
        kamehameha=get_image(self.player_surf,frame_x=9,frame_y=5,width=PlAYER_TILE_SIZE,height=PlAYER_TILE_SIZE,end_number=3)
        del kamehameha[1]
        punch_dam=get_image(self.player_surf,frame_x=0,frame_y=3,end_number=8)
        del punch_dam[6]
        del punch_dam[2]
        darkest_power=get_image(self.player_surf,frame_x=4,frame_y=0,end_number=3)
        darkest_power.append(get_image(self.player_surf,frame_x=11,frame_y=4)[0])

        self.player_frames={
            "idle":get_image(self.player_surf,frame_x=0,frame_y=0),
            "run":get_image(self.player_surf,frame_x=1,frame_y=1),
            "sword_attack":get_image(self.player_surf,frame_x=0,frame_y=5,end_number=6),
            "kamehameha":kamehameha,
            "super_punch":get_image(self.player_surf,frame_x=3,frame_y=2,end_number=6),
            "kick":get_image(self.player_surf,frame_x=9,frame_y=2),
            "kick_dam":get_image(self.player_surf,frame_x=1,frame_y=3),
            "punch_dam":punch_dam,
            "down":get_image(self.player_surf,frame_x=16,frame_y=0),
            "single_punch":get_image(self.player_surf,frame_x=2,frame_y=2),
            "single_punch_damage":get_image(self.player_surf,frame_x=3,frame_y=3),
            "lay_down":get_image(self.player_surf,frame_x=7,frame_y=3),
            "darkest_power":darkest_power,
            "dark_power_attract":get_image(self.player_surf,frame_x=4,frame_y=3),
            "Amaterasu":get_image(self.opponent_surf,frame_x=0,frame_y=6,end_number=4),
            "Amaterasu_damage":get_image(self.player_surf,frame_x=9,frame_y=3),
            "jump":get_image(self.player_surf,frame_x=15,frame_y=2),
            "punch_block":get_image(self.player_surf,frame_x=0,frame_y=3)
            }
        
        kamehameha=get_image(self.opponent_surf,frame_x=9,frame_y=5,width=PlAYER_TILE_SIZE,height=PlAYER_TILE_SIZE,end_number=3)
        del kamehameha[1]
        punch_dam=get_image(self.opponent_surf,frame_x=0,frame_y=3,end_number=8)
        del punch_dam[6]
        del punch_dam[2]
        darkest_power=get_image(self.opponent_surf,frame_x=4,frame_y=0,end_number=3)
        darkest_power.append(get_image(self.opponent_surf,frame_x=11,frame_y=4)[0])
            
        self.opponent_frames={
            "idle":get_image(self.opponent_surf,frame_x=0,frame_y=0,width=PlAYER_TILE_SIZE,height=PlAYER_TILE_SIZE),
            "run":get_image(self.opponent_surf,frame_x=1,frame_y=1,width=PlAYER_TILE_SIZE,height=PlAYER_TILE_SIZE),
            "sword_attack":get_image(self.opponent_surf,frame_x=0,frame_y=5,width=PlAYER_TILE_SIZE,height=PlAYER_TILE_SIZE,end_number=6),
            "kamehameha":kamehameha,
            "super_punch":get_image(self.opponent_surf,frame_x=3,frame_y=2,end_number=6),
            "punch_dam":punch_dam,
            "down":get_image(self.opponent_surf,frame_x=16,frame_y=0),
            "single_punch":get_image(self.opponent_surf,frame_x=2,frame_y=2),
            "single_punch_damage":get_image(self.opponent_surf,frame_x=3,frame_y=3),
            "kick":get_image(self.opponent_surf,frame_x=9,frame_y=2),
            "kick_dam":get_image(self.opponent_surf,frame_x=1,frame_y=3),
            "lay_down":get_image(self.opponent_surf,frame_x=7,frame_y=3),
            "darkest_power":darkest_power,
            "dark_power_attract":get_image(self.opponent_surf,frame_x=4,frame_y=3),
            "Amaterasu":get_image(self.opponent_surf,frame_x=0,frame_y=6,end_number=4),
            "Amaterasu_damage":get_image(self.opponent_surf,frame_x=9,frame_y=3),
            "jump":get_image(self.player_surf,frame_x=15,frame_y=2),
            "punch_block":get_image(self.opponent_surf,frame_x=0,frame_y=3)
            }

        self.BG_frames=[pygame.transform.scale(frame,(WINDOW_WIDTH,WINDOW_HEIGHT))  for frame in import_folder("graphics",("bg_frames"))]
        
    def setup(self):
        map=load_pygame(get_absolute_path("data","map","world.tmx"))
        if self.round==1:
            for x,y ,image in map.get_layer_by_name("Main").tiles():
                Sprite(image,(TILE_SIZE*x,TILE_SIZE*y),self.all_sprites)
        else:
            BG(self.BG_frames,self.all_sprites)
             

        # player
        opponent_frames={}
        for k,v in self.opponent_frames.items():
            opponent_frames[k]=[pygame.transform.flip(frame,True,False) for frame in self.opponent_frames[k]]
        self.opponent=Opponent(opponent_frames,(WINDOW_WIDTH/2+250,WINDOW_HEIGHT-370),(self.all_sprites,self.collision_sprites),self.all_sprites,self.collision_sprites,self.game_audio)
        self.player=Player(self.player_frames,(WINDOW_WIDTH/4-330,WINDOW_HEIGHT-370),(self.all_sprites,self.collision_sprites),self.all_sprites,self.collision_sprites,self.game_audio
        )
        self.player.opponent=self.opponent
        self.opponent.opponent=self.player
        
    def run(self):
        while self.running:
            dt=self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
            self.all_sprites.draw()
            if self.start:
                self.all_sprites.update(dt)
            else:
                self.roundBar()
            self.health_bar()
            pygame.display.update()


if __name__=="__main__":
    game=Game()
    game.run()
# import pygame

# # Initialize Pygame
# pygame.init()

# # Set up the display
# screen = pygame.display.set_mode((400, 400))
# pygame.display.set_caption("Circle with Transparent Overlay")

# # Define colors
# # Blue for the circle
# blackish = (0, 0, 0, 100)  # Semi-transparent black (100 is the alpha value)

# # Set up the clock for FPS
# clock = pygame.time.Clock()

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the screen with white
#     screen.fill((255, 255, 255))

#     # Draw the circle (filled with blue)
#     imgeR=pygame.image.load(get_absolute_path("graphics","powers","Dragon.png")).convert_alpha()
#     screen.blit(imge,(100,100))
#     # pygame.draw.circle(screen, "green", (200, 200), 100)

#     # Create a new surface with per-pixel alpha
#     overlay = pygame.Surface((400, 400), pygame.SRCALPHA)
    
#     # Draw the transparent blackish layer
#     pygame.draw.circle(overlay, blackish, (200, 200), 100)
    
#     # Blit the transparent surface on top of the main screen
#     screen.blit(overlay, (0, 0))

#     # Update the display
#     pygame.display.flip()

#     # Cap the frame rate
#     clock.tick(60)

# # Quit Pygame
# pygame.quit()

# my_dict={"name":"sushma","age":1}

# list1=[("a",1),("b",2)]

# a=dict(list1)
# print(a)

# list3=[1,2,3,4]
# dict3=dict.fromkeys(list3,9)

# dict1={"yug":10,"shivam":30,"shikhar":50,"siddharth":60}
# max=0
# # for k,v in dict1.items():
# #     if v>max:

# grades = 


