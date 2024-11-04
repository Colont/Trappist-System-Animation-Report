import numpy as np
import math
import pygame
pygame.init()
#all info in code is made along side a video
#https://www.youtube.com/watch?v=WTLPmUHTPqo&ab_channel=TechWithTim
#learning classes and game, all made was done by hand and
#checked by video

#start
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")
# Proxima Centauri
RED = (255, 0 ,0) # RGV Value
CYAN = (0, 255, 255)
BROWN = (150, 75, 0)
BLUE = (173, 216, 230)
BLUEish = (25, 0, 255)
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont("comicsans", 16)
earth_radius = 6378
def mathe():
    luminosity = .0017
    rinner = np.sqrt(luminosity/1.1)
    router = np.sqrt(luminosity/.53)
class Planet:
    AU = (149.6e6 * 1000)
    G = 6.67e-11
    SCALE = 250/AU 
    TIME = 3600*24 # 1 full day
    EARTH_MASS = 5.9742e24
    
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color= color
        #mass in kg
        self.mass = mass
        self.orbit= []
        self.trappist1 = False
        self.distance_to_trappist1 = 0
        
        
        self.x_vel = 0
        self.y_vel = 0
    def draw(self, win):
        x=self.x * self.SCALE + WIDTH/2 #(0,0) is top left adding width centers it
        
        y=self.y * self.SCALE + WIDTH/2
        if len(self.orbit) > 2:
            updated_points=[]
            for point in self.orbit:
                x, y = point
            
                x = x*self.SCALE + WIDTH /2
                y = y*self.SCALE + HEIGHT/2
                updated_points.append((x,y))
            pygame.draw.lines(win, self.color, False,updated_points, 2)
        pygame.draw.circle(win, self.color, (x,y), self.radius)
        if not self.trappist1:
            distance_text = FONT.render(f"{round(self.distance_to_trappist1/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        if other.trappist1:
            self.distance_to_trappist1 = distance
                        #if the other thing we are trying to calculate
                      #is the star, we just calculate distance to the star
                      #we update it so we can use it to drawn the distance
                      #of the star  to the planet
            
            
        force = self.G * self.mass * other.mass / distance**2 #F = GMm/r^2
        angle = math.atan2(distance_y, distance_x)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        #found equation by simple manipulation, will state in paper
        return force_x, force_y
    def update_position(self,planets):
        #getting all forces from all planets but itself
        
        total_fx = total_fy = 0
        
        for planet in planets:
            if self == planet:
                continue
                
                #dont want to calculate force with self 
                #(will get 0 error as distance would be r**2 = 0)
                
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIME
        self.y_vel += total_fy / self.mass * self.TIME
        self.x += .5*self.x_vel * self.TIME
        self.y += .5*self.y_vel * self.TIME
        #append the position to draw to orbit
       
        self.orbit.append((self.x, self.y))
def window():
    #creates the pygame window
    #credit to https://www.youtube.com/watch?v=WTLPmUHTPqo&ab_channel=TechWithTim
    
    run = True
    #Increase frames
    clock = pygame.time.Clock()
    #https://exoplanets.nasa.gov/exoplanet-catalog/5500/trappist-1-b/
    trappist1 = Planet(0,0, 20, RED, 1.77e29)
    trappist1.trappist1 = True
    #each planet being added to the game
    trappistb = Planet(-.01154*Planet.AU, 0, 7.1, CYAN, 1.374*Planet.EARTH_MASS)
    trappistb.y_vel = 1636.118 * 1000
    trappistc = Planet(.0158*Planet.AU, 0, 6.5, BROWN, 1.308*Planet.EARTH_MASS)
    trappistc.y_vel = -1412.961 * 1000
    trappistd = Planet(-.02227*Planet.AU, 0, 3.9, BLUE, .708*Planet.EARTH_MASS)
    trappistd.y_vel = 1178.112* 1000
    trappiste = Planet(.02925*Planet.AU, 0, 5.3, BLUEish, .692*Planet.EARTH_MASS)
    trappiste.y_vel = -1060.151* 1000
    trappistf = Planet(-.03849*Planet.AU, 0, 6.8, BLUE, 1.039*Planet.EARTH_MASS)
    trappistf.y_vel =  957.031 * 1000
    trappistg = Planet(-.04683*Planet.AU, 0, 6.7, BROWN, 1.321*Planet.EARTH_MASS)
    trappistg.y_vel =  -892.260* 1000
    trappisth = Planet(.06189*Planet.AU, 0, 3.5, BROWN, .326*Planet.EARTH_MASS)
    trappisth.y_vel = -768.382* 1000

    
    planets = [trappist1, trappistb, trappistc, trappistd, trappiste, 
               trappistf, trappistg, trappisth]
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update()
        #60 represents number of frames
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.draw(WIN)
        pygame.display.update()
    pygame.quit()
window()