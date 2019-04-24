import curses
from random import randint


def can_move(tiles):
    dir_string = []
    can_move = [False, False, False, False]
    for dir in ["UP_DOWN", "LEFT_RIGHT"]:
        x_offset = 1 if dir == "UP_DOWN" else 0
        y_offset = 0 if dir == "UP_DOWN" else 1
        vertical = 0 if dir == "UP_DOWN" else 2 
        for row_col_1 in range(4):
            for row_col_2 in range(3):
                y = row_col_1 if dir == "UP_DOWN" else row_col_2
                x = row_col_2 if dir == "UP_DOWN" else row_col_1
                if tiles[x + x_offset][y + y_offset] != 0 and tiles[x][y] == 0:
                    can_move[0 + vertical] = True
                if tiles[x][y] != 0 and tiles[x + x_offset][y + y_offset] == 0:
                    can_move[1 + vertical] = True
                if tiles[x][y] == tiles[x + x_offset][y + y_offset] and tiles[x][y] != 0:
                    can_move[0 + vertical] = True
                    can_move[1 + vertical] = True

    for i in range(4):
        if can_move[i]:
            if i == 0:
                dir_string.append("UP")
            if i == 1:
                dir_string.append("DOWN")
            if i == 2:
                dir_string.append("LEFT")
            if i == 3:
                dir_string.append("RIGHT")

    return dir_string


def add(direction, tiles):
    score = 0
    slide(direction, tiles)

    if direction == "RIGHT":
        for i in range(4):
            if tiles[i][3] == tiles[i][2] == tiles[i][1] == tiles[i][0]:
                tiles[i][3] = tiles[i][3] * 2
                tiles[i][2] = 0
                tiles[i][1] = tiles[i][1] * 2
                tiles[i][0] = 0
                score += tiles[i][1] + tiles[i][3]

            if tiles[i][3] == tiles[i][2]:
                tiles[i][3] = tiles[i][2] * 2
                tiles[i][2] = 0
                score += tiles[i][3]

            if tiles[i][2] == tiles[i][1]:
                tiles[i][2] = tiles[i][2] * 2
                tiles[i][1] = 0
                score += tiles[i][2]

            if tiles[i][1] == tiles[i][0]:
                tiles[i][1] = tiles[i][1] * 2
                tiles[i][0] = 0
                score += tiles[i][1]

    elif direction == "LEFT":
        for i in range(4):
            if tiles[i][3] == tiles[i][2] == tiles[i][1] == tiles[i][0]:
                tiles[i][3] = 0
                tiles[i][2] = tiles[i][1] * 2
                tiles[i][1] = 0
                tiles[i][0] = tiles[i][1] * 2
                score += tiles[i][2] + tiles[i][0]

            if tiles[i][0] == tiles[i][1]:
                tiles[i][0] = tiles[i][0] * 2
                tiles[i][1] = 0
                score += tiles[i][0]

            if tiles[i][1] == tiles[i][2]:
                tiles[i][1] = tiles[i][1] * 2
                tiles[i][2] = 0
                score += tiles[i][1]

            if tiles[i][2] == tiles[i][3]:
                tiles[i][2] = tiles[i][2] * 2
                tiles[i][3] = 0
                score += tiles[i][2]

    elif direction == "UP":

        for i in range(4):
            if tiles[0][i] == tiles[1][i] == tiles[2][i] == tiles[3][i]:
                tiles[0][i] = tiles[0][i] * 2
                tiles[1][i] = 0
                tiles[2][i] = tiles[2][i] * 2
                tiles[3][i] = 0
                score += tiles[0][i] + tiles[2][i]

            if tiles[0][i] == tiles[1][i]:
                tiles[0][i] = tiles[0][i] * 2
                tiles[1][i] = 0
                score += tiles[0][i]

            if tiles[1][i] == tiles[2][i]:
                tiles[1][i] = tiles[1][i] * 2
                tiles[2][i] = 0
                score += tiles[1][i]

            if tiles[2][i] == tiles[3][i]:
                tiles[2][i] = tiles[2][i] * 2
                tiles[3][i] = 0
                score += tiles[2][i]

    elif direction == "DOWN":

        for i in range(4):
            if tiles[0][i] == tiles[1][i] == tiles[2][i] == tiles[3][i]:
                tiles[0][i] = 0
                tiles[1][i] = tiles[1][i] * 2
                tiles[2][i] = 0
                tiles[3][i] = tiles[3][i] * 2
                score += tiles[1][i] + tiles[3][i]

            if tiles[3][i] == tiles[2][i]:
                tiles[3][i] = tiles[3][i] * 2
                tiles[2][i] = 0
                score += tiles[3][i]

            if tiles[2][i] == tiles[1][i]:
                tiles[2][i] = tiles[1][i] * 2
                tiles[1][i] = 0
                score += tiles[2][i]

            if tiles[1][i] == tiles[0][i]:
                tiles[1][i] = tiles[0][i] * 2
                tiles[0][i] = 0
                score += tiles[1][i]
    slide(direction, tiles)
    return score


