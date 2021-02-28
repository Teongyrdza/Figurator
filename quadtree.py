from rect import *
from point import *
from random import randrange


class QuadTree:
    """A class implementing a quadtree."""

    def __init__(self, boundary: Rect, max_points: int, depth: int):
        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.depth = depth
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.divided = False

    def divide(self):
        """Divide (branch) this node by spawning four children nodes."""
        x1, x2 = self.boundary.x1, self.boundary.x2
        y1, y2 = self.boundary.y1, self.boundary.y2
        cx, cy = self.boundary.cx, self.boundary.cy
        # The boundaries of the four children nodes are "northwest",
        # "northeast", "southeast" and "southwest" quadrants within the
        # boundary of the current node.
        self.nw = QuadTree(Rect(x1, y1, cx, cy), self.max_points, self.depth - 1)
        self.ne = QuadTree(Rect(cx, y1, x2, y2), self.max_points, self.depth - 1)
        self.nw = QuadTree(Rect(x1, cy, cx, y2), self.max_points, self.depth - 1)
        self.nw = QuadTree(Rect(cx, cy, y2, x2), self.max_points, self.depth - 1)

        # Move points to corresponding children
        for point in self.points:
            self.nw.try_insert(point)
            self.ne.try_insert(point)
            self.sw.try_insert(point)
            self.se.try_insert(point)
        self.points = []

        self.divided = True

    def try_insert(self, point: Point) -> bool:
        """Try to try_insert point into this QuadTree."""

        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.max_points and not self.divided:
            self.points.append(point)
            return True

        if not self.divided:
            self.divide()

        return self.nw.try_insert(point) or self.ne.try_insert(point) or self.sw.try_insert(point) or self.se.try_insert(point)

    def query(self, boundary: Rect, found_points: list[Point]) -> Union[list[Point], bool]:
        """Find the points in the quadtree that lie within boundary."""

        if not self.boundary.intersects(boundary):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within boundary ...
        for point in self.points:
            if boundary.contains(point):
                found_points.append(point)
        # ... and if this node has children, search them too.
        if self.divided:
            self.nw.query(boundary, found_points)
            self.ne.query(boundary, found_points)
            self.se.query(boundary, found_points)
            self.sw.query(boundary, found_points)
        return found_points

    def available_box(self) -> Rect:
        """Find a free box in the tree."""

        if self.points == []:
            return self.boundary

        searched_child = randrange(3)

        children = (self.nw, self.ne, self.sw, self.se)
        return children[searched_child].available_box()
