from settings import *
from TImer import Timer
from support import *
from math import atan2 ,sin,degrees
class Sprite(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups,Z_index=0):
        super().__init__(groups)
        self.image=surf
        self.Z_index=Z_index
        self.rect=self.image.get_frect(topleft=pos)


class AnimationSprite(Sprite):
    def __init__(self,frames,pos,groups):
        self.frames,self.frame_index=frames,0
        super().__init__(frames[0],pos,groups)

    def animate(self,dt):
        self.frame_index+=7*dt
        self.image=self.frames[int(self.frame_index)%len(self.frames)]
class Player(Sprite):
    def __init__(self,frames,pos,groups,all_sprites,collision_sprites,game_audio,Z_index=1):
        # frames
        self.frames=frames
        self.frame_index,self.state=0,"idle"
        self.image=frames[self.state]
        # groups
        self.all_sprites=all_sprites
        self.collision_sprites=collision_sprites
        self.weapon_sprites=pygame.sprite.Group()
        self.opponent=True
        self.health=30
        self.Z_index=1
        self.win=0

        super().__init__(self.image[self.frame_index],pos,groups)
        # hitbox and old rect for collisons
        self.hitbox_rect=self.rect.inflate(-190,-50)
        self.old_rect=self.hitbox_rect

        # self.powers={
        #     "kamehameha":Sprite(pygame.transform.scale(import_image("graphics","powers","Dragon"),(100,100)),(20,150),self.all_sprites)
        # }
        self.name="player"
        # direction
        self.direction=vector(0,0)
        self.speed=600
        self.fly_speed=150
        self.jump=False
        self.reverse=False
        self.facing_right=True
        self.animate_speed=3
        self.dir=vector(0,0)             # for taking direction between the two players
        self.down=True                  # for using the control of down movement of the player
        
        self.attack_timer={
            "Sword":Timer(1700,func=self.sword),
            "hit":Timer(2000),                                      # to get hit by sword
            "block":Timer(2000),
            "bomb":Timer(1000,func=self.bomb),
            "super_punch":Timer(3000),                                  # shift +x and shift +n                                                            
            "opponent_kick_block":Timer(4000),                                # for doing shift + x move opponeny block
            "single_punch":Timer(500),
            "dark_power":Timer(8000,func=self.fly_down),  
            "fly_down":Timer(700),                     # for applying gravity when the dark power effect is finished
            "neck":Timer(3000),                        # for attract the opponent towards the player
            "block_neck":Timer(6000),             # for block the keys of opponent when player gets caught by fly attack
            "black_light":Timer(2000,func=self.opponent_attract),
            "Amaterasu_damage":Timer(2000),             # this is  for getting lay down on legs when gettig hit by black flames
            "black_light_block":Timer(3000),              # this is for getting sure that you only should get damage per shot by opponent by shift+w
            "lay_down":Timer(2000),                       # to get lay down when the dark power timer gets finished
            "shield":Timer(3000),
            "kick":Timer(700),
            "kick_dam":Timer(400)
        }

        # for shift + w
        self.special_move=True
        # audio
        self.game_audio=game_audio
    def fly_down(self):
        self.attack_timer["fly_down"].activate()
        self.state="idle"
        self.opponent.attack_timer["fly_down"].activate()
        self.opponent.attack_timer["lay_down"].activate()
        self.opponent.state="lay_down"
        self.opponent.frame_index=0
    def input(self):
        keys=pygame.key.get_pressed()
        # key[(pygame.K_d,pygame.K_a),(pygame.K_r),(pygame.K_q),(pygame.K_LSHIFT,pygame.K_w),(pygame.K_LSHIFT,pygame.K_x),(pygame.K_w),(pygame.K_f)]
        self.direction.x=int(keys[pygame.K_d]-keys[pygame.K_a])
        if keys[pygame.K_d] and not int(keys[pygame.K_a]) and not self.attack_timer["opponent_kick_block"].active  :
            if  self.opponent.state!="single_punch" and not self.jump:
                self.state="run"
            if self.attack_timer["single_punch"].active:
                self.state="single_punch"
            for k,v in self.attack_timer.items():
                if k!="single_punch" and k!="jump" and k!="shield":
                    self.attack_timer[k].deactive()
            self.reverse=False
            self.facing_right=True
        elif keys[pygame.K_a]  and not int(keys[pygame.K_d]) and not self.attack_timer["opponent_kick_block"].active:
            if self.opponent.state!="single_punch" and not self.jump:
                self.state="run"
            if self.attack_timer["single_punch"].active:
                self.state="single_punch"
            for k,v in self.attack_timer.items():
                if k!="single_punch" and k!="jump" and k!="shield":
                    self.attack_timer[k].deactive()
            self.reverse=True
            self.facing_right=False        
        elif keys[pygame.K_r]  and not self.attack_timer["block"].active and not self.attack_timer["super_punch"] :
            self.attack_timer["block"].activate()
            self.attack_timer["Sword"].activate()
            self.state="sword_attack"
            self.frame_index=0
        elif keys[pygame.K_q] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"]:
            self.state="kamehameha"
            self.attack_timer["bomb"].activate()
            self.animate_speed=1.3
            self.attack_timer["block"].activate()
            self.frame_index=0
        elif keys[pygame.K_LSHIFT] and keys[pygame.K_w] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"] and self.special_move:
            if( self.facing_right and self.rect.right<=self.opponent.rect.right) or (not self.facing_right and self.rect.right>=self.opponent.rect.right):
                self.attack_timer["dark_power"].activate()
                self.attack_timer["hit"].activate()
                self.state="darkest_power"
                self.neck=True                                              # for allow opponent to again show Amaterasu
                self.frame_index=0
                self.animate_speed=1 
                self.special_move=False
        elif keys[pygame.K_LSHIFT] and keys[pygame.K_x] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"] :
            if abs(self.opponent.rect.centerx-self.rect.centerx)<150:
                for k,v in self.opponent.attack_timer.items():
                    self.opponent.attack_timer[k].deactive()
                self.state="super_punch"
                self.punch=True
                self.attack_timer["super_punch"].activate()
                self.attack_timer["block"].activate()
                self.attack_timer["hit"].activate()
                self.frame_index=0
                self.opponent.animate_speed=2
                self.opponent.state="punch_dam"
                self.opponent.attack_timer["block"].activate()
                self.opponent.attack_timer["opponent_kick_block"].activate()
                self.punch=False
        elif pygame.key.get_just_pressed()[pygame.K_z]:
            if self.state!="single_punch_damage":
                self.state="punch_block"
                self.frame_index=0
        elif pygame.key.get_just_pressed()[pygame.K_x] and not self.attack_timer["kick"] and not self.jump:
            self.game_audio["kick"].play()
            self.state="kick"
            self.frame_index=0
            self.jump=True
            self.direction.y=-400
            self.direction.x=1 if self.facing_right else -1
            self.attack_timer["kick"].activate()
        else :  
                self.direction.x=0
        if pygame.key.get_just_pressed()[pygame.K_w] and not keys[pygame.K_LSHIFT]   and not self.jump:
            for k,v in self.attack_timer.items():
                self.attack_timer[k].deactive()
            self.frame_index=0
            self.state="jump"
            self.jump=True
            self.direction.y=-700

        if pygame.key.get_just_pressed()[pygame.K_f] and not self.attack_timer["single_punch"]:
            self.game_audio["punch"].play()
            self.frame_index=0
            self.state="single_punch"
            if self.opponent.state!="punch_block":
                self.attack_timer["single_punch"].activate()
                if  self.hitbox_rect.colliderect(self.opponent.hitbox_rect.inflate(10,0)):
                    self.opponent.frame_index=0
                    self.opponent.health-=20
                    self.opponent.state="single_punch_damage"
                    self.opponent.animate_speed=2


        if pygame.key.get_just_pressed()[pygame.K_s] and not self.attack_timer["shield"]:
            Shield(self,self.all_sprites,self.weapon_sprites)
            self.attack_timer["shield"].activate()

    def move(self,dt):
   
        self.hitbox_rect.x+=self.direction.x*self.speed*dt
        if self.jump:
            if self.state!="kick":
                self.state="jump"
            self.direction.y+=1000*dt
        else:
            self.direction.y=0
        self.collision(dt)


        self.hitbox_rect.y+=self.direction.y*dt
        if (self.hitbox_rect.top>=WINDOW_HEIGHT-370):
            self.hitbox_rect.top=WINDOW_HEIGHT-370
            self.jump=False
        

        if self.attack_timer["neck"].active:   
            self.opponent.hitbox_rect.center+=self.dir*1500*dt if self.facing_right else self.dir*1500*dt
            if self.opponent.hitbox_rect.top<=self.hitbox_rect.top:
                self.opponent.hitbox_rect.top=self.hitbox_rect.top
            if self.opponent.hitbox_rect.right>=self.hitbox_rect.left and self.name=="opponent" :
                self.opponent.hitbox_rect.right=self.hitbox_rect.left
            if self.opponent.hitbox_rect.left<=self.hitbox_rect.right+100 and self.name=="player":
                self.opponent.hitbox_rect.left=self.hitbox_rect.right+100
            self.opponent.rect.center=self.opponent.hitbox_rect.center
       
        self.rect.x=self.hitbox_rect.x
        self.rect.y=self.hitbox_rect.y
        if self.attack_timer["dark_power"].active and self.attack_timer["hit"].active:
            self.hitbox_rect.y+=-1*self.fly_speed*dt
        elif self.attack_timer["fly_down"].active:
            self.hitbox_rect.y+=1*400*dt
            if self.hitbox_rect.y>=WINDOW_HEIGHT-370:
                self.hitbox_rect.y=WINDOW_HEIGHT-370
        self.rect.y=self.hitbox_rect.y
    def animate(self,dt):
        self.frame_index+=self.animate_speed*dt
        if self.state=="punch_dam" and self.attack_timer["opponent_kick_block"].active and int(self.frame_index)==len(self.frames[self.state]):  ## for when  opponent is sleep down on groound
            self.frame_index=-1
            self.state="lay_down"
        if self.state=="dark_power_attract" and self.opponent.attack_timer["dark_power"]  and int(self.frame_index)==len(self.frames[self.state]):  ## for when  opponent is sleep down on groound
            self.frame_index-=1
            self.Z_index=2
        if self.attack_timer["lay_down"].active:
            self.frame_index=0
        if self.state=="darkest_power" and self.attack_timer["dark_power"] and int (self.frame_index)==len(self.frames[self.state]):
            if not self.attack_timer["black_light"].active  and not self.attack_timer["black_light_block"]:
                self.opponent.state="Amaterasu_damage"
                self.opponent.frame_index=0
                for k,v in self.opponent.attack_timer.items():
                    self.opponent.attack_timer[k].deactive()
                self.attack_timer["black_light"].activate()
                self.opponent.attack_timer["block_neck"].activate()
                for i in range(0,20,10):
                    Dark(self.frames["Amaterasu"],self.opponent,(i,i),self.all_sprites)
            self.frame_index-=1
        if self.attack_timer["black_light"].active:
            self.opponent.frame_index=0
        if self.attack_timer["kick"] :
            self.frame_index=0
        if self.opponent.state=="punch_dam":
            self.opponent.health-=0.1
        if int(self.frame_index)<len(self.frames[self.state]):
            if self.attack_timer["hit"].active and self.state=="idle":            ## for when player hit with sword 
                self.frame_index=0
                self.state="down"
                
            self.image=self.frames[self.state][int(self.frame_index)%len(self.frames[self.state])]
            if self.reverse:
                self.image=pygame.transform.flip(self.image,True,False)
        
        else:
            for k,v in self.attack_timer.items():
                if k!="hit" and k!="opponent_kick_block" and k!="single_punch" and k!="fly_down" and k!="dark_power" and k!="black_light" and k!="block_neck" and k!="shield":
                    self.attack_timer[k].deactive()
            self.frame_index=0
            self.animate_speed=3
            self.Z_index=1
            self.state="idle"

    def sword(self):
        for sprite in self.all_sprites:
            if hasattr(sprite,"name") and self.name!=sprite.name:
                Sword((sprite.rect.x-200,-100),(self.all_sprites,self.opponent.weapon_sprites),sprite)
                Sword((sprite.rect.x+200,-100),(self.all_sprites,self.opponent.weapon_sprites),sprite)

    def bomb(self):
        Bomb(self,(self.all_sprites,self.opponent.weapon_sprites),self.collision_sprites,self.weapon_sprites)

    def collision(self,dt):
        # sword collision
        group=[sprite for sprite in self.all_sprites if hasattr(sprite,"weapon")]
        collision_sprites=pygame.sprite.spritecollide(self,group,False,pygame.sprite.collide_mask)
        for sprite in collision_sprites:
                if not self.attack_timer["hit"].active:
                    self.health-=100
                    self.attack_timer["hit"].activate()
                    self.state="down"
                    self.attack_timer["dark_power"].deactive()
                    self.attack_timer["fly_down"].activate()

        # player collision
        if self.hitbox_rect.colliderect(self.opponent.hitbox_rect):
            if self.hitbox_rect.right>=self.opponent.hitbox_rect.left and self.old_rect.left<self.opponent.old_rect.left:
                    self.hitbox_rect.right=self.opponent.hitbox_rect.left
                    if self.state=="kick":
                        self.attack_timer["kick"].deactive()
                        self.opponent.attack_timer["kick_dam"].activate()
                        self.opponent.direction.x=0.5
                        self.opponent.state="kick_dam"
                        self.opponent.frame_index=0
                        self.opponent.animate_speed=2
                        self.opponent.health-=20
            elif self.hitbox_rect.left<=self.opponent.hitbox_rect.right and self.old_rect.right>self.opponent.old_rect.left:
                    self.hitbox_rect.left=self.opponent.hitbox_rect.right
                    if self.state=="kick":
                        self.attack_timer["kick"].deactive()
                        self.opponent.attack_timer["kick_dam"].activate()
                        self.opponent.direction.x=-0.5
                        self.opponent.state="kick_dam"
                        self.opponent.frame_index=0
                        self.opponent.animate_speed=2
                        self.opponent.health-=20
                    
            elif self.hitbox_rect.left<=self.opponent.hitbox_rect.right and self.old_rect.right>self.opponent.old_rect.left:
                    self.hitbox_rect.left=self.opponent.hitbox_rect.right
            elif self.hitbox_rect.bottom>=self.opponent.hitbox_rect.top:
                self.hitbox_rect.bottom=self.opponent.hitbox_rect.top
                self.jump=False
    
        # single punch collision


    def flicker(self):
        if self.attack_timer["hit"].active and self.state=="down" and sin(pygame.time.get_ticks()*150)>=0 :
            red_mask = pygame.Surface((self.image.get_size()), pygame.SRCALPHA)
            red_mask.fill((255, 0, 0, 255))  
            red_mask.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.image=red_mask

    def wall_collision(self):
        if self.hitbox_rect.left<=-60:
            self.hitbox_rect.left=-60
        if self.hitbox_rect.right>=WINDOW_WIDTH-100:
            self.hitbox_rect.right=WINDOW_WIDTH-100

    def opponent_attract(self):
        if not self.attack_timer["neck"].active:
            self.attack_timer["neck"].activate()
            self.opponent.state="dark_power_attract"
            self.opponent.frame_index=0
            self.opponent.reverse=False
            self.opponent.facing_right=not self.facing_right
            self.attack_timer["black_light_block"].activate()
            self.dir=vector(vector(self.hitbox_rect.topleft)-vector(self.opponent.hitbox_rect.topleft)).normalize()
    def update(self,dt):
        self.old_rect=self.hitbox_rect
        # pygame.draw.rect(self.image,"green",pygame.FRect((0,0),(self.image.get_size())),3)
        for timer in self.attack_timer.values():
            timer.update()
        if not self.attack_timer["hit"].active and not self.attack_timer["dark_power"] and not self.attack_timer["opponent_kick_block"] and not self.attack_timer["fly_down"]  and not self.attack_timer["block_neck"].active  and not self.attack_timer["kick"] and not self.attack_timer["kick_dam"]:
            self.input()
        self.move(dt)
        self.wall_collision()
        self.animate(dt)
        self.flicker()
           
