import pygame,sys, random, time, math


#coordinates sys goes from ground up and from left to right with origin on left down corner at spawn
 
pygame.init()                                                           #set up screen and clock
pygame.display.set_caption("Planefall")
clock= pygame.time.Clock()  
screen = pygame.display.set_mode((1600,800))
screen.fill((255,255,255)) 



def screen_coord(player):
    return(player.x_pos-400,player.y_pos-400,player.x_pos+1200,player.y_pos+400)        #return the coord that are in the display at the moment

class set():
    def __init__(self):

        pass

    

class game_gui():                                                       #handles points calculation, screens and ingame guis
    def __init__(self) -> None:
         self.plane_surf=pygame.image.load('Plane.png').convert_alpha()
         self.plane_surf=pygame.transform.scale2x(pygame.transform.scale2x(self.plane_surf))
         self.plane_rect=self.plane_surf.get_rect()
         self.heart_surf=pygame.image.load('Heart.png').convert_alpha()
         self.heart_rect=self.heart_surf.get_rect()
         self.boost_surf=pygame.image.load('Double_arrow.png').convert_alpha()
         self.boost_rect=self.boost_surf.get_rect()
         self.boost_rect.center=(120,60)
         self.font_title=pygame.font.Font('PublicPixel-z84yD.ttf',80)
         self.font_norm=pygame.font.Font('PublicPixel-z84yD.ttf',50)
         self.font_small=pygame.font.Font('PublicPixel-z84yD.ttf',30)
         self.record_points=0
         self.points=0
         self.level=1
         self.lifes=3
         self.level_points=[0,0]
         self.death_lap=0
         self.ongoing_lap=False


    def start_screen(self):
        screen.fill(('orange'))
        self.plane_rect.center=(800,400)
        screen.blit(self.plane_surf,self.plane_rect)

        self.text1=self.font_title.render("PLANEFALL",False,(0,0,0),)
        self.text1_rect=self.text1.get_rect()
        self.text1_rect.center=(800,200)
        screen.blit(self.text1,self.text1_rect)

        self.point_text=self.font_norm.render("press w to start the game",False,(0,0,0),)
        self.points_rect=self.point_text.get_rect()
        self.points_rect.center=(800,600)
        screen.blit(self.point_text,self.points_rect)
    
    def level_screen(self):
        screen.fill(('brown1'))
        self.plane_rect.center=(800,400)
        screen.blit(self.plane_surf,self.plane_rect)

        self.text1=self.font_title.render("WELL DONE",False,(0,0,0),)
        self.text1_rect=self.text1.get_rect()
        self.text1_rect.center=(800,200)
        screen.blit(self.text1,self.text1_rect)

        self.point_text=self.font_norm.render(f"press w to go to level {self.level}",False,(0,0,0),)
        self.points_rect=self.point_text.get_rect()
        self.points_rect.center=(800,600)
        screen.blit(self.point_text,self.points_rect)

        
    def death_screen(self):
        screen.fill(('black'))
        self.plane_rect.center=(800,400)
        screen.blit(self.plane_surf,self.plane_rect)

        self.text1=self.font_title.render(f"YOU DIED",False,(255,255,255),)
        self.text1_rect=self.text1.get_rect()
        self.text1_rect.center=(800,200)
        screen.blit(self.text1,self.text1_rect)

        self.point_text=self.font_norm.render("press w to restart the game",False,(255,255,255),)
        self.points_rect=self.point_text.get_rect()
        self.points_rect.center=(800,600)
        screen.blit(self.point_text,self.points_rect)

        self.text3=self.font_small.render(f"you died with {round(self.points)}p, your record is {round(self.record_points)}p",False,(255,255,255),)
        self.text3_rect=self.text3.get_rect()
        self.text3_rect.center=(800,700)
        screen.blit(self.text3,self.text3_rect)

        self.level_points=[0,0]
        self.death_lap=0
        self.lifes=3
        
    def stop_screen(self):
        if self.level==1:
            self.start_screen()
        elif self.level==0:
            if self.points>self.record_points: self.record_points=self.points

            self.death_screen()
            
        else: self.level_screen()
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.level==0:self.level=1
            return (True)
        else: return (False)

    def ingame_gui(self):                                               #10 points/sec + 50*level number per level and 20 per death lap
        if player1.ang<4.5 and player1.ang>3.14:
            if not self.ongoing_lap: self.death_lap+=1
            self.ongoing_lap=True
        else: self.ongoing_lap=False
        self.level_points[self.level-1]=(pygame.time.get_ticks()-start_time)/100
        self.points=sum(self.level_points)+((self.level-1)*(self.level)*25)+self.death_lap*20
        self.point_text=self.font_small.render(str(round(self.points)),False,(0,0,0),)
        self.points_rect=self.point_text.get_rect()
        self.points_rect.center=(50,60)
        screen.blit(self.point_text,self.points_rect)

        for life in range(self.lifes):
            self.heart_rect.center=(1600-life*50-30,50)
            screen.blit(self.heart_surf,self.heart_rect)
        if player1.boost_available:screen.blit(self.boost_surf,self.boost_rect)
       

