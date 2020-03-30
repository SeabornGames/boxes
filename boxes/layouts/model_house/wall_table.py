import os
import sys
from seaborn_table import SeabornTable

from .cell import VirtualCell, WindowCell, WallCell, DoorCell


class WallTable:
    WALL_FILE_COLUMNS = ['horizontal', 'status',
                         'height_1', 'height_2', 'window_1', 'window_2', 'door',
                         'room_0', 'room_1', 'room_2', 'room_3',
                         'x', 'y', 'symbols']

    def __init__(self, wall_file, clear=False):
        self.wall_file = wall_file
        if os.path.exists(wall_file) and not clear:
            self.wall_table = SeabornTable.file_to_obj(
                wall_file, columns=self.WALL_FILE_COLUMNS)
        else:
            self.wall_table = SeabornTable(columns=self.WALL_FILE_COLUMNS)

    def update_wall_file(self, diagram):
        diagram.grid = diagram.create_grid()
        diagram.add_layout_to_grid()
        grid = '\n'.join(diagram.grid)
        for room in diagram.rooms:
            room.calc_room_dimensions(diagram.layout, diagram.width * 4,
                                      diagram.height * 2)
        horizontal = self.extract_horizontal_walls(grid, diagram.rooms)
        vertical = self.extract_vertical_walls(grid, diagram.rooms)

        for row in self.wall_table:
            row['status'] = 'missing'

        def update_wall(wall):
            for row in self.wall_table:
                if (row['status'] == 'missing' and
                            wall['horizontal'] == row.get('horizontal') and
                            wall.get('room_0') == row.get('room_0') and
                            wall.get('room_1') == row.get('room_1') and
                            wall.get('room_2') == row.get('room_2') and
                            wall.get('room_3') == row.get('room_3')):
                    row.update(wall)
                    row['status'] = 'used'
                    return True
            return False

        for wall in horizontal + vertical:
            if not update_wall(wall):
                self.wall_table.append(dict(status='new', **wall))
        self.wall_table.obj_to_file(self.wall_file, align='left',
                                    quote_numbers=False)

    def extract_horizontal_walls(self, grid, rooms):
        horizontal_cells = [DoorCell.horizontal, VirtualCell.horizontal,
                          WindowCell.horizontal, WallCell.horizontal]
        for v in [WallCell.vertical, WindowCell.vertical] + list(
                VirtualCell.characters):
            grid = grid.replace(v, ' ')
        walls = []
        grid = grid.split('\n')
        for y in range(len(grid)):
            symbols = ''
            for x in range(len(grid[y])):
                cell = grid[y][x]
                if cell != ' ':
                    symbols += cell
                if cell == ' ' or x == len(grid[y]):
                    if len(symbols) > 1:
                        wall = dict(x=x - len(symbols),
                                    y=y,
                                    symbols=symbols,
                                    horizontal=True)
                        wall_rooms = self.extract_rooms(
                            x - len(symbols), x, y, y + 1, rooms)
                        if not wall_rooms:
                            print("WARNING: failed to find room for horizontal"
                                  " wall from x: %s to %s and y: %s" %
                                  (x - len(symbols), x, y))
                            sys.exit(1)
                        for i, room in enumerate(wall_rooms):
                            wall[f'room_{i}'] = room
                        walls.append(wall)
                    symbols = ''
        return walls

    def extract_vertical_walls(self, grid, rooms):
        vertical_cells = [DoorCell.vertical, VirtualCell.vertical,
                          WindowCell.vertical, WallCell.vertical]

        for h in [WallCell.horizontal,
                  WindowCell.horizontal] + list(VirtualCell.characters):
            grid = grid.replace(h, ' ')

        walls = []
        grid = grid.split('\n')
        for x in range(len(grid[0])):
            symbols = ''
            for y in range(len(grid)):
                cell = grid[y][x]
                if cell != ' ':
                    symbols += cell
                if cell not in vertical_cells or x == len(grid[y]):
                    if len(symbols) > 1:
                        symbols = self.convert_vertical_to_horizontal(symbols)
                        wall = dict(x=x,
                                    y=y - len(symbols),
                                    symbols=symbols.strip(),
                                    horizontal=False)
                        wall_rooms = self.extract_rooms(
                            x, x + 1, y - len(symbols), y, rooms)
                        for i, room in enumerate(wall_rooms):
                            wall[f'room_{i}'] = room
                        walls.append(wall)
                        symbols = ''
                    elif cell == ' ':
                        symbols = ''
        return walls

    def convert_vertical_to_horizontal(self, symbols):
        # rotate wall counter clockwise
        replacements = {}
        for cls in [WallCell, WindowCell, VirtualCell, DoorCell]:
            for _old, _new in [('vertical', 'horizontal'),
                               ('top_left_corner', 'bottom_left_corner'),
                               ('top_intersect', 'left_intersect'),
                               ('top_right_corner', 'top_left_corner'),
                               ('bottom_left_corner', 'bottom_right_corner'),
                               ('bottom_intersect', 'right_intersect'),
                               ('bottom_right_corner', 'top_right_corner'),
                               ('left_intersect', 'bottom_intersect'),
                               ('right_intersect', 'top_intersect')
                               ]:
                if getattr(cls, _old, None) and getattr(cls, _new, None):
                    replacements[getattr(cls, _old)] = getattr(cls, _new)

        return ''.join([replacements.get(s, s) for s in symbols])

    @staticmethod
    def extract_rooms(x_start, x_end, y_start, y_end, rooms):
        def room_found(room):
            if not room.walls:
                return False
            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    if (x, y) in room.walls:
                        return True
            return False

        return [room for room in rooms if room_found(room)]

    def recreate_diagram_file(self, filename):
        walls = [wall for wall in self.wall_table if wall.status != 'missing']
        width = max([wall.x + len(wall.symbols) for wall in walls
                     if wall.horizontal])
        height = max([wall.y + len(wall.symbols) for wall in walls
                      if not wall.horizontal])
        grid = [[' ' for w in width] for h in height]
        for wall in self.wall_table:
            if wall.horizontal:
                for i, s in enumerate(wall.symbols):
                    grid[wall.y][wall.x + i] = s
            else:
                for i, s in enumerate(wall.symbols):
                    grid[wall.y + i][wall.x] = s
        with open(filename, 'w') as fn:
            fn.write('\n'.join([''.join(row) for row in grid]))