class Sword(Sprite):
    def __init__(self,pos,groups,opponent):
        image=import_image("graphics","weapons","sword")
        sword_surf=pygame.transform.scale(image,(200,200))
        self.sword_surf=pygame.transform.flip(sword_surf,False,True)
        super().__init__(self.sword_surf,(pos),groups)
        # direction
        self.all_sprites=groups
        self.direction=vector(1,1)
        self.opponent=opponent
        self.speed=2500
        self.weapon="sword"

    def update(self,dt):
        if self.rect.bottom<self.opponent.rect.top:
            self.direction=(vector(self.opponent.rect.center-vector(30,0))-vector(self.rect.center)).normalize()
            angle=degrees(atan2(self.direction.x,self.direction.y))-90
            self.image=pygame.transform.rotate(self.sword_surf,angle)
        if self.rect.top>WINDOW_HEIGHT+50:
            self.kill()
        self.rect.center+=self.direction*self.speed*dt

class Opponent(Player):
    def __init__(self,frames,pos,groups,all_sprites,collision_sprites,game_audio):
        super().__init__(frames,pos,groups,all_sprites,collision_sprites,game_audio)
        self.reverse=False
        self.name="opponent"
        self.facing_right=False


    def input(self):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_l]-keys[pygame.K_j])
        if keys[pygame.K_u] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"]  :
            self.attack_timer["block"].activate()
            self.attack_timer["Sword"].activate()
            self.state="sword_attack"
            self.frame_index=0
        elif keys[pygame.K_p] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"] :
            self.state="kamehameha"
            self.animate_speed=1.3
            self.attack_timer["bomb"].activate()
            self.attack_timer["block"].activate()
            self.frame_index=0
        elif keys[pygame.K_RSHIFT] and keys[pygame.K_i] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"]  and self.special_move:
            if( not self.facing_right and self.rect.right>=self.opponent.rect.right) or ( self.facing_right and self.rect.right<=self.opponent.rect.right):
                self.attack_timer["dark_power"].activate()
                self.attack_timer["hit"].activate()
                self.state="darkest_power"
                self.neck=True                                              # for allow opponent to again show Amaterasu
                self.frame_index=0
                self.animate_speed=1 
                self.special_move=False
        elif keys[pygame.K_RSHIFT] and keys[pygame.K_n] and not self.attack_timer["block"].active and not self.attack_timer["super_punch"]  :
            if abs(self.opponent.rect.centerx-self.rect.centerx)<150:
                    self.state="super_punch"
                    self.punch=True
                    self.attack_timer["super_punch"].activate()
                    self.attack_timer["block"].activate()
                    self.attack_timer["opponent_kick_block"].activate()
                    self.frame_index=0
                    self.opponent.animate_speed=2
                    self.opponent.state="punch_dam"
                    self.opponent.attack_timer["block"].activate()
                    self.opponent.attack_timer["opponent_kick_block"].activate()
                    self.punch=False
        elif keys[pygame.K_l] and not int(keys[pygame.K_j]) and not self.attack_timer["opponent_kick_block"].active:
            if  self.opponent.state!="single_punch" and not self.jump:
                self.state="run"
            if self.attack_timer["single_punch"].active:
                self.state="single_punch"
                self.opponent.state="single_punch_damage"
            for k,v in self.attack_timer.items():
                if k!="single_punch" and k!="jump" and k!="shield":
                    self.attack_timer[k].deactive()
            self.reverse=True
            self.facing_right=True
        elif keys[pygame.K_j]  and not int(keys[pygame.K_l]) and not self.attack_timer["opponent_kick_block"].active :
            if  self.opponent.state!="single_punch" and not self.jump:         # when player get a punch then it should not in run state
                self.state="run"
            if self.attack_timer["single_punch"].active:
                self.state="single_punch"
            for k,v in self.attack_timer.items():
                if k!="single_punch" and k!="jump" and k!="shield":
                    self.attack_timer[k].deactive()
            self.reverse=False
            self.facing_right=False
        elif pygame.key.get_just_pressed()[pygame.K_m]:
            if self.state!="single_punch_damage":
                self.state="punch_block"
                self.frame_index=0
        elif pygame.key.get_just_pressed()[pygame.K_n] and not self.attack_timer["kick"] and not self.jump:
            self.state="kick"
            self.frame_index=0
            self.jump=True
            self.direction.y=-400
            self.direction.x=1 if self.facing_right else -1
            self.attack_timer["kick"].activate()
        else :
            self.direction.x=0
        if pygame.key.get_just_pressed()[pygame.K_i] and not keys[pygame.K_RSHIFT] and not self.jump:
            for k,v in self.attack_timer.items():
                self.attack_timer[k].deactive()
            self.frame_index=0
            self.state="jump"
            self.jump=True
            self.direction.y=-700
        if pygame.key.get_just_pressed()[pygame.K_h] and not self.attack_timer["single_punch"] :
            self.frame_index=0
            self.state="single_punch"
            if self.opponent.state!="punch_block":
                self.attack_timer["single_punch"].activate()
                if  self.hitbox_rect.colliderect(self.opponent.hitbox_rect.inflate(10,0)):
                    self.opponent.frame_index=0
                    self.opponent.health-=20
                    self.opponent.state="single_punch_damage"
                    self.opponent.animate_speed=2


        if pygame.key.get_just_pressed()[pygame.K_k] and not self.attack_timer["shield"]:
            Shield(self,self.all_sprites,self.weapon_sprites)
            self.attack_timer["shield"].activate()