def draw(stdscr, score, tiles):
    # which number is which color
    color = {2: 6, 1024: 6, 4: 2, 512: 2, 8: 3, 256: 3, 16: 4, 128: 4, 32: 5, 64: 5, 2048: 1}
    stdscr.clear()
    for x in range(4):
        # first line of row
        if x == 0:
            stdscr.addstr("_" * 25 + "\n", curses.color_pair(0))
        else:
            stdscr.addstr(4*("|" + 5 * "_") + "|" + "\n", curses.color_pair(0))
        # second line of row
        stdscr.addstr(4*("|" + 5 * " ") + "|" + "\n", curses.color_pair(0))
        # numbered line
        for y in range(4):
            if tiles[x][y] != 0:
                stdscr.addstr("|", curses.color_pair(0))
                # add the string and chose its color from the dictionary we defined
                stdscr.addstr(str(tiles[x][y]).center(5), curses.color_pair(color[tiles[x][y]]))
            # print space if the number is 0
            else:
                stdscr.addstr("|     ", curses.color_pair(0))
        # fourth line of row
        stdscr.addstr("|" + "\n", curses.color_pair(0))
    # closing line
    stdscr.addstr(4*("|" + 5 * "_") + "|" + "\n", curses.color_pair(0))
    # print out score
    stdscr.addstr(str(score) + "  ", curses.color_pair(0))
    stdscr.refresh()
    stdscr.move(0, 0)


def spawn(tiles):
    instance = 0
    while(True):
        instance += 1
        if randint(0, 1) == 1:
            rand_number = 2
        else:
            rand_number = 4
        rx = randint(0, 3)
        ry = randint(0, 3)

        if tiles[rx][ry] == 0:
            tiles[rx][ry] = rand_number
            return True
            break
        if instance > 10000:
            break
            return False


def slide(dir, tiles):
    moved = True
    while moved:
        moved = False

        bottom, top, step = (3, 0, -1) if dir == "UP" or dir == "LEFT" else(0, 3, 1)
        x_offset = - 1 if dir == "UP" else 1 if dir == "DOWN" else 0
        y_offset = - 1 if dir == "LEFT" else 1 if dir == "RIGHT" else 0

        for rows_cols_1 in range(4):
            for rows_cols_2 in range(bottom, top, step):
                x = rows_cols_1 if dir == "LEFT" or dir == "RIGHT" else rows_cols_2
                y = rows_cols_1 if dir == "UP" or dir == "DOWN" else rows_cols_2
                if not(tiles[x][y] == 0) and tiles[x+x_offset][y+y_offset] == 0:
                    moved = True
                    tiles[x + x_offset][y + y_offset] = tiles[x][y]
                    tiles[x][y] = 0 


def keyboard_inputs(stdscr):
    while True:

        # get keyboard input, returns -1 if none available
        c = stdscr.getch()

        if c != -1:
            if c == ord('q'):
                return "QUIT"
            elif c == curses.KEY_DOWN:
                return "DOWN"
            elif c == curses.KEY_UP:
                return "UP"
            elif c == curses.KEY_LEFT:
                return "LEFT"
            elif c == curses.KEY_RIGHT:
                return "RIGHT"


def init_curses():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)


def main(stdscr):
    init_curses()
    tiles = []
    for tile in range(4):
        tiles.append([0] * 4)

    spawn(tiles)
    score = 0
    while True:
        spawn(tiles)
        can = can_move(tiles)
        if len(can) == 0:
            break
        draw(stdscr, score, tiles)
        while True:
            key = (keyboard_inputs(stdscr))
            if key in can or key == "QUIT":
                break
        if key == "QUIT":
            break
        score += add(key, tiles)
        can = can_move(tiles)
    while True:
        stdscr.clear()
        stdscr.addstr("Game over")
        stdscr.refresh
        if stdscr.getch() == ord('q'):
            break


# wrap it so it doesn't mess with terminal settings while debugging
if __name__ == '__main__':
    curses.wrapper(main)
