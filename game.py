import random
import time
from tkinter import *
from CanvasPlus import CanvasPlus
from sprites import *
from rect import *
from spawner import EnemySpawner
import logging

sprite_colors = ['red', 'green', 'blue', 'yellow', 'brown', 'pink', 'cyan', 'magenta', 'black']


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Фігуратор")
        self.tk.wm_attributes('-topmost', True)
        self.tk.wm_attributes('-fullscreen', True)
        window_width = self.tk.winfo_screenwidth()
        window_height = self.tk.winfo_screenheight()
        self.canvas = CanvasPlus(self.tk, width=window_width, height=window_height, background="white")
        self.canvas.pack()

        self.screen = BoundingRect(0, 0, window_width, window_height)
        self.player = PlayerSprite(self.canvas)
        self.enemies = []
        self.enemy_spawner = EnemySpawner(
            bounds=BoundingRect(0, 0, window_width, window_height / 4),
            sprite_colors=sprite_colors,
            canvas=self.canvas
        )
        self.enemyMovement = 8.5
        self.enemyRotation = 75
        self.enemySpawnTime = time.time()
        self.running = True

    def run(self):
        while True:
            if self.running:
                # Spawn enemy every second
                if time.time() - self.enemySpawnTime >= 1:
                    logging.debug("Game spawns new enemy")
                    new_enemy = self.enemy_spawner.spawn_enemy()
                    if new_enemy.coords.width != 0 or new_enemy.coords.height != 0:
                        self.enemies.append(new_enemy)

                    # Update timestamp
                    self.enemySpawnTime = time.time()

                # Move enemies around
                logging.debug("Game moving enemies")

                enemiesToDelete = []  # Indices of enemies to delete

                for i in range(len(self.enemies)):
                    enemy = self.enemies[i]

                    logging.debug(f"Moving {i + 1}th enemy of {len(self.enemies)} with id {enemy.id}")

                    # And remove ofscreen ones
                    if not within(enemy.coords, self.screen):
                        enemiesToDelete.append(i)
                        logging.debug(f"Removing enemy with bounds {enemy.coords} and id {enemy.id}")
                        continue

                    enemyMovement = self.enemyMovement * (random.random() + 0.5)
                    logging.debug(f"Moving enemy down by {enemyMovement} pixels")
                    enemy.move(0, enemyMovement)

                    # Move enemy if it is a small polygon or an equiertal circle
                    moveEnemy = \
                        ((isinstance(enemy, Polygon) and enemy.coords.width <= self.screen.height and enemy.coords.height <= self.screen.height)
                         or (isinstance(enemy, Circle) and enemy.coords.width == enemy.coords.height))

                    if moveEnemy:
                        enemyRotation = self.enemyRotation * (random.random() + 0.5)
                        logging.debug(f"Rotating enemy by {enemyRotation} degrees")
                        enemy.rotate(enemyRotation)

                self.enemies = [
                    self.enemies[i] for i in range(len(self.enemies)) if i not in enemiesToDelete
                ]

                self.enemy_spawner.enemies = self.enemies

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()]
)
game = Game()
game.run()
