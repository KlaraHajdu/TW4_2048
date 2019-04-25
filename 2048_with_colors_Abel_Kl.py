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
        for x in range(4):
            if tiles[x][3] == tiles[x][2] == tiles[x][1] == tiles[x][0]:
                tiles[x][0], tiles[x][2] = 0, 0
                tiles[x][1], tiles[x][3] = tiles[x][1] * 2,  tiles[x][3] * 2
                score += tiles[x][1] + tiles[x][3]
            for y in range(3, 0, -1):
                if tiles[x][y] == tiles[x][y-1]:
                    tiles[x][y] *= 2
                    tiles[x][y-1] = 0
                    score += tiles[x][y]

    elif direction == "LEFT":
        for x in range(4):
            if tiles[x][3] == tiles[x][2] == tiles[x][1] == tiles[x][0]:
                tiles[x][3], tiles[x][1] = 0, 0
                tiles[x][2], tiles[x][0] = tiles[x][2] * 2, tiles[x][0] * 2
                score += tiles[x][2] + tiles[x][0]
            for y in range(3):
                if tiles[x][y] == tiles[x][y+1]:
                    tiles[x][y] = tiles[x][y] * 2
                    tiles[x][y+1] = 0
                    score += tiles[x][y]

    elif direction == "UP":

        for y in range(4):
            if tiles[0][y] == tiles[1][y] == tiles[2][y] == tiles[3][y]:
                tiles[0][y], tiles[2][y] = tiles[0][y] * 2, tiles[2][y] * 2
                tiles[1][y], tiles[3][y] = 0, 0
                score += tiles[0][y] + tiles[2][y]
            for x in range(3):
                if tiles[x][y] == tiles[x+1][y]:
                    tiles[x][y] = tiles[x][y] * 2
                    tiles[x+1][y] = 0
                    score += tiles[x][y]

    elif direction == "DOWN":

        for y in range(4):
            if tiles[0][y] == tiles[1][y] == tiles[2][y] == tiles[3][y]:
                tiles[0][y], tiles[2][y] = 0, 0
                tiles[1][y], tiles[3][y] = tiles[1][y] * 2, tiles[3][y] * 2
                score += tiles[1][y] + tiles[3][y]

            for x in range(3, 0, -1):
                if tiles[x][y] == tiles[x-1][y]:
                    tiles[x][y] = tiles[x-1][y] * 2
                    tiles[2][y] = 0
                    score += tiles[3][y]

    slide(direction, tiles)
    return score


def draw(stdscr, score, tiles):
    # which number is which color
    color = {2: 6, 1024: 6, 4: 2, 512: 2, 8: 3,
             256: 3, 16: 4, 128: 4, 32: 5, 64: 5, 2048: 1}
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
                stdscr.addstr(str(tiles[x][y]).center(
                    5), curses.color_pair(color[tiles[x][y]]))
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

        bottom, top, step = (
            3, 0, -1) if dir == "UP" or dir == "LEFT" else(0, 3, 1)
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


def keyboard_inputs(stdscr, can):
    while True:
        while True:

            # get keyboard input, returns -1 if none available
            c = stdscr.getch()
            key = ""
            if c != -1:
                if c == ord('q'):
                    return "QUIT"
                elif c == curses.KEY_DOWN:
                    key = "DOWN"
                    break
                elif c == curses.KEY_UP:
                    key = "UP"
                    break
                elif c == curses.KEY_LEFT:
                    key = "LEFT"
                    break
                elif c == curses.KEY_RIGHT:
                    key = "RIGHT"
                    break
        if key in can:
            return key


def init_curses():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)


def game_over(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr("Game over")
        stdscr.refresh()
        if stdscr.getch() == ord('q'):
            break


def main(stdscr):
    init_curses()
    tiles = []
    for tile in range(4):
        tiles.append([0] * 4)
    printed = False
    spawn(tiles)
    score = 0
    while True:
        spawn(tiles)
        can = can_move(tiles)
        if not can:
            break
        while True:
            try:
                draw(stdscr, score, tiles)
                break
            except curses.error:
                if not printed:
                    stdscr.clear()
                    stdscr.addstr("Screen too small, please restart the program!")
                    stdscr.refresh()
                    printed = True
        key = keyboard_inputs(stdscr, can)
        if key == "QUIT":
            break
        score += add(key, tiles)
    game_over(stdscr)


# wrap it so it doesn't mess with terminal settings while debugging
if __name__ == '__main__':
    curses.wrapper(main)
