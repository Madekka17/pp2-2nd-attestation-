import pygame
import datetime

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
mouse = pygame.image.load('mainclock.png')
leftarm = pygame.image.load('leftarm.png')
rightarm = pygame.image.load('rightarm.png')
mouse = pygame.transform.scale(mouse, (500, 400))
hscalefactor = 0.5
leftarm = pygame.transform.scale(leftarm, (float(leftarm.get_width() * hscalefactor), float(leftarm.get_height() * hscalefactor)))
rightarm = pygame.transform.scale(rightarm, (float(rightarm.get_width() * hscalefactor), float(rightarm.get_height() * hscalefactor)))
done = True
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    current_time = datetime.datetime.now()
    minute_angle = -6 * ((current_time.minute + current_time.second / 60) * 6)
    second_angle = -6 * current_time.second

    rlarm = pygame.transform.rotate(leftarm, minute_angle)
    rrarm = pygame.transform.rotate(rightarm, second_angle)
    done = True
    screen.blit(mouse, mouse.get_rect(center=screen.get_rect().center))
    screen.blit(rlarm, rlarm.get_rect(center=screen.get_rect().center))
    screen.blit(rrarm, rrarm.get_rect(center=screen.get_rect().center))

    pygame.display.flip()

    clock.tick(120)
pygame.quit()