class object():                                                         #ingame objects
    def __init__(self):
        self.x_pos=0
        self.y_pos=0
        self.rect=0
        self.plane_surf=0
    def render(self,playern):                                           #renders the object with screen coord from absolute coord
        self.screen_x=self.x_pos-playern.x_pos+400
        self.screen_y=400-(self.y_pos-playern.y_pos)
        self.rect.center=(self.screen_x, self.screen_y)
        screen.blit(self.plane_surf,self.rect)
        return (self.screen_x, self.screen_y)
        

class ground(object):                                                   #the ground (incomplete: cannot cchange the surface)
    def __init__(self):
        self.x_pos=800
        self.y_pos=0
        self.rect=0
        self.plane_surf=0
    def move(self):
        y0=screen_coord(player1)
        if y0[1]<0:
            self.plane_surf=pygame.Surface((1600, round(-y0[1])))
            self.plane_surf.fill('green')
            self.y_pos=y0[1]/2
            self.x_pos=player1.x_pos+400
            self.rect=self.plane_surf.get_rect()
            self.render(player1)
            

class cloud(object):                                                    #clouds are positioned high in the sky randomly and cover the plane
    
    def __init__(self,x_pos):
        self.plane_surf=pygame.Surface((random.randint(150,200),random.randint(80,120)))
        self.plane_surf.fill('azure4')
        self.rect=self.plane_surf.get_rect()
        self.y_pos=1200+random.randint(-50,+50)
        self.x_pos=x_pos

class tree(object):                                                    #clouds are positioned high in the sky randomly and cover the plane
    
    def __init__(self,x_pos):
        self.plane_surf=pygame.Surface((50,100))
        self.plane_surf=pygame.image.load('Tree.png')
        #self.plane_surf.fill('red2')
        self.rect=self.plane_surf.get_rect()
        self.y_pos=50
        self.x_pos=x_pos


class shot(object):                                                     #shoot functions generate shots
    def __init__(self,ang, v_shooter, x_pos, y_pos):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.v=10+v_shooter
        self.ang=ang
        self.plane_surf=pygame.image.load('Shot.png').convert_alpha()
        #self.plane_surf.fill('gold')
        self.plane_surf=pygame.transform.rotate(self.plane_surf,self.ang/math.pi*180)
        self.rect=self.plane_surf.get_rect()
        
    def move(self):
        self.x_pos += self.v*math.cos(self.ang)
        self.y_pos += self.v*math.sin(self.ang)
        self.rect.center=(self.x_pos,self.y_pos)
        

