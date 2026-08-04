PADDLE_SPRITE = "31-Breakout-Tiles.png"
BALL_SPRITE = "58-Breakout-Tiles.png"

import pygame
import sys
import xml.etree.ElementTree as ET


class Game:

    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT)
        )
        pygame.display.set_caption("Brick Game")

        self.load_assets()

        self.initialize_game()

        self.clock = pygame.time.Clock()

        self.running = True

    def load_assets(self):
        self.sprite_sheet = pygame.image.load("assets/Breakout_Tile_Free.png").convert_alpha()
        self.sprites = {}
        self.load_sprites()

    def initialize_game(self):

        # ------------------
        # GAME STATE
        # ------------------

        self.score = 0
        self.level = 1
        self.lives = 3

        # ------------------
        # PADDLE
        # ------------------

        self.paddle = self.get_sprite_by_name(
            "56-Breakout-Tiles.png"
        )

        self.paddle = pygame.transform.scale(
            self.paddle,
            (120, 30)
        )

        self.paddle_x = (
            self.WIDTH - self.paddle.get_width()
        ) // 2

        self.paddle_y = self.HEIGHT - 80

        self.paddle_speed = 8

        # ------------------
        # BALL
        # ------------------

        self.ball = self.get_sprite_by_name(
            "58-Breakout-Tiles.png"
        )

        self.ball = pygame.transform.scale(
            self.ball,
            (24, 24)
        )

        self.ball_x = (
            self.WIDTH - self.ball.get_width()
        ) // 2

        self.ball_y = self.paddle_y - 40

        self.ball_dx = 5
        self.ball_dy = -5

        # ------------------
        # BRICKS
        # ------------------

        self.bricks = []

        self.create_level_1()

    def update_ball(self):

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        # Left wall
        if self.ball_x <= 0:
            self.ball_dx *= -1

        # Right wall
        if self.ball_x >= self.WIDTH - self.ball.get_width():
            self.ball_dx *= -1

        # Top wall
        if self.ball_y <= 0:
            self.ball_dy *= -1

    def get_sprite(self, x, y, width, height):
        rect = pygame.Rect(
            x,
            y,
            width,
            height
        )
        return self.sprite_sheet.subsurface(rect)

    def load_sprites(self):

        tree = ET.parse(
            "assets/Breakout_Tile_Free.xml"
        )

        root = tree.getroot()

        for sprite in root.findall("SubTexture"):

            name = sprite.attrib["name"]

            x = int(sprite.attrib["x"])
            y = int(sprite.attrib["y"])

            width = int(sprite.attrib["width"])
            height = int(sprite.attrib["height"])

            image = self.get_sprite(
                x,
                y,
                width,
                height
            )

            self.sprites[name] = image
            print(len(self.sprites))

    def get_sprite_by_name(self, name):
        if name not in self.sprites:
            raise ValueError(
                f"Sprite '{name}' was not found."
            )
        return self.sprites[name]

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.paddle_x -= self.paddle_speed

        if keys[pygame.K_RIGHT]:
            self.paddle_x += self.paddle_speed


        if self.paddle_x < 0:
            self.paddle_x = 0

        if self.paddle_x > self.WIDTH - self.paddle.get_width():
            self.paddle_x = (
                self.WIDTH -
                self.paddle.get_width()
            )
        self.update_ball()


    def create_level_1(self):

        self.bricks.clear()
        colors = [
        "02-Breakout-Tiles.png",
        "03-Breakout-Tiles.png",
        "04-Breakout-Tiles.png",
        "05-Breakout-Tiles.png",
        "06-Breakout-Tiles.png"
    ]
        start_x = 50
        start_y = 100

        rows = 5
        cols = 10

        spacing_x = 8
        spacing_y = 8

        brick_width = 80
        brick_height = 30

        for row in range(rows):

            sprite = colors[row]

            for col in range(cols):

                x = start_x + col * (brick_width + spacing_x)
                y = start_y + row * (brick_height + spacing_y)

                brick = self.create_brick(
                    sprite,
                    x,
                    y
                )

                self.bricks.append(brick)

    


    def create_brick(self, sprite_name, x, y):

        sprite = self.get_sprite_by_name(sprite_name)

        sprite = pygame.transform.scale(
            sprite,
            (80, 30)
        )

        return {
            "sprite": sprite,
            "rect": pygame.Rect(x, y, 80, 30),
            "alive": True
        }

    def draw(self):

        self.screen.fill((0, 0, 0))

        # Draw bricks
        for brick in self.bricks:
            if brick["alive"]:
                self.screen.blit(
                    brick["sprite"],
                    brick["rect"]
                )

        # Draw paddle
        self.screen.blit(
            self.paddle,
            (self.paddle_x, self.paddle_y)
        )

        # Draw ball
        self.screen.blit(
            self.ball,
            (self.ball_x, self.ball_y)
        )

        pygame.display.flip()

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


game = Game()
game.run()