class Bomb(Sprite):
    def __init__(self,player,groups,collision_sprites,weapon_sprites):
        surf=import_image("graphics","weapons","bomb")
        bomb_surf=pygame.transform.scale(surf,(surf.get_width()/6,surf.get_height()/6))
        self.player=player
        pos=player.rect.center+vector(40,-25) if player.facing_right else player.rect.center+vector(-110,-25)
        super().__init__(bomb_surf,pos,groups)
        self.collision_sprites=collision_sprites
        self.weapon_sprites=weapon_sprites
        self.speed=700
        self.direction=1 if player.facing_right else -1
    def colision(self):
        collision_sprites=pygame.sprite.spritecollide(self,self.collision_sprites,False,pygame.sprite.collide_mask)
        if collision_sprites and collision_sprites[0].name!=self.player.name:
            self.player.opponent.health-=50
            self.player.opponent.attack_timer["hit"].activate()
            self.player.opponent.state="down"
            self.kill()
        if pygame.sprite.spritecollide(self,self.weapon_sprites,True,pygame.sprite.collide_mask):
            self.kill()
    def update(self,dt):
        self.rect.right+=self.direction*self.speed*dt

        if self.rect.left>WINDOW_WIDTH+20:
            self.kill()
        if self.rect.right<0:
            self.kill()   
        self.colision()   


class Dark(Sprite):
    def __init__(self,frames,opponent,offset,groups):
        self.frames,self.frame_index=frames,0
        image=self.frames[self.frame_index]
        self.opponent=opponent
        super().__init__(image,opponent.rect.topleft,groups)
        self.offset=vector(offset)
    def update(self,dt):
        self.rect.topleft=vector(self.opponent.rect.topleft)+vector(self.offset)
        self.frame_index+=4*dt
        self.opponent.health-=0.1
        self.image=self.frames[int(self.frame_index)% len(self.frames)]
        if self.opponent.state=="lay_down":
            self.kill()

class Shield(AnimationSprite):
    def __init__(self,player,groups,weapon_sprites):
        frames=[pygame.transform.scale(frame,(265,265))for frame in import_folder("graphics","shield_frames")]
        self.player=player
        self.weapon_sprites=weapon_sprites
        super().__init__(frames,self.player.rect.topleft,groups)
        self.rect.center=player.rect.center

    def update(self,dt):
        self.animate(dt)
        collision_sprites=pygame.sprite.spritecollide(self,self.weapon_sprites,True,pygame.sprite.collide_mask)
        self.rect.center=self.player.rect.center
        if not self.player.attack_timer["shield"].active:
            self.kill()


class BG(AnimationSprite):
    def __init__(self,frames,groups):
        super().__init__(frames,(0,0),groups)
    
    def update(self,dt):
        self.animate(dt)
    