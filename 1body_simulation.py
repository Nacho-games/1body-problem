import math
import pygame # type: ignore
import sys
import time

#inicalizamos todo
pygame.init()
pygame.font.init()
pygame.mixer.init()

# PANTALLA
screen_width = 1400
screen_length = 700
half_width = screen_width / 2
half_length = screen_length / 2
screen = pygame.display.set_mode((screen_width, screen_length))
screen_rect = pygame.Rect(0, 0, screen_width, screen_length)

#counters
change_time = 15

#font 
font_size1 = 25  
font1 = pygame.font.Font("./files//lato.ttf", font_size1)
font_size2 = 70  
font2 = pygame.font.Font("./files//lato.ttf", font_size2)

#simulation
simulation = True

#menu
menu = True

#time
clock = pygame.time.Clock()
fps = 0
seconds_in_day   = 60 * 60 * 24 
dt = 2 * seconds_in_day

#real life values
sun_earth = 1.5 * 10**8 
sun_mars = 2.28 * 10**8
earth_radius = 6.371 * 10**3
sun_radius = 6.96340 * 10**5
mars_radius = 3.3895 * 10**3
earth_mass = 5.9722 * 10**24
sun_mass = 1.989 * 10**30
gravitational_constant = 6.67430 * 10**-20

#draw sizes
earth_draw_radius = 24.886718875 
sun_draw_radius = 99.4771428571
mars_draw_radius = (mars_radius * earth_draw_radius) / earth_radius
earth_draw_size= 2 * earth_draw_radius
sun_draw_size= 2 * sun_draw_radius
mars_draw_size= 2 * mars_draw_radius
sun_earth_draw_distance = 200
sun_mars_draw_distance = (sun_mars * sun_earth_draw_distance) / sun_earth

#ratios
earth_radius_ratio = earth_radius / earth_draw_radius
sun_radius_ratio = sun_radius / sun_draw_radius
mars_radius_ratio = mars_radius / mars_draw_radius
distance_ratio = sun_earth / sun_earth_draw_distance

#velocities (km per day)
#earth
speed_km_s_earth =  math.sqrt((gravitational_constant * sun_mass) / sun_earth)
earth_vel_x      = speed_km_s_earth * seconds_in_day
draw_earth_vel_x = earth_vel_x / distance_ratio
time_ratio       = 2 * 30 / 30 #months per second

#mars
speed_km_s_mars = -math.sqrt((gravitational_constant * sun_mass) / sun_mars)
mars_vel_x      = speed_km_s_mars * seconds_in_day
draw_mars_vel_x = mars_vel_x / distance_ratio

#atrophysical objects
sun_repre   = pygame.Rect(half_width - sun_draw_size / 2, half_length - sun_draw_size / 2, sun_draw_size, sun_draw_size)
earth_repre = pygame.Rect(half_width - earth_draw_size / 2, ((half_length + sun_draw_size / 2) + screen_length) / 2 - earth_draw_size / 2, earth_draw_size, earth_draw_size)
mars_repre  = pygame.Rect(half_width - mars_draw_size / 2, half_length - sun_mars_draw_distance - mars_draw_size / 2, mars_draw_size, mars_draw_size)

#distance
#draw
draw_distance_earth = math.sqrt((earth_repre.centerx - sun_repre.centerx)**2 + (earth_repre.centery -sun_repre.centery)**2)
draw_distance_mars  = math.sqrt((mars_repre.centerx - sun_repre.centerx)**2 + (mars_repre.centery -sun_repre.centery)**2)

#aceleration
earth_accerelation = (gravitational_constant * sun_mass) / sun_earth**2

#velocity
earth_velocity = pygame.math.Vector2(speed_km_s_earth, 0)

#cordinates
earth_x = earth_repre.x * distance_ratio
earth_y = earth_repre.y * distance_ratio
mars_x = mars_repre.x * distance_ratio
mars_y = mars_repre.y * distance_ratio

