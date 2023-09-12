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
        self.coordinates: list[list[Rect | None]] = list()
        for i in range(self.number_lines):
            self.coordinates.append(list())
            for _ in range(self.number_columns):
                self.coordinates[i].append(Rect(0, 0, spacing[0], spacing[1]))
        self.update()


    def __str__(self) -> str:
        string = [f"lines: {self.number_lines}", f"columns: {self.number_columns}", f"spacing: {self.spacing.w} {self.spacing.h}", f"topleft: {self.position.topleft}", f"coordinates: {self.coordinates}"]
        return "\n".join(string)


    def move(self, vertex: str, relative_coordinates: tuple[int, int]) -> None:
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

        for i in range(self.number_lines):
            for j in range(self.number_columns):
                rect = self.coordinates[i][j]
                if rect is None:
                    continue
                x = self.position.left + j*self.spacing.w
                y = self.position.top + i*self.spacing.h
                rect.topleft = x, y


    def shift(self, shift_amount: tuple[int,int], line_index: int | None = None, column_index: int | None = None) -> None:
        """ moves all elements which belong to the same line/column
            by a certain displacement value given as coordinates

            if both line_index and column_index are None, all elements
            are shifted

            if both line_index and column_index are not None, only 1 element
            is shifted """

        if not (line_index or column_index):
            for i in range(self.number_lines):
                for j in range(self.number_columns):
                    rect = self.coordinates[i][j]
                    if rect is None:
                        continue
                    rect.move_ip(shift_amount)
            return


        if line_index is not None:
            for rect in self.coordinates[line_index]:
                if rect is None:
                    continue
                rect.move_ip(shift_amount)

        if column_index is None:
            return

        for l in range(self.number_lines):
            rect = self.coordinates[l][column_index] 
            if rect is not None:
                rect.move_ip(shift_amount)


    def get_positions(self, vertex: str) -> list[tuple[int, int]]:
        positions = list()
        for i in range(self.number_lines):
            for j in range(self.number_columns):
                rect = self.coordinates[i][j]
                if rect is None:
                    continue
                position = getattr(rect, vertex)
                positions.append(position)
        return positions
