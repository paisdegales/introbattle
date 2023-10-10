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
        self.w: int = number_columns * spacing[0] # total width of this grid (it does not change!!!)
        self.h: int = number_lines * spacing[1] # total height of this grid (it does not change!!!)
        for i in range(self.number_lines):
            self.coordinates.append(list())
            for _ in range(self.number_columns):
                self.coordinates[i].append(Rect(0, 0, spacing[0], spacing[1]))
        self.update()


    def __str__(self) -> str:
        string = [f"lines: {self.number_lines}", f"columns: {self.number_columns}", f"spacing: {self.spacing.w} {self.spacing.h}", f"topleft: {self.position.topleft}", f"coordinates: {self.coordinates}"]
        return "\n".join(string)


    def move(self, vertex: str, relative_coordinates: tuple[int, int]) -> None:
        """ Moves the grid and updates all its points """

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

        self.update_size()


    def update_size(self) -> None:
        """ update the grid's size by looking for the max X and Y coordinates inside of it """

        last_col: list[Rect] = list()
        last_line: list[Rect] = list()

        for line_index in range(self.number_lines):
            rect = self.coordinates[line_index][-1]
            if rect is None:
                continue
            last_col.append(rect)

        for column_index in range(self.number_columns):
            rect = self.coordinates[-1][column_index]
            if rect is None:
                continue
            last_line.append(rect)

        max_x = max([r.bottomright[0] for r in last_col])
        max_y = max([r.bottomright[1] for r in last_col])
        self.w = max_x
        self.h = max_y


    def shift(self, shift_amount: tuple[int,int], line_index: int | None = None, column_index: int | None = None) -> None:
        """ moves all elements which belong to the same line/column
            by a certain displacement value given as coordinates

            if both line_index and column_index are None, all elements
            are shifted

            if both line_index and column_index are not None, only 1 element
            is shifted """

        if line_index is None and column_index is None:
            for i in range(self.number_lines):
                for j in range(self.number_columns):
                    rect = self.coordinates[i][j]
                    if rect is None:
                        continue
                    rect.move_ip(shift_amount)
            self.update_size()
            return


        if line_index is not None:
            for index in range(self.number_columns):
                rect = self.coordinates[line_index][index]
                if rect is None:
                    continue
                rect.move_ip(shift_amount)


        if column_index is None:
            self.update_size()
            return


        for l in range(self.number_lines):
            rect = self.coordinates[l][column_index] 
            if rect is not None:
                rect.move_ip(shift_amount)
        self.update_size()


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