#vectors
sun_pos   = pygame.math.Vector2(sun_repre.centerx, sun_repre.centery)
earth_pos = pygame.math.Vector2(earth_repre.centerx, earth_repre.centery)
mars_pos = pygame.math.Vector2(mars_repre.centerx, mars_repre.centery)
direction_earth = (sun_pos - earth_pos).normalize()
direction_mars = (sun_pos - mars_pos).normalize()
earth_acceleration = direction_earth * ((gravitational_constant * sun_mass) / (draw_distance_earth * distance_ratio)**2)
mars_acceleration  = direction_mars  * ((gravitational_constant * sun_mass) / (draw_distance_mars * distance_ratio)**2)

#tangents
tangent_earth = direction_earth.rotate(90)
tangent_mars = direction_mars.rotate(-90)
earth_velocity = tangent_earth.normalize() * speed_km_s_earth
mars_velocity  = tangent_mars.normalize() * -speed_km_s_mars

#commments
earth_ratio_comment    = f"Earth ratio: 1-{round(earth_radius_ratio, 1)}"
mars_ratio_comment     = f"Mars ratio: 1-{round(mars_radius_ratio, 1)}"
sun_ratio_comment      = f"Sun ratio: 1-{round(sun_radius_ratio, 1)}"
distance_ratio_comment = f"Distance ratio: 1-{round(distance_ratio)}"
ratio_comment          = "1px = 1km"
time_ratio             = f"Time ratio: 1sec - {round(time_ratio)} months"

#colores
Black = (0, 0, 0)
White = (255, 255, 255)
Gray_Blue = (50, 50, 100)
Gray_Red = (100, 50, 50)
Gray_Green = (50, 100, 50)

#images
earth_i = pygame.image.load("./files/earth.jpg")
earth_adjus = pygame.transform.scale(earth_i,(earth_draw_size, earth_draw_size))
sun_i = pygame.image.load("./files/sun.png")
sun_adjus = pygame.transform.scale(sun_i,(sun_draw_size, sun_draw_size))
mars_i = pygame.image.load("./files/mars.jpg")
mars_adjus = pygame.transform.scale(mars_i,(mars_draw_size, mars_draw_size))
background_i = pygame.image.load("./files/background.jpg")
barckgound_adjus = pygame.transform.scale(background_i,(screen_width, screen_length))
gravitational_accelaration_i = pygame.image.load("./files/gravitational_acceleration.png")
gravitational_acceleration_adjus = pygame.transform.scale(gravitational_accelaration_i,(300, 150))
orbital_velocity_i = pygame.image.load("./files/orbital_velocity.png")
orbital_velocity_adjus = pygame.transform.scale(orbital_velocity_i,(300, 150))
eulers_integration_of_velocity_i = pygame.image.load("./files/eulers_integration_of_velocity.png")
eulers_integration_of_velocity_adjus = pygame.transform.scale(eulers_integration_of_velocity_i,(500, 100))
eulers_integration_of_position_i = pygame.image.load("./files/eulers_integration_of_position.png")
eulers_integration_of_position_adjus = pygame.transform.scale(eulers_integration_of_position_i,(500, 100))
distance_calculation_i = pygame.image.load("./files/distance_calculation.png")
distance_calculation_adjus = pygame.transform.scale(distance_calculation_i,(500, 50))

#start button
start_i = pygame.image.load("./files/start.png")
start_adjus = pygame.transform.scale(start_i,(300, 160))
start_button = pygame.Rect(half_width - 150, 502.5, 300, 160)


#sound
clack = pygame.mixer.Sound('./files/click.mp3')

#formulas rect
gravitational_accelaration_rect = pygame.Rect(half_width - 150, 330, 300, 150)
eulers_velocity_rect = pygame.Rect(0, 325, 500, 100)
eulers_position_rect = pygame.Rect(860, 330, 500, 100)
orbital_vel_rect = pygame.Rect(100, 515, 300, 150)
distance_rect = pygame.Rect(860, 580, 500, 50)


