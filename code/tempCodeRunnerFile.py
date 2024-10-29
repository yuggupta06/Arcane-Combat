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
        self.load_assets()
        self.setup()


    def health_bar(self):
        pygame.draw.rect(self.display_surface,"red",pygame.FRect((20,40),(600,40)),border_radius=3)
        pygame.draw.rect(self.display_surface,"grey",pygame.FRect((20,40),(self.player.health,40)),border_radius=3)
        font=pygame.font.Font(get_absolute_path("font","Red Blood.otf"),50)
        player_name=font.render("ZENITH",True,"white")
        self.display_surface.blit(player_name,(20,90))
        pygame.draw.rect(self.display_surface,"red",pygame.FRect((920,40),(600,42)),border_radius=3)
        pygame.draw.rect(self.display_surface,"grey",pygame.FRect((920,40),(self.opponent.health,42)),border_radius=3)
        player_name=font.render("Verock",True,"white")
        self.display_surface.blit(player_name,(WINDOW_WIDTH-120,90))


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
            