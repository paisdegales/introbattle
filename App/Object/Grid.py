class Grid:
    def __init__(self, topleft: tuple[int,int], spacing: tuple[int, int], dimensions: tuple[int,int]):
        self.x0, self.y0 = topleft
        self.column_spacing, self.line_spacing = spacing
        self.number_lines, self.number_columns = dimensions


    def coordinates(self) -> list[list[int]]:
        coords = list()
        for i in range(self.number_lines):
            for j in range(self.number_columns):
                x = self.x0 + j*self.column_spacing
                y = self.y0 + i*self.line_spacing
                coords.append([x, y])

        return coords


    def shift(self, coords: list[list[int]], shift_amount: tuple[int,int], line_index: int | None = None, column_index: int | None = None) -> list[list[int]]:
        """
            moves all elements which belong to the same line/column by a certain displacement value given as coordinates
        """
        if line_index:
            x, y = shift_amount
            for index, point in enumerate(coords):
                if (index // self.number_columns) == line_index:
                    point[0] += x
                    point[1] += y

        if column_index:
            x, y = shift_amount
            for index, point in enumerate(coords):
                if (index % self.number_lines) == column_index:
                    point[0] += x
                    point[1] += y

        return coords