class player(object):
    def __init__(self):
        self.y_pos=50
        self.x_pos=400
        self.v=10
        self.g=-0.27
        self.ang=0
        self.Vacc=0
        self.vy=0
        self.vx=0
        self.boost_time=0
        self.boost_start=0
        self.boost_active=False
        self.boost_available=False
        self.shots=[]
        self.shoot_time=0
        self.surf_orig=pygame.image.load('Plane.png').convert_alpha()
    
    def gravity(self): 
        self.acc=self.g+abs(self.vx/(self.v*3))                         #plane flies if goes fast enough 
        self.Vacc+=self.acc
        if self.Vacc>0 :self.Vacc=0

        if self.vx<0: self.ang-=0.1*math.cos(self.ang)                  #nose goes down if fly upside down
        self.ang=self.ang%(2*math.pi)                                   

        self.vx=self.v*math.cos(self.ang)                               #calculates speed on axes given costant speed (with limits)
        self.vy=self.v*math.sin(self.ang)+self.Vacc
        if self.vy<-15: self.vy=-15
        if self.vy<0:self.vx+=0.1*(-self.vy)*math.cos(self.ang)

        self.x_pos+=self.vx                                              #updates position recreates surfaces
        self.y_pos+=self.vy
        if self.y_pos<0:
            self.y_pos=0
            
        
        self.plane_surf=pygame.transform.rotate(self.surf_orig,self.ang/math.pi*180)
        self.rect=self.plane_surf.get_rect()
        
        
    def shoot(self):
        if pygame.time.get_ticks()-self.shoot_time>500:                 #shoot every 500ms if called
            self.shots.append(shot((self.ang + random.gauss(0,0.02)), self.v,self.x_pos,self.y_pos))
                     
            self.shoot_time=pygame.time.get_ticks()
    
    def bomb(self):
        pass

    def boost(self,keys):
        #print(pygame.time.get_ticks()-self.boost_time,pygame.time.get_ticks()-self.boost_start)                                               #handles boost
        if pygame.time.get_ticks()-self.boost_time>10000 and pygame.time.get_ticks()-self.boost_start<1000:
            self.boost_available=True
        else: self.boost_available=False
        if keys[pygame.K_RIGHT]and self.boost_available: 
                self.v=25
                self.boost_active=True
        elif self.boost_active:
            self.boost_active=False
            self.boost_time=pygame.time.get_ticks()
            
        elif self.v>10: self.v-=0.5
        else: 
            self.v=10
            self.boost_start=pygame.time.get_ticks()
                
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: self.ang+=0.05
        if keys[pygame.K_DOWN]: self.ang-=0.05
        self.boost(keys)
        if keys[pygame.K_SPACE]: self.shoot()
        if keys[pygame.K_RETURN]: self.bomb()
        
    
    def update_shots(self):
        if self.shots:                                                  #moves every shot and deletes the ones that are too far
            for shot_n in self.shots:  
                 shot_n.move()
                 shot_n.render(self)
            self.shots=[shot_n for shot_n in self.shots if shot_n.screen_x<1700 and shot_n.screen_x>-100 and shot_n.screen_y>-100 and shot_n.screen_y<900]    

    
class airship(object) :
    pass


class plane(object):
    def __init__(self,x_spawn, y_spawn):
        self.y_pos=y_spawn
        self.x_pos=x_spawn
        self.v=8
        self.g=-0.27
        self.ang=0
        self.Vacc=0
        self.vy=0
        self.vx=0
        self.shots=[]
        self.shoot_time=0
        self.surf_orig=pygame.image.load('Plane.png').convert_alpha()
        self.surf_orig=pygame.transform.flip(self.surf_orig,True,False)

    def gravity(self):
        self.acc=self.g+abs(self.vx/self.v*3)                           #plane flies if goes fast enough
        self.Vacc+=self.acc
        if self.Vacc>0 :self.Vacc=0

        if self.vx<0: self.ang-=0.1*math.cos(self.ang)                  #nose goes down if fly upside down
        self.ang=((self.ang+math.pi)%(2*math.pi))-math.pi 
        
        self.vx=self.v*math.cos(self.ang)                               #calculates speed on axes given costant speed (with limits)
        self.vy=self.v*math.sin(self.ang)+self.Vacc
        if self.vy<0:self.vx+=0.1*(-self.vy)*math.cos(self.ang)
        if self.vy<-15: self.vy=-15

        self.x_pos=(self.x_pos-self.vx)                                 #updates position recreates surfaces
        self.y_pos+=self.vy
        
        self.plane_surf=pygame.transform.rotate(self.surf_orig,(-self.ang)/math.pi*180)
        self.rect=self.plane_surf.get_rect()
        

    def move(self, x, y):
        try: aim_ang = math.atan((y-self.y_pos)/abs(x-self.x_pos))      #aims at the angle between the player and himself and reaches it slowly
        except ZeroDivisionError: aim_ang=math.pi/2
        if  abs(aim_ang-self.ang)<0.01: pass
        elif aim_ang>self.ang and self.ang< math.pi/4: self.ang+=0.01
        elif aim_ang<self.ang and self.ang> -math.pi/4: self.ang-=0.01
        

    def shoot(self):
        if pygame.time.get_ticks()-self.shoot_time>1000:                 #shoot every 500ms
            self.shots.append(shot(math.pi-self.ang+random.gauss(0,0.05), self.v,self.x_pos,self.y_pos))
            self.shoot_time=pygame.time.get_ticks()

    def update_shots(self,playern):
        if self.shots: 
            for shot_n in self.shots:  
                shot_n.move()
                shot_n.render(playern)
            self.shots=[shot_n for shot_n in self.shots if shot_n.screen_x<1700 and shot_n.screen_x>-100 and shot_n.screen_y>-100 and shot_n.screen_y<900]   