while menu:

    #exit 
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            simulation = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                menu = False
                clack.play()

    if key[pygame.K_ESCAPE]:
        menu = False
        simulation = False
    if key[pygame.K_SPACE] or key[pygame.K_RETURN]:
        menu = False
        clack.play()

    #limpiamos
    screen.fill(((32, 33, 35)))
    

    #text
    title_txt = font2.render(str(f"1 Body Problem"), True, White)
    title_txt_rect = title_txt.get_rect(center=(half_width, 50 ))
    subtitle_txt = font1.render(str(f"This simulation simulates the 1 body problem with the Earth and Mars"), True, White)
    subtitle_txt_rect = subtitle_txt.get_rect(center=(half_width, 130 ))
    subtitle2_txt = font1.render(str(f"All calculations are done with the real distances, "), True, White)
    subtitle2_txt_rect = subtitle2_txt.get_rect(center=(half_width, 170 ))
    subtitle3_txt = font1.render(str(f"I calculated the orbital speed of Earth to be around {round(speed_km_s_earth, 1)}km/s and Mars orbital speed to be around {round(-speed_km_s_mars, 1)}km/s"), True, White)
    subtitle3_txt_rect = subtitle3_txt.get_rect(center=(half_width, 210 ))
    subtitle4_txt = font1.render(str(f" I used the following equations for calculating the orbits:"), True, White)
    subtitle4_txt_rect = subtitle4_txt.get_rect(center=(half_width, 250 ))
    gravi_txt = font1.render(str(f" Gravitational Acceleration:"), True, White)
    gravi_txt_rect = gravi_txt.get_rect(center=(half_width, 315 ))
    euler_vel_txt = font1.render(str(f" Euler's Integration of Velocity:"), True, White)
    eurler_vel_txt_rect = euler_vel_txt.get_rect(center=(250, 325 ))
    euler_pos_txt = font1.render(str(f" Euler's Integration of Position:"), True, White)
    euler_pos_txt_rect = euler_pos_txt.get_rect(center=(1110, 325 ))
    orbital_txt = font1.render(str(f" Orbital Velocity for a Circular Orbit:"), True, White)
    orbiatl_txt_rect = orbital_txt.get_rect(center=(250, 490 ))
    distance_txt = font1.render(str(f"Distance for Cartesian Coordinates:"), True, White)
    distance_txt_rect = distance_txt.get_rect(center=(1110, 540 ))


    #pintamos
    screen.blit(title_txt, title_txt_rect)
    screen.blit(subtitle_txt, subtitle_txt_rect)
    screen.blit(subtitle2_txt, subtitle2_txt_rect)
    screen.blit(subtitle3_txt, subtitle3_txt_rect)
    screen.blit(subtitle4_txt, subtitle4_txt_rect)
    screen.blit(gravi_txt, gravi_txt_rect) 
    screen.blit(start_adjus, start_button )
    screen.blit(gravitational_acceleration_adjus, gravitational_accelaration_rect)
    screen.blit(eulers_integration_of_velocity_adjus, eulers_velocity_rect)
    screen.blit(eulers_integration_of_position_adjus, eulers_position_rect)
    screen.blit(orbital_velocity_adjus, orbital_vel_rect)
    screen.blit(distance_calculation_adjus, distance_rect)
    screen.blit(euler_vel_txt, eurler_vel_txt_rect)
    screen.blit(euler_pos_txt, euler_pos_txt_rect)
    screen.blit(orbital_txt, orbiatl_txt_rect)
    screen.blit(distance_txt, distance_txt_rect)


    pygame.display.update()



