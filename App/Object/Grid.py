from pygame.rect import Rect


class Grid:
    """ This class creates a list of pygame.rect.Rect objects and
        positions each one in a Grid fashion way

        The coordinates of each rectangle can be retrieved by
        specifying the desired vertex of interest """

    def __init__(self, number_lines: int, number_columns: int, spacing: tuple[int, int]):
        self.number_lines: int = number_lines
        self.number_columns: int = number_columns
        self.spacing: Rect = Rect((0, 0), spacing)
        self.position: Rect = Rect((0, 0), (number_columns * self.spacing.w, number_lines * self.spacing.h))
        self.update()


    def __str__(self) -> str:
        string = [f"lines: {self.number_lines}", f"columns: {self.number_columns}", f"spacing: {self.spacing.w} {self.spacing.h}", f"topleft: {self.position.topleft}", f"coordinates: {self.coordinates}"]
        return "\n".join(string)


    def move(self, vertex: str, relative_coordinates: tuple[int, int]):
        """ Moving the grid should be the first to be done,
            since any 'shift' or 'use' operations will be
            discarded after the grid get's moved and a call
            to rebuild it from scratch is made by 'update' """

        setattr(self.position, vertex, relative_coordinates)
        self.update()


    def update(self) -> None:
        """ rebuilds the list of coordinates, based on:
            1. the topleft of the grid
            2. how many lines and columns there are
            3. the spacing in between lines and columns

            This method is automatically called by '__init__'
            and 'move' methods and should not be explictly used """

        self.coordinates: list[Rect | None] = list()
        for i in range(self.number_lines):
            for j in range(self.number_columns):
                x = self.position.left + j*self.spacing.w
                y = self.position.top + i*self.spacing.h
                rect = self.spacing.copy().move((x, y))
                self.coordinates.append(rect)


    def shift(self, shift_amount: tuple[int,int], line_index: int, column_index: int) -> None:
        """ moves all elements which belong to the same line/column
            by a certain displacement value given as coordinates """

        for index, rect in enumerate(self.coordinates):
            if rect is not None and (index // self.number_columns) == line_index:
                rect.move_ip(shift_amount)

        for index, rect in enumerate(self.coordinates):
            if rect is not None and (index % self.number_lines) == column_index:
                rect.move_ip(shift_amount)


    def use(self, indexes: list[int]) -> None:
        """ pick certain coordinates by index """

        if not len(indexes):
            return

        new_coords: list[Rect | None] = list()
        for index, position in enumerate(self.coordinates):
            if index in indexes:
                new_coords.append(position)
            else:
                new_coords.append(None)
        self.coordinates = new_coords


    def positions(self, vertex: str) -> list[list[int]]:
        positions: list[list[int]] = list()

        for rect in self.coordinates:
            if rect is not None:
                positions.append(getattr(rect, vertex))

        return positions


    def at(self, index: int, vertex: str = "topleft") -> list[int]:
        size = len(self.coordinates)
        if (index >= size) or (index < -size):
            index %= size

        if self.coordinates[index] is not None:
            return getattr(self.coordinates[index], vertex)

        while self.coordinates[index] is None:
            index += 1
            index %= size

        return getattr(self.coordinates[index], vertex)