game_active=False                                                       #variables to use classes
enemies=[]
clouds=[]
trees=[]
player1=player()
game_gui1=game_gui()
ground1=ground()

while True:

    for event in pygame.event.get():                                    #event queue handler
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

    if   game_active: 
        
        screen.fill(('light blue'))
        game_gui1.ingame_gui()

        player1.gravity()
        player1.get_input()
        player1.update_shots()
        player1.render(player1)
       
        for enemy in enemies:

            enemy.gravity()
            enemy.move(player1.x_pos,player1.y_pos)
            enemy.shoot()
            enemy.update_shots(player1)
            enemy.render(player1)

        #collisions
        
            if pygame.time.get_ticks()-collision_time>500:
                if player1.rect.colliderect(enemy.rect) or player1.rect.collidelist(enemy.shots)!=-1  or player1.rect.collidelist(trees)!=-1 or player1.y_pos<2: 
                    game_gui1.lifes-=1
                    collision_time=pygame.time.get_ticks()
                    if game_gui1.lifes==0 or player1.y_pos<-10:
                        game_active=False
                        game_gui1.level=0
                    
                elif enemy.rect.collidelist(player1.shots)!=-1:
                    game_gui1.level+=1
                    game_active=False
                    game_gui1.level_points.append(0)

           
                    
        enemies=[enemy for enemy in enemies if enemy.screen_x>-200]
        if len(enemies)<=2: 
            enemies.append(plane(player1.x_pos+2000,player1.y_pos+300))
        if len(enemies)<=game_gui1.level: 
            enemies.append(plane(player1.x_pos+1500+random.randint(0,10000),random.randint(50,1000)))
            print("a")
            
        
        print(len(enemies), game_gui1.level)

        x_screen_start,y_screen_start,x_screen_end,y_screen_end=screen_coord(player1)
        
        if len(clouds)<6: clouds.append(cloud(x_screen_start-(x_screen_start%400)+600*(len(clouds)+1)+random.randint(-50,50)))
        
        for cloud1 in (clouds):
            cloud1.render(player1)
        clouds=[cloud1 for cloud1 in clouds if  cloud1.screen_x>-100 ]

        if len(trees)<6 and len(trees):
            #x_tree=x_screen_end-(x_screen_end%400)+600*(len(trees)+1)+random.randint(-300,300)
            x_tree=trees[-1].x_pos+random.randint(40,800)
            trees.append(tree(x_tree))
        elif not len(trees): trees.append(tree(x_screen_end+100))
        

        for tree1 in (trees):
           tree1.render(player1)
        trees=[tree1 for tree1 in trees if  tree1.screen_x>-100 ]

        ground1.move()
        

    else:

        game_active=game_gui1.stop_screen()
        player1=player()
        enemies=[]
        clouds=[] 
        trees=[]
        ground1=ground()
        start_time=pygame.time.get_ticks()
        collision_time=pygame.time.get_ticks()
        player1.boost_time=pygame.time.get_ticks()

    pygame.display.update()                                             #clock 
    clock.tick(60)




    #to do list
    #airships
    #true levels