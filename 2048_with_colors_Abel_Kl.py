import curses
from random import randint


def can_move(tiles):
    dir_string = []
    can_move = [False, False, False, False]

    # if dir == "UP","DOWN":
    for y in range(4):
        for x in range(3):
            if tiles[x + 1][y] != 0 and tiles[x][y] == 0:
                can_move[0] = True
            if tiles[x][y] != 0 and tiles[x + 1][y] == 0:
                can_move[1] = True
            if tiles[x][y] == tiles[x + 1][y] and tiles[x][y] != 0:
                can_move[0] = True
                can_move[1] = True

    # if dir == "LEFT","RIGHT":
    for x in range(4):
        for y in range(3):
            if tiles[x][y + 1] != 0 and tiles[x][y] == 0:
                can_move[2] = True
            if tiles[x][y] != 0 and tiles[x][y + 1] == 0:
                can_move[3] = True
            if tiles[x][y] == tiles[x][y + 1] and tiles[x][y] != 0:
                can_move[2] = True
                can_move[3] = True

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

    stdscr.clear()

    stdscr.addstr("", curses.color_pair(0))
    for i in range(4):
        if i == 0:
            stdscr.addstr("_" * 25 + "\n", curses.color_pair(0))
        else:
            stdscr.addstr("|" + 5 * "_" + "|" + 5 * "_" + "|" + 5 *
                          "_" + "|" + + 5 * "_" + "|" + "\n", curses.color_pair(0))
        stdscr.addstr("|" + 5 * " " + "|" + 5 * " " + "|" + 5 *
                      " " + "|" + + 5 * " " + "|" + "\n", curses.color_pair(0))
        for j in range(4):
            if tiles[i][j] != 0:
                if tiles[i][j] == 2 or tiles[i][j] == 1024:
                    stdscr.addstr("|", curses.color_pair(0))
                    stdscr.addstr(str(tiles[i][j]).center(
                        5), curses.color_pair(6))
                if tiles[i][j] == 4 or tiles[i][j] == 512:
                    stdscr.addstr("|", curses.color_pair(0))
                    stdscr.addstr(str(tiles[i][j]).center(
                        5), curses.color_pair(2))
                if tiles[i][j] == 8 or tiles[i][j] == 256:
                    stdscr.addstr("|", curses.color_pair(0))
                    stdscr.addstr(str(tiles[i][j]).center(
                        5), curses.color_pair(3))
                if tiles[i][j] == 16 or tiles[i][j] == 128:
                    stdscr.addstr("|", curses.color_pair(0))
                    stdscr.addstr(str(tiles[i][j]).center(
                        5), curses.color_pair(4))
                if tiles[i][j] == 32 or tiles[i][j] == 64:
                    stdscr.addstr("|", curses.color_pair(0))
                    stdscr.addstr(str(tiles[i][j]).center(
                        5), curses.color_pair(5))
                if tiles[i][j] == 2048:
                    stdscr.addstr("|", curses.color_pair(0))
                    stdscr.addstr(str(tiles[i][j]).center(
                        5), curses.color_pair(1))
            else:
                stdscr.addstr("|     ", curses.color_pair(0))
        stdscr.addstr("|" + "\n", curses.color_pair(0))
    stdscr.addstr("|" + 5 * "_" + "|" + 5 * "_" + "|" + 5 * "_" +
                  "|" + + 5 * "_" + "|" + "\n", curses.color_pair(0))

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
        if dir == "UP":
            for y in range(4):
                for x in range(3, 0, -1):
                    if not(tiles[x][y] == 0) and tiles[x - 1][y] == 0:
                        moved = True
                        tiles[x - 1][y] = tiles[x][y]
                        tiles[x][y] = 0
        if dir == "DOWN":
            for y in range(4):
                for x in range(3):
                    if not(tiles[x][y] == 0) and tiles[x + 1][y] == 0:
                        moved = True
                        tiles[x + 1][y] = tiles[x][y]
                        tiles[x][y] = 0
        if dir == "LEFT":
            for x in range(4):
                for y in range(3, 0, -1):
                    if not(tiles[x][y] == 0) and tiles[x][y - 1] == 0:
                        moved = True
                        tiles[x][y - 1] = tiles[x][y]
                        tiles[x][y] = 0
        if dir == "RIGHT":
            for x in range(4):
                for y in range(3):
                    if not(tiles[x][y] == 0) and tiles[x][y + 1] == 0:
                        moved = True
                        tiles[x][y + 1] = tiles[x][y]
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


def main(stdscr):
    # init color-pairs

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    tiles = []
    for tile in range(4):
        tiles.append([0] * 4)

    # do not wait for input when calling getch
    # stdscr.nodelay(1)
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
