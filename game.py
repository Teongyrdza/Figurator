import random
import time
from tkinter import *
from sprites import *
from rect import *
from spawner import EnemySpawner
import logging

sprite_colors = ['red', 'green', 'blue', 'yellow', 'brown', 'pink', 'cyan', 'magenta', 'black']
image_width = 1435
image_height = 765


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Фігуратор")
        self.tk.wm_attributes('-topmost', 1)
        self.canvas = Canvas(self.tk, width=image_width, height=image_height)
        self.canvas.pack()

        self.enemy_spawner = EnemySpawner(BoundingRect(0, 0, 700, 300), sprite_colors, canvas=self.canvas)
        self.player = PlayerSprite(self.canvas)
        self.enemies = []
        self.running = True
        self.enemySpawnTime = time.time()

    def run(self):

        global image_width, image_height
        while True:
            if self.running:
                # Spawn enemy every second
                if time.time() - self.enemySpawnTime >= 1:
                    new_enemy = self.enemy_spawner.spawn_enemy()
                    if new_enemy.coords.width != 0 and new_enemy.coords.height != 0:
                        self.enemies.append(new_enemy)

                    # Update timestamp
                    self.enemySpawnTime = time.time()

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


logging.basicConfig(level=logging.DEBUG)
game = Game()
game.run()
