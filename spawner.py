from sprites import *
from rect import *
from tkinter import Canvas
import random
import logging


def randrange(start, stop=None, step=1):
    if start == 0 and not stop:
        return 0
    if (stop - start) == 0:
        return stop
    return random.randrange(start, stop, step)


class EnemySpawner:
    """The enemy spawner class."""

    @staticmethod
    def surrounding_boxes(taken_box: BoundingRect, bounds: BoundingRect) -> list[BoundingRect]:
        surrounding_boxes = []

        top_box = BoundingRect(bounds.x1, bounds.y1, bounds.x2, taken_box.y1)
        if top_box.width != 0 and top_box.height != 0:
            surrounding_boxes.append(top_box)

        left_box = BoundingRect(bounds.x1, bounds.y1, taken_box.x1, bounds.y2)
        if left_box.width != 0 and left_box.height != 0:
            surrounding_boxes.append(left_box)

        bottom_box = BoundingRect(bounds.x1, taken_box.y2, bounds.x2, bounds.y2)
        if bottom_box.width != 0 and bottom_box.height != 0:
            surrounding_boxes.append(bottom_box)

        right_box = BoundingRect(taken_box.x2, bounds.y1, bounds.x2, bounds.y2)
        if right_box.width != 0 and right_box.height != 0:
            surrounding_boxes.append(right_box)

        return surrounding_boxes

    @classmethod
    def free_box(cls, searched_boxes: list[BoundingRect], search_bounds: BoundingRect) -> BoundingRect:
        """Calculate free box for new enemy in given bounds."""

        logging.debug(f"free_box(searched_boxes={searched_boxes}, search_bounds={search_bounds})")

        if not searched_boxes:
            return search_bounds

        first_box = searched_boxes[0]
        surrounding_boxes = EnemySpawner.surrounding_boxes(first_box, bounds=search_bounds)
        box_count = len(surrounding_boxes)
        box_index = random.randrange(box_count)
        for i in range(box_count):
            if i == box_index:
                new_bounds = surrounding_boxes[i]
                new_boxes = [
                    box if new_bounds.contains(box) else box.chopped(bounds=new_bounds)
                    for box in searched_boxes if within(new_bounds, box)
                ]
                return cls.free_box(searched_boxes=new_boxes, search_bounds=new_bounds)

        return BoundingRect(0, 0, 0, 0)

    def random_triangle(self, bounds, color):
        logging.debug("random_triangle()")

        minX = bounds.x1
        maxX = bounds.x2
        minY = bounds.y1
        maxY = bounds.y2

        x1 = randrange(minX, maxX)
        logging.debug(f"x1: {x1}")
        assert minX <= x1 <= maxX

        y1 = randrange(minY, maxY)
        logging.debug(f"y1: {y1}")
        assert minY <= y1 <= maxY

        x2 = randrange(minX, x1)
        logging.debug(f"x2: {x2}")
        assert minX <= x2 <= maxX

        y2 = randrange(y1, maxY)
        logging.debug(f"y2: {y2}")
        assert minY <= y2 <= maxY

        x3 = randrange(x1, maxX)
        logging.debug(f"x3: {x3}")
        assert minX <= x3 <= maxX

        y3 = randrange(y1, maxY)
        logging.debug(f"y3: {y3}")
        assert minY <= y3 <= maxY

        return Triangle(self.canvas, x1, y1, x2, y2, x3, y3, color=color)

    def random_rectangle(self, bounds, color):
        logging.debug("random_rectangle()")

        minX = bounds.x1
        maxX = bounds.x2
        minY = bounds.y1
        maxY = bounds.y2

        x1 = randrange(minX, maxX)
        logging.debug(f"x1: {x1}")
        assert minX <= x1 <= maxX

        y1 = randrange(minY, maxY)
        logging.debug(f"y1: {y1}")
        assert minY <= y1 <= maxY

        x2 = randrange(x1, maxX)
        logging.debug(f"x2: {x2}")
        assert minX <= x2 <= maxX

        y2 = randrange(y1, maxY)
        logging.debug(f"y2: {y2}")
        assert minY <= y2 <= maxY

        x3 = randrange(x2, maxX)
        logging.debug(f"x3: {x3}")
        assert minX <= x3 <= maxX

        y3 = randrange(y1, maxY)
        logging.debug(f"y3: {y3}")
        assert minY <= y3 <= maxY

        x4 = randrange(x1, maxX)
        logging.debug(f"x4: {x4}")
        assert minX <= x4 <= maxX

        y4 = randrange(minY, y3)
        logging.debug(f"y4: {y4}")
        assert minY <= y4 <= maxY

        return Rect(self.canvas, x1, y1, x2, y2, x3, y3, x4, y4, color=color)

    def random_pentagon(self, bounds, color):
        logging.debug("random_pentagon()")

        minX = bounds.x1
        maxX = bounds.x2
        minY = bounds.y1
        maxY = bounds.y2

        x1 = randrange(minX, maxX)
        logging.debug(f"x1: {x1}")
        assert minX <= x1 <= maxX

        y1 = randrange(minY, maxY)
        logging.debug(f"y1: {y1}")
        assert minY <= y1 <= maxY

        x2 = randrange(minX, x1)
        logging.debug(f"x2: {x2}")
        assert minX <= x2 <= maxX

        y2 = randrange(y1, maxY)
        logging.debug(f"y2: {y2}")
        assert minY <= y2 <= maxY

        x3 = randrange(x2, maxX)
        logging.debug(f"x3: {x3}")
        assert minX <= x3 <= maxX

        y3 = randrange(y2, maxY)
        logging.debug(f"y3: {y3}")
        assert minY <= y3 <= maxY

        x4 = randrange(x3, maxX)
        logging.debug(f"x4: {x4}")
        assert minX <= x4 <= maxX

        y4 = randrange(y3, maxY)
        logging.debug(f"y4: {y4}")
        assert minY <= y4 <= maxY

        x5 = randrange(x1, maxX)
        logging.debug(f"x5: {x5}")
        assert minX <= x5 <= maxX

        y5 = randrange(y1, maxY)
        logging.debug(f"y5: {y5}")
        assert minY <= y1 <= maxY

        return Pentagon(self.canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, color=color)

    def random_hexagon(self, bounds, color):
        logging.debug("random_hexagon()")

        minX = bounds.x1
        maxX = bounds.x2
        minY = bounds.y1
        maxY = bounds.y2

        x1 = randrange(minX, maxX)
        logging.debug(f"x1: {x1}")
        assert minX <= x1 <= maxX

        y1 = randrange(minY, maxY)
        logging.debug(f"y1: {y1}")
        assert minY <= y1 <= maxY

        x2 = randrange(minX, x1)
        logging.debug(f"x2: {x2}")
        assert minX <= x2 <= maxX

        y2 = randrange(y1, maxY)
        logging.debug(f"y2: {y2}")
        assert minY <= y2 <= maxY

        x3 = randrange(minX, x2)
        logging.debug(f"x3: {x3}")
        assert minX <= x3 <= maxX

        y3 = randrange(y2, maxY)
        logging.debug(f"y3: {y3}")
        assert minY <= y3 <= maxY

        x4 = randrange(x3, maxX)
        logging.debug(f"x4: {x4}")
        assert minX <= x4 <= maxX

        y4 = randrange(y3, maxY)
        logging.debug(f"y4: {y4}")
        assert minY <= y4 <= maxY

        x5 = randrange(x4, maxX)
        logging.debug(f"x5: {x5}")
        assert minX <= x5 <= maxX

        y5 = randrange(y2, y4)
        logging.debug(f"y5: {y5}")
        assert minY <= y5 <= maxY

        x6 = randrange(x4, maxX)
        logging.debug(f"x6: {x6}")
        assert minX <= x6 <= maxX

        y6 = randrange(y1, y5)
        logging.debug(f"y6: {y6}")
        assert minY <= y6 <= maxY

        return Hexagon(self.canvas, x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6, color=color)

    def random_circle(self, bounds, color):
        logging.debug("random_circle()")

        minX = bounds.x1
        maxX = bounds.x2
        minY = bounds.y1
        maxY = bounds.y2

        x1 = randrange(minX, maxX)
        logging.debug(f"x1: {x1}")
        assert minX <= x1 <= maxX

        y1 = randrange(minY, maxY)
        logging.debug(f"y1: {y1}")
        assert minY <= y1 <= maxY

        x2 = randrange(x1, maxX)
        logging.debug(f"x2: {x2}")
        assert minX <= x2 <= maxX

        y2 = randrange(y1, maxY)
        logging.debug(f"y2: {y2}")
        assert minY <= y2 <= maxY

        return Circle(self.canvas, x1, y1, x2, y2, color=color)

    def random_shape(self, bounds):
        logging.debug(f"random_shape(bounds={bounds})")
        shape = random.randrange(5)
        color = random.choice(self.sprite_colors)

        result = None

        if shape == 0:
            result = self.random_triangle(bounds, color)
        elif shape == 1:
            result = self.random_rectangle(bounds, color)
        elif shape == 2:
            result = self.random_pentagon(bounds, color)
        elif shape == 3:
            result = self.random_hexagon(bounds, color)
        elif shape == 4:
            result = self.random_circle(bounds, color)

        logging.debug(f"random_shape returns {result} with bounding rect {result.coords}")

        return result

    def __init__(self, bounds: BoundingRect, sprite_colors: list[str], canvas: Canvas):
        self.taken_boxes = []
        self.bounds = bounds
        self.sprite_colors = sprite_colors
        self.canvas = canvas

    def spawn_enemy(self):
        enemy_bounds = self.__class__.free_box(self.taken_boxes, self.bounds)
        new_enemy = self.random_shape(enemy_bounds)
        if new_enemy.coords.width != 0 and new_enemy.coords.height != 0:
            self.taken_boxes.append(new_enemy.coords)
        return new_enemy