#simulation
while simulation:

    #exit 
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulation = False

    if key[pygame.K_ESCAPE]:
        simulation = False
    

    if change_time > 29:
        fps = clock.get_fps()
        fps = round(fps)
        change_time = 0
    change_time += 1    


    #changing comments
    earth_pos_comment = f"Earth x: {round(earth_repre.x, 1)}, y: {screen_length - (round(earth_repre.y, 1))}"
    mars_pos_comment = f"Mars x: {round(mars_repre.x, 1)}, y: {screen_length - (round(mars_repre.y, 1))}"

    #text
    fps_txt = font1.render(str(f"Frame rate: {fps}"), True, White)
    fps_txt_rect = fps_txt.get_rect(center=(1280, 25))

    earth_ratio_txt = font1.render(earth_ratio_comment, True, White)
    earth_ratio_txt_rect = earth_ratio_txt.get_rect(center=(117, 25 ))
    mars_ratio_txt = font1.render(mars_ratio_comment, True, White)
    mars_ratio_txt_rect = mars_ratio_txt.get_rect(center=(115, 60 ))
    sun_ratio_txt = font1.render(sun_ratio_comment, True, White)
    sun_ratio_txt_rect = sun_ratio_txt.get_rect(center=(115, 95 ))
    distance_ratio_txt = font1.render(distance_ratio_comment, True, White)
    distance_ratio_txt_rect = distance_ratio_txt.get_rect(center=(148, 130 ))
    ratio_txt = font1.render(ratio_comment, True, White)
    ratio_txt_rect = ratio_txt.get_rect(center=(65, 165 ))
    time_ratio_txt = font1.render(time_ratio, True, White)
    time_ratio_txt_rect = time_ratio_txt.get_rect(center=(152, 220 ))
    earth_pos_txt = font1.render(earth_pos_comment, True, White)
    earth_pos_txt_rect = earth_pos_txt.get_rect(center=(115, 630 ))
    mars_pos_txt = font1.render(mars_pos_comment, True, White)
    mars_pos_txt_rect = mars_pos_txt.get_rect(center=(115, 665 ))


    #astronomical movement
    earth_velocity += earth_acceleration * dt
    earth_x += earth_velocity.x * dt
    earth_y += earth_velocity.y * dt

    mars_velocity += mars_acceleration * dt
    mars_x += mars_velocity.x * dt
    mars_y += mars_velocity.y * dt


    #aceleration
    real_distance_earth = math.sqrt((earth_x - sun_pos.x*distance_ratio)**2 + (earth_y - sun_pos.y*distance_ratio)**2)
    earth_pos = pygame.math.Vector2(earth_x / distance_ratio, earth_y / distance_ratio)
    direction_earth = (sun_pos - earth_pos).normalize()
    earth_acceleration = direction_earth * ((gravitational_constant * sun_mass) / real_distance_earth**2)

    real_distance_mars = math.sqrt((mars_x - sun_pos.x*distance_ratio)**2 + (mars_y - sun_pos.y*distance_ratio)**2)
    mars_pos = pygame.math.Vector2(mars_x / distance_ratio, mars_y / distance_ratio)
    direction_mars = (sun_pos - mars_pos).normalize()
    mars_acceleration = direction_mars * ((gravitational_constant * sun_mass) / real_distance_mars**2)

    #actualizamos
    earth_repre.x = earth_x / distance_ratio
    earth_repre.y = earth_y / distance_ratio
    mars_repre.x = mars_x / distance_ratio
    mars_repre.y = mars_y / distance_ratio

    #limpiamos
    screen.fill(Black)
    screen.blit(barckgound_adjus, screen_rect)

    #pintamos 
    screen.blit(earth_adjus, earth_repre)
    screen.blit(sun_adjus, sun_repre)
    screen.blit(mars_adjus, mars_repre)

    #pintamos text
    pygame.draw.rect(screen, Gray_Blue, (0, 0, 307, 245))
    pygame.draw.rect(screen, Gray_Red, (0, 605, 240, 95))
    pygame.draw.rect(screen, Gray_Green, (1190, 0, 310, 50))
    screen.blit(fps_txt, fps_txt_rect)
    screen.blit(earth_ratio_txt, earth_ratio_txt_rect)
    screen.blit(mars_ratio_txt, mars_ratio_txt_rect)
    screen.blit(sun_ratio_txt, sun_ratio_txt_rect)
    screen.blit(distance_ratio_txt, distance_ratio_txt_rect)
    screen.blit(ratio_txt, ratio_txt_rect)
    screen.blit(time_ratio_txt, time_ratio_txt_rect)
    screen.blit(earth_pos_txt, earth_pos_txt_rect)
    screen.blit(mars_pos_txt, mars_pos_txt_rect)

    #actualizamos
    pygame.display.update()
    
    #fps
    clock.tick(30)


pygame.quit()
sys.exit()