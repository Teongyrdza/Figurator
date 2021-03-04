import random
import time
from tkinter import *
from CanvasPlus import CanvasPlus
from sprites import *
from rect import *
from spawner import EnemySpawner
import logging
import platform

sprite_colors = ['red', 'green', 'blue', 'yellow', 'brown', 'pink', 'cyan', 'magenta', 'black']


def random_double(start, stop):
    return start + random.random() * stop


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Фігуратор")
        self.tk.wm_attributes('-topmost', True)
        self.tk.wm_attributes('-fullscreen', True)
        self.window_width = self.tk.winfo_screenwidth()
        self.window_height = self.tk.winfo_screenheight()
        self.canvas = CanvasPlus(self.tk, width=self.window_width, height=self.window_height, background="white")
        self.canvas.pack()

        self.screen = BoundingRect(0, 0, self.window_width, self.window_height)
        self.player = PlayerSprite(self.canvas)
        self.playerLives = None
        self.enemies = None
        self.enemy_spawner = EnemySpawner(
            bounds=BoundingRect(0, 0, self.window_width, self.window_height / 4),
            sprite_colors=sprite_colors,
            canvas=self.canvas
        )
        self.enemyMovement = 8.5
        self.enemyRotation = 75
        self.rotationDict = None  # A dict to hold will each enemy rotate
        self.timeouts = None  # Timeouts for every sprite, if any
        self.timeout = 10
        self.enemySpawnTime = None
        self.running = False
        self.reset()

    def run(self):
        previous_update = time.time()

        while True:
            if self.running:
                now = time.time()
                elapsed = now - previous_update
                previous_update = now
                expected = 1 / 60  # Expected update time in seconds
                ratio = elapsed / expected  # Update timestep
                logging.debug(f"{elapsed:.2f} seconds elapsed from the last update, the expected is {expected: .2f}")
                logging.debug(f"The ratio is {ratio: .2f}")

                # Spawn enemy every second
                if time.time() - self.enemySpawnTime >= 1:
                    logging.debug("Game spawns new enemy")
                    new_enemy = self.enemy_spawner.spawn_enemy()
                    if new_enemy.coords.width != 0 or new_enemy.coords.height != 0:
                        self.enemies.append(new_enemy)
                        self.rotationDict[new_enemy.id] = bool(random.randint(0, 1))  # Select rotated sprites randomly
                        self.timeouts[new_enemy.id] = 0  # The enemy is in the game by default

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

                    enemyMovement = self.enemyMovement * random_double(0.5, 1.5) * ratio
                    logging.debug(f"Moving enemy down by {enemyMovement: .2f} pixels")
                    enemy.move(0, enemyMovement)

                    # Move enemy if it is a small polygon or an equiertal circle
                    rotateEnemy = \
                        ((isinstance(enemy,
                                     Polygon) and enemy.coords.width <= self.screen.height and enemy.coords.height <= self.screen.height)
                         or (isinstance(enemy, Circle) and enemy.coords.width == enemy.coords.height)) and \
                        self.rotationDict[enemy.id]

                    if rotateEnemy:
                        enemyRotation = self.enemyRotation * random_double(0.5, 1.5) * ratio
                        logging.debug(f"Rotating enemy by {enemyRotation: .2f} degrees")
                        enemy.rotate(enemyRotation)

                # Delete ofscreen enemies
                self.enemies = [
                    self.enemies[i] for i in range(len(self.enemies)) if i not in enemiesToDelete
                ]

                # Check for game over
                for enemy in self.enemies:
                    if self.timeouts[enemy.id] == 0:  # Enemy in game
                        if collided(enemy, self.player):
                            self.playerLives -= 1
                            self.timeouts[enemy.id] = self.timeout  # This enemy takes a break
                    else:
                        self.timeouts[enemy.id] -= elapsed if elapsed < self.timeout else expected
                    if self.playerLives == 0:
                        self.gameOver()

                self.enemy_spawner.enemies = self.enemies  # Update spawner enemies

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

    def gameOver(self):
        def resume_game():
            nonlocal self, gameover_text, resume_button
            self.canvas.delete(gameover_text)
            resume_button.destroy()

            self.reset()

        logging.debug("Game over!")

        self.running = False

        # Create game over text
        text_x, text_y = self.window_width / 2, self.window_height / 2
        gameover_text = self.canvas.create_text(text_x, text_y, fill="black", font="System 40", text="Game Over!")

        # Create resume button
        if platform.system() == "Darwin":
            resume_button = Button(
                self.canvas,
                text="Click to resume",
                font="System 20",
                highlightbackground="red",
                highlightthickness=15,
                fg="black",
                relief=FLAT,
                bd=0,
                command=resume_game
            )
            resume_button.place(x=text_x + 2, y=text_y + 55, anchor=CENTER)
        else:
            resume_button = Button(
                self.canvas,
                text="Click to resume",
                font="System 20",
                bg="red",
                fg="black",
                relief=FLAT,
                bd=0,
                command=resume_game
            )
            resume_button.place(x=text_x + 2, y=text_y + 40, anchor=CENTER)

    def reset(self):
        logging.debug("Game is reset")

        self.playerLives = 5
        self.enemies = []
        self.rotationDict = {}
        self.timeouts = {}
        self.enemySpawnTime = time.time()
        self.running = True


logging.basicConfig(
    level=logging.DEBUG,
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()]
)
game = Game()
game.run()
