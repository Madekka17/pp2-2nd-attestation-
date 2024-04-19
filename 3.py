import pygame
pygame.init()

fps = 60
timer = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
active_size = 0
active_color = 'white'
eraser_color = 'white'
drawing_mode = 'circle'
painting = []

# Создаем экран Pygame
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Paint!')

# Функция для отрисовки меню
def draw_menu(size, color, mode):
    pygame.draw.rect(screen, 'grey', [0, 0, WIDTH, 70])  # Отрисовываем фон меню
    pygame.draw.line(screen, 'black', (0, 70), (WIDTH, 70), 3)  # Отрисовываем черную линию над меню

    # Отрисовываем кисти 2 размеров
    xl_brush = pygame.draw.rect(screen, 'black', [10, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (35, 35), 20)
    l_brush = pygame.draw.rect(screen, 'black', [70, 10, 50, 50])
    pygame.draw.circle(screen, 'white', (95, 35), 15)
    brush_list = [xl_brush, l_brush]

    blue = pygame.draw.rect(screen, (0, 0, 255), [WIDTH - 35, 10, 25, 25])
    red = pygame.draw.rect(screen, (255, 0, 0), [WIDTH - 35, 35, 25, 25])
    green = pygame.draw.rect(screen, (0, 255, 0), [WIDTH - 60, 10, 25, 25])
    yellow = pygame.draw.rect(screen, (255, 255, 0), [WIDTH - 60, 35, 25, 25])
    eraser = pygame.draw.rect(screen, eraser_color, [WIDTH - 90, 10, 25, 25])
    color_rect = [blue, red, green, yellow, eraser]
    rgb_list = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), 'eraser']

    # Отрисовываем кнопки выбора режима рисования: круг, прямоугольник, треугольник, ромб
    if mode == 'circle':
        pygame.draw.rect(screen, 'lightgray', [200, 10, 80, 50])
    pygame.draw.rect(screen, 'black', [200, 10, 80, 50], 3)
    pygame.draw.circle(screen, 'black', (240, 35), 20)

    if mode == 'rectangle':
        pygame.draw.rect(screen, 'lightgray', [300, 10, 80, 50])
    pygame.draw.rect(screen, 'black', [300, 10, 80, 50], 3)
    pygame.draw.rect(screen, 'black', [310, 20, 60, 30])

    if mode == 'triangle':
        pygame.draw.rect(screen, 'lightgray', [400, 10, 80, 50])
    pygame.draw.rect(screen, 'black', [400, 10, 80, 50], 3)
    pygame.draw.polygon(screen, 'black', [(440, 20), (420, 60), (460, 60)])

    if mode == 'rhombus':
        pygame.draw.rect(screen, 'lightgray', [500, 10, 80, 50])
    pygame.draw.rect(screen, 'black', [500, 10, 80, 50], 3)
    pygame.draw.polygon(screen, 'black', [(540, 20), (520, 35), (540, 50), (560, 35)])

    return brush_list, color_rect, rgb_list

# Функция для отрисовки всех элементов рисунка
def draw_painting(paints):
    for paint in paints:
        if paint[0] == 'rectangle':
            pygame.draw.rect(screen, paint[1], paint[2])
        elif paint[0] == 'circle':
            pygame.draw.circle(screen, paint[1], paint[2], paint[3])
        elif paint[0] == 'triangle' or paint[0] == 'rhombus':
            pygame.draw.polygon(screen, paint[1], paint[2])

# Основной игровой цикл
run = True
while run:
    timer.tick(fps)

    screen.fill('white')

    mouse = pygame.mouse.get_pos() 
    left_click = pygame.mouse.get_pressed()[0] 

    # Если левая кнопка мыши нажата и позиция мыши находится в пределах холста
    if left_click and mouse[1] > 70:
        if drawing_mode == 'circle':
            color_to_use = eraser_color if pygame.mouse.get_pressed()[2] else active_color
            painting.append(('circle', color_to_use, mouse, active_size))
        elif drawing_mode == 'rectangle':
            painting.append(('rectangle', active_color, pygame.Rect(mouse[0] - active_size, mouse[1] - active_size, active_size * 2, active_size * 2)))
        elif drawing_mode == 'triangle':
            painting.append(mouse)
            if len(painting) == 3:
                painting.append((drawing_mode, active_color, [(mouse[0], mouse[1] - active_size), (mouse[0] - active_size, mouse[1] + active_size), (mouse[0] + active_size, mouse[1] + active_size)]))
                painting.clear()
        elif drawing_mode == 'rhombus':
            painting.append(mouse)
            if len(painting) == 2:
                painting.append((drawing_mode, active_color, [(mouse[0], mouse[1] - active_size), (mouse[0] - active_size, mouse[1]), (mouse[0], mouse[1] + active_size), (mouse[0] + active_size, mouse[1])]))
                painting.clear()

    draw_painting(painting)  # Отрисовываем все элементы рисунка

    # Отрисовываем меню
    brushes, colors, rgbs = draw_menu(active_size, active_color, drawing_mode)

    # Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если произошло событие выхода из игры
            run = False  # Завершаем игровой цикл
        
        if event.type == pygame.MOUSEBUTTONDOWN:  # Если произошло событие нажатия кнопки мыши
            mouse_pos = pygame.mouse.get_pos()
            # Проверяем, на какие элементы меню было произведено нажатие
            for i in range(len(brushes)):
                if brushes[i].collidepoint(mouse_pos):
                    active_size = 20 - (i * 5)
            for i in range(len(colors)):
                if colors[i].collidepoint(mouse_pos):
                    mode_or_color = rgbs[i]
                    if mode_or_color == 'rectangle' and drawing_mode != 'rectangle':
                        drawing_mode = 'rectangle'
                    elif mode_or_color == 'circle' and drawing_mode != 'circle':
                        drawing_mode = 'circle'
                    elif mode_or_color == 'triangle' and drawing_mode != 'triangle':
                        drawing_mode = 'triangle'
                    elif mode_or_color == 'rhombus' and drawing_mode != 'rhombus':
                        drawing_mode = 'rhombus'
                    else:
                        active_color = mode_or_color

            # Переключаем режим рисования по клику на соответствующие кнопки
            if 200 < mouse_pos[0] < 280 and 10 < mouse_pos[1] < 60:
                drawing_mode = 'circle'
            elif 300 < mouse_pos[0] < 380 and 10 < mouse_pos[1] < 60:
                drawing_mode = 'rectangle'
            elif 400 < mouse_pos[0] < 480 and 10 < mouse_pos[1] < 60:
                drawing_mode = 'triangle'
            elif 500 < mouse_pos[0] < 580 and 10 < mouse_pos[1] < 60:
                drawing_mode = 'rhombus'

    pygame.display.flip()  # Обновляем экран

pygame.quit()  # Завершаем Pygame
