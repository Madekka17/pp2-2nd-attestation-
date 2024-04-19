from tkinter import *
import random

WIDTH = 700
HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "grey"
FOOD_COLOR = "black"
FOOD_COLOR2 = "green"
BACKGROUND_COLOR = "white"

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for i, (x, y) in enumerate(self.coordinates):
            x = int(x)
            y = int(y)
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        self.spawn_food()

    def spawn_food(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        food_color = random.choice([FOOD_COLOR, FOOD_COLOR2])

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=food_color, tag="food")

    def remove_food(self):
        canvas.delete("food")

# Функция для обновления игрового цикла
def next_turn(snake, food):
    global score

    x, y = snake.coordinates[0]

    # Обновляем координаты головы змеи в зависимости от направления
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # Проверяем съела ли змея еду
    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Если цвет еды зеленый 2 очка
        if canvas.itemcget("food", "fill") == FOOD_COLOR2:
            score += 2
        else:
            score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
        window.after(5000, food.remove_food)
        window.after(2000, food.spawn_food)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

# Функция для изменения направления движения змеи
def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# Функция для проверки столкновений
def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

# Функция для вывода сообщения о завершении игры
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

# Создаем окно приложения
window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()

window.update()

# Центрируем окно на экране
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Привязываем клавиши для управления змеей
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Создаем змею и еду, запускаем игровой цикл
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
