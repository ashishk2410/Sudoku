import datetime
from copy import deepcopy

GRID_SIZE = 9
SUBGRID_SIZE = 3

def print_sudoku(puzzle):
    """Prints the Sudoku puzzle in a 9x9 grid format."""
    separator = "=" * 41
    print(separator)
    for i in range(GRID_SIZE):
        if i in [3, 6]:
            print(separator)
        row = " || ".join([" | ".join(map(str, puzzle[i][j:j+SUBGRID_SIZE])) for j in range(0, GRID_SIZE, SUBGRID_SIZE)])
        print(f"|| {row} ||")
    print(separator)
    print()

def pop_n(puzzle_comb, x, y, n):
    """Removes n from all related rows, columns, and boxes."""
    for j in range(GRID_SIZE):
        if puzzle_comb[j][y] != 0 and n in puzzle_comb[j][y]:
            puzzle_comb[j][y].remove(n)
            if not puzzle_comb[j][y]:
                puzzle_comb[j][y] = 0

        if puzzle_comb[x][j] != 0 and n in puzzle_comb[x][j]:
            puzzle_comb[x][j].remove(n)
            if not puzzle_comb[x][j]:
                puzzle_comb[x][j] = 0

    box_x = (x // SUBGRID_SIZE) * SUBGRID_SIZE
    box_y = (y // SUBGRID_SIZE) * SUBGRID_SIZE
    for j in range(box_x, box_x + SUBGRID_SIZE):
        for k in range(box_y, box_y + SUBGRID_SIZE):
            if puzzle_comb[j][k] != 0 and n in puzzle_comb[j][k]:
                puzzle_comb[j][k].remove(n)
                if not puzzle_comb[j][k]:
                    puzzle_comb[j][k] = 0

def input_n(puzzle, puzzle_comb, x, y, n, sudoku_cnt):
    """Inserts a number into the puzzle and updates combinations."""
    sudoku_cnt -= 1
    puzzle[x][y] = n
    puzzle_comb[x][y] = 0
    pop_n(puzzle_comb, x, y, n)
    return sudoku_cnt

def input_sudoku(puzzle, puzzle_comb, s_inputs):
    """Provides input to sudoku puzzle from predefined inputs."""
    for n in s_inputs:
        x = int(n / 100) - 1
        y = int((n % 100) / 10) - 1
        num = n % 10
        sudoku_cnt = input_n(puzzle, puzzle_comb, x, y, num, 81)
    print("INPUT SUDOKU COMPLETED...")
    return puzzle, puzzle_comb

def solve_sudoku(puzzle, puzzle_comb):
    """Solves Sudoku using single suggestion technique."""
    flg = 0
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if puzzle_comb[x][y] != 0 and len(puzzle_comb[x][y]) == 1:
                n = puzzle_comb[x][y][0]
                sudoku_cnt = input_n(puzzle, puzzle_comb, x, y, n, 81)
                flg = 1
    return flg

def naked_pair(puzzle_comb):
    """Checks for naked pairs and updates possibilities."""
    flg = 0
    for x in range(GRID_SIZE):
        s = -1
        for y in range(GRID_SIZE):
            if s == -1 and puzzle_comb[x][y] != 0 and len(puzzle_comb[x][y]) == 2:
                s = y
            elif s != -1 and puzzle_comb[x][y] == puzzle_comb[x][s]:
                for item in puzzle_comb[x][y]:
                    for z in range(GRID_SIZE):
                        if z != y and z != s and puzzle_comb[x][z] != 0 and item in puzzle_comb[x][z]:
                            puzzle_comb[x][z].remove(item)
                            flg = 1
                break

    for x in range(GRID_SIZE):
        s = -1
        for y in range(GRID_SIZE):
            if s == -1 and puzzle_comb[y][x] != 0 and len(puzzle_comb[y][x]) == 2:
                s = y
            elif s != -1 and puzzle_comb[y][x] == puzzle_comb[s][x]:
                for item in puzzle_comb[y][x]:
                    for z in range(GRID_SIZE):
                        if z != y and z != s and puzzle_comb[z][x] != 0 and item in puzzle_comb[z][x]:
                            puzzle_comb[z][x].remove(item)
                            flg = 1
                break

    return flg

def hidden_pair_rc(puzzle_comb, choice):
    """Checks for hidden pairs in rows or columns and updates possibilities."""
    flg = 0
    for x in range(GRID_SIZE):
        srtd_box = []
        srtd_box1 = []
        for t in range(GRID_SIZE):
            val = puzzle_comb[x][t] if choice == "r" else puzzle_comb[t][x]
            if val != 0:
                srtd_box += val
        srtd_box1 = sorted(set([i for i in srtd_box if srtd_box.count(i) == 2]))
        if len(srtd_box1) >= 2:
            tmp = list(map(list, ((x, y) for x in srtd_box1 for y in srtd_box1 if x != y and x < y)))
        else:
            continue
        for srtd_box1 in tmp:
            s = -1
            for y in range(GRID_SIZE):
                r, c = (x, y) if choice == "r" else (y, x)
                if s == -1 and puzzle_comb[r][c] != 0 and set(srtd_box1).intersection(puzzle_comb[r][c]) == set(srtd_box1):
                    s = y
                elif s != -1 and puzzle_comb[r][c] != 0 and set(srtd_box1).intersection(puzzle_comb[r][c]) == set(srtd_box1):
                    for item in puzzle_comb[r][c]:
                        if item not in srtd_box1:
                            puzzle_comb[r][c].remove(item)
                            flg = 1
                    lst = puzzle_comb[x][s] if choice == "r" else puzzle_comb[s][x]
                    for item in lst:
                        if item not in srtd_box1:
                            lst.remove(item)
                            flg = 1
                    break
    return flg

def hidden_pair(puzzle_comb):
    """Checks for hidden pairs and updates possibilities."""
    return hidden_pair_rc(puzzle_comb, "r") + hidden_pair_rc(puzzle_comb, "c")

def solve_sudoku_pos_rc(puzzle_comb, x, y, item, choice):
    """Helper function to solve Sudoku using positional techniques."""
    flg = 0
    for r in range(GRID_SIZE):
        if choice == "r" and not (r >= (y // SUBGRID_SIZE) * SUBGRID_SIZE and r < (y // SUBGRID_SIZE) * SUBGRID_SIZE + SUBGRID_SIZE):
            if item in puzzle_comb[x][r]:
                flg = 1
                break
        elif choice == "c" and not (r >= (x // SUBGRID_SIZE) * SUBGRID_SIZE and r < (x // SUBGRID_SIZE) * SUBGRID_SIZE + SUBGRID_SIZE):
            if item in puzzle_comb[r][y]:
                flg = 1
                break
    if flg == 0:
        for a in range((x // SUBGRID_SIZE) * SUBGRID_SIZE, (x // SUBGRID_SIZE) * SUBGRID_SIZE + SUBGRID_SIZE):
            if (choice == "r" and a == x) or (choice == "c" and a == y):
                continue
            for b in range((y // SUBGRID_SIZE) * SUBGRID_SIZE, (y // SUBGRID_SIZE) * SUBGRID_SIZE + SUBGRID_SIZE):
                if choice == "c" and b == y:
                    continue
                if item in puzzle_comb[a][b]:
                    puzzle_comb[a][b].remove(item)
                    flg = 1
    return flg

def solve_sudoku_pos(puzzle_comb):
    """Solves Sudoku using positional techniques."""
    flag = 0
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if puzzle_comb[x][y] != 0 and len(puzzle_comb[x][y]) >= 1:
                for item in puzzle_comb[x][y]:
                    flag += solve_sudoku_pos_rc(puzzle_comb, x, y, item, "r")
                    flag += solve_sudoku_pos_rc(puzzle_comb, x, y, item, "c")
    return flag

def find_unique_box(puzzle, puzzle_comb):
    """Finds and assigns unique numbers in each 3x3 box."""
    flg = 0
    for x in range(0, GRID_SIZE, SUBGRID_SIZE):
        box = [[] for _ in range(SUBGRID_SIZE)]
        srtd_box = [[] for _ in range(SUBGRID_SIZE)]
        for y in range(GRID_SIZE):
            for i in range(SUBGRID_SIZE):
                if puzzle_comb[x + i][y] != 0:
                    box[y // SUBGRID_SIZE] += puzzle_comb[x + i][y]
        for y in range(SUBGRID_SIZE):
            srtd_box[y] = sorted(set([i for i in box[y] if box[y].count(i) == 1]))
            for item in srtd_box[y]:
                for z in range(y * SUBGRID_SIZE, (y + 1) * SUBGRID_SIZE):
                    for i in range(SUBGRID_SIZE):
                        if puzzle_comb[x + i][z] != 0 and puzzle_comb[x + i][z].count(item) == 1:
                            sudoku_cnt = input_n(puzzle, puzzle_comb, x + i, z, item, 81)
                            flg = 1
                            break
    return flg

def solve_candidate_line(puzzle, puzzle_comb):
    """Solves Sudoku using candidate line technique."""
    flg = 0
    for x in range(0, GRID_SIZE, SUBGRID_SIZE):
        box = [[] for _ in range(SUBGRID_SIZE)]
        srtd_box = [[] for _ in range(SUBGRID_SIZE)]
        for y in range(GRID_SIZE):
            for i in range(SUBGRID_SIZE):
                if puzzle_comb[x + i][y] != 0:
                    box[y // SUBGRID_SIZE] += puzzle_comb[x + i][y]
        for y in range(SUBGRID_SIZE):
            srtd_box[y] = sorted(set([i for i in box[y] if box[y].count(i) >= 1]))
            for item in srtd_box[y]:
                for z in range(y * SUBGRID_SIZE, (y + 1) * SUBGRID_SIZE):
                    for i in range(SUBGRID_SIZE):
                        if puzzle_comb[x + i][z] != 0 and puzzle_comb[x + i][z].count(item) == 1:
                            flg += unique_in_row(puzzle_comb, item, x + i, z)
                            flg += unique_in_col(puzzle_comb, item, x + i, z)
    return flg

def unique_in_row(puzzle_comb, num, row_no, col_no):
    """Eliminates candidates from a row."""
    flg = 0
    subgrid_cols = range((col_no // SUBGRID_SIZE) * SUBGRID_SIZE, (col_no // SUBGRID_SIZE) * SUBGRID_SIZE + SUBGRID_SIZE)
    if all(num not in puzzle_comb[row_no][col] for col in subgrid_cols):
        for b in range(GRID_SIZE):
            if b not in subgrid_cols and num in puzzle_comb[row_no][b]:
                puzzle_comb[row_no][b].remove(num)
                flg = 1
    return flg

def unique_in_col(puzzle_comb, num, row_no, col_no):
    """Eliminates candidates from a column."""
    flg = 0
    subgrid_rows = range((row_no // SUBGRID_SIZE) * SUBGRID_SIZE, (row_no // SUBGRID_SIZE) * SUBGRID_SIZE + SUBGRID_SIZE)
    if all(num not in puzzle_comb[row][col_no] for row in subgrid_rows):
        for b in range(GRID_SIZE):
            if b not in subgrid_rows and num in puzzle_comb[b][col_no]:
                puzzle_comb[b][col_no].remove(num)
                flg = 1
    return flg

def find_unique(puzzle, puzzle_comb):
    """Finds unique candidates in rows and columns and assigns them."""
    flg = 0
    for x in range(GRID_SIZE):
        lst_row = []
        lst_col = []
        for y in range(GRID_SIZE):
            if puzzle_comb[x][y] != 0:
                lst_row += puzzle_comb[x][y]
            if puzzle_comb[y][x] != 0:
                lst_col += puzzle_comb[y][x]
        srtd_row = sorted(set([i for i in lst_row if lst_row.count(i) == 1]))
        srtd_col = sorted(set([i for i in lst_col if lst_col.count(i) == 1]))
        for item in srtd_row:
            for y in range(GRID_SIZE):
                if puzzle_comb[x][y] != 0 and puzzle_comb[x][y].count(item) == 1:
                    sudoku_cnt = input_n(puzzle, puzzle_comb, x, y, item, 81)
                    flg = 1
                    break
        for item in srtd_col:
            for y in range(GRID_SIZE):
                if puzzle_comb[y][x] != 0 and puzzle_comb[y][x].count(item) == 1:
                    sudoku_cnt = input_n(puzzle, puzzle_comb, y, x, item, 81)
                    flg = 1
                    break
    return flg

def main():
    """Main function to solve the Sudoku puzzle."""
    w, h, z = GRID_SIZE, GRID_SIZE, GRID_SIZE
    sudoku_cnt = 81
    puzzle = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    puzzle_comb = [[[x + 1 for x in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    s_inputs = [122, 155, 177, 233, 264, 298, 337, 361, 426, 439, 453, 512, 558, 597, 652, 676, 684, 743, 771, 819, 846, 872, 938, 951, 986]
    
    puzzle, puzzle_comb = input_sudoku(puzzle, puzzle_comb, s_inputs)
    print("Sudoku sheet")
    print_sudoku(puzzle)

    print("Start Solving....")
    level = 0
    st_time = datetime.datetime.now()
    flag, i = 1, 0

    while flag > 0 and sudoku_cnt > 0:
        flag = 0
        print("attempt", i + 1)
        flag = solve_sudoku(puzzle, puzzle_comb)
        flag += find_unique(puzzle, puzzle_comb)
        flag += find_unique_box(puzzle, puzzle_comb)
        i += 1

    if sudoku_cnt <= 0:
        level = 1
    elif level == 0:
        flag = 1
        print_sudoku(puzzle)
        print("Candidate Line approach")

    while flag > 0 and sudoku_cnt > 0 and i < 15:
        flag = 0
        print("attempt", i + 1)
        flag = solve_candidate_line(puzzle, puzzle_comb)
        flag += solve_sudoku_pos(puzzle_comb)
        flag += solve_sudoku(puzzle, puzzle_comb)
        flag += find_unique(puzzle, puzzle_comb)
        flag += find_unique_box(puzzle, puzzle_comb)
        i += 1

    if sudoku_cnt <= 0 and level == 0:
        level = 2
    elif level == 0:
        flag = 1
        print_sudoku(puzzle)
        print("Naked Pair approach")

    while flag > 0 and sudoku_cnt > 0 and i < 15:
        flag = 0
        print("attempt", i + 1)
        flag += naked_pair(puzzle_comb)
        flag += solve_candidate_line(puzzle, puzzle_comb)
        flag += solve_sudoku_pos(puzzle_comb)
        flag += solve_sudoku(puzzle, puzzle_comb)
        flag += find_unique(puzzle, puzzle_comb)
        flag += find_unique_box(puzzle, puzzle_comb)
        i += 1

    if sudoku_cnt <= 0 and level == 0:
        level = 3
    elif level == 0:
        flag = 1
        print_sudoku(puzzle)
        print("Hidden Pair approach")

    while flag > 0 and sudoku_cnt > 0 and i < 15:
        flag = 0
        print("attempt", i + 1)
        flag += hidden_pair(puzzle_comb)
        flag += solve_sudoku_pos(puzzle_comb)
        flag += naked_pair(puzzle_comb)
        flag = solve_candidate_line(puzzle, puzzle_comb)
        flag += solve_sudoku(puzzle, puzzle_comb)
        flag += find_unique(puzzle, puzzle_comb)
        flag += find_unique_box(puzzle, puzzle_comb)
        i += 1

    if sudoku_cnt <= 0 and level == 0:
        level = 4
    elif level == 0:
        print_sudoku(puzzle)
        print("Using assumptions")
        temp_count = sudoku_cnt
        temp_puzzle = deepcopy(puzzle)
        temp_comb = deepcopy(puzzle_comb)
        temp_i = i

        for i1 in range(GRID_SIZE):
            for j1 in range(GRID_SIZE):
                if temp_comb[i1][j1] != 0:
                    x, y = i1, j1
                    for item in temp_comb[x][y]:
                        print("attempt", i + 1)
                        sudoku_cnt = input_n(puzzle, puzzle_comb, x, y, item, 81)
                        flag = 1
                        while flag > 0 and sudoku_cnt > 0 and i < 20:
                            flag = 0
                            flag += solve_sudoku(puzzle, puzzle_comb)
                            flag += find_unique(puzzle, puzzle_comb)
                            flag += find_unique_box(puzzle, puzzle_comb)
                            flag += solve_candidate_line(puzzle, puzzle_comb)
                            flag += solve_sudoku_pos(puzzle_comb)
                            flag += naked_pair(puzzle_comb)
                            flag += hidden_pair(puzzle_comb)
                            i += 1
                        if sudoku_cnt <= 0:
                            break
                        else:
                            sudoku_cnt = temp_count
                            puzzle = deepcopy(temp_puzzle)
                            puzzle_comb = deepcopy(temp_comb)
                        i=temp_i
                if sudoku_cnt<=0: 
                    break
    elif sudoku_cnt<=0 and level==0:
        level=5

    if(sudoku_cnt>0):
        print("No Solution")
        print_sudoku(puzzle)
        print_sudoku(puzzle_comb)
        print("Does this has one solution??")
    
    else:
        print("Solved.. puzzle level=",level)
        print_sudoku(puzzle)
        end_time=datetime.datetime.now()
        print("Elapsed Time ",end_time-st_time)
