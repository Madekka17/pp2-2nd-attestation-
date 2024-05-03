import psycopg2
import pygame
import random
import time
from config import host, user, password, db_name, port

# Initialize Pygame
pygame.init()

# Set up the display
screen_x, screen_y = 600, 400
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Snake Game")

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# Game settings
snake_speed = 15
fps = pygame.time.Clock()

# Snake settings
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
direction = 'RIGHT'
change_to = direction

# Fruit settings
fruit_position = [random.randrange(1, (screen_x//10)) * 10,
                  random.randrange(1, (screen_y//10)) * 10]
fruit_spawn = True

# Score
score = 0

# Database connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None

def create_tables():
    conn = connect_to_db()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    level INTEGER NOT NULL DEFAULT 1
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_score (
                    score_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                );
            """)
            conn.commit()
        conn.close()

def get_username():
    username = input("Please enter your username: ")
    conn = connect_to_db()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, level FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                print(f"Welcome back {username}, you are on level {user[1]}")
                return username, user[1]
            else:
                cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id, level", (username,))
                user_id, level = cursor.fetchone()
                conn.commit()
                print(f"Welcome {username}, starting at level 1.")
                return username, level
        conn.close()
    else:
        return None, 1  # Default to level 1 if DB connection fails

def game_loop(username, level):
    global direction, change_to, snake_position, fruit_position, fruit_spawn, score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        # Game dynamics
        direction = change_to
        snake_position[0] += 10 if direction == 'RIGHT' else -10 if direction == 'LEFT' else 0
        snake_position[1] += 10 if direction == 'DOWN' else -10 if direction == 'UP' else 0

        snake_body.insert(0, list(snake_position))
        if snake_position == fruit_position:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (screen_x//10)) * 10,
                              random.randrange(1, (screen_y//10)) * 10]
            fruit_spawn = True

        screen.fill(black)
        for pos in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] >= screen_x or \
           snake_position[1] < 0 or snake_position[1] >= screen_y or \
           any(block == snake_position for block in snake_body[1:]):
            pygame.quit()
            quit()

        pygame.display.flip()
        fps.tick(snake_speed)

def main():
    create_tables()
    username, level = get_username()
    game_loop(username, level)

if __name__ == "__main__":
    main()
