import time
import gurobipy as gp
from gurobipy import GRB
import tkinter as tk


def create_game():
    global rows, cols, matrix_entries, current_cell
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())

    if matrix_entries:
        for row in matrix_entries:
            for cell in row:
                cell.destroy()

    matrix_entries = []
    for i in range(rows):
        row_entries = []
        for j in range(cols):
            cell = tk.Entry(matrix_frame, justify='center', width=3)
            cell.grid(row=i, column=j, padx=5, pady=5)
            cell.bind('<Key>', lambda event, i=i, j=j: move(event, i, j))
            row_entries.append(cell)
        matrix_entries.append(row_entries)

    current_cell = matrix_entries[0][0]
    current_cell.focus_set()

    solve_button.pack()


def move(event, i, j):
    global current_cell
    if event.keysym == 'Left' and j > 0:
        matrix_entries[i][j - 1].focus_set()
    elif event.keysym == 'Right' and j < cols - 1:
        matrix_entries[i][j + 1].focus_set()
    elif event.keysym == 'Up' and i > 0:
        matrix_entries[i - 1][j].focus_set()
    elif event.keysym == 'Down' and i < rows - 1:
        matrix_entries[i + 1][j].focus_set()


def find_random_connected_component(x_var):
    current_strategy = []

    for i in range(n + 1):
        for j in range(m + 1):
            for k in range(6):
                if x_var[i, j, k].x > 0.75:
                    current_strategy.append([i, j, k])

    connected_component = [current_strategy[0]]

    for i in range(len(current_strategy) - 1):
        stop = True
        i1, j1, k1 = current_strategy[i]
        for j in range(i + 1, len(current_strategy)):
            i2, j2, k2 = current_strategy[j]
            if ((i2 - i1 == 1 and k2 in [0, 1, 4] and j1 == j2) or
                    (i1 - i2 == 1 and k2 in [2, 3, 4] and j1 == j2) or
                    (j1 - j2 == 1 and k2 in [1, 3, 5] and i1 == i2) or
                    (j2 - j1 == 1 and k2 in [0, 2, 5] and i1 == i2)):
                stop = False
                connected_component.append(current_strategy[j])
                current_strategy[i + 1], current_strategy[j] = current_strategy[j], current_strategy[i + 1]
                break
        if stop:
            break

    return connected_component


def display_solution(strategy):
    displayed_solution = [['   ' for _ in range(2 * m + 1)] for _ in range(2 * n + 1)]

    for i in range(0, 2 * n + 1, 2):
        for j in range(0, 2 * m + 1, 2):
            displayed_solution[i][j] = '*'
            if i < 2 * n - 1:
                displayed_solution[i + 1][j] = ' '

    for square in slitherlink_game:
        x, y, a = square
        displayed_solution[2 * x + 1][2 * y + 1] = f' {a} '

    for move in strategy:
        i, j, state = move
        if state == 0:
            displayed_solution[2 * i][2 * j - 1] = '---'
            displayed_solution[2 * i - 1][2 * j] = '|'
        elif state == 1:
            displayed_solution[2 * i][2 * j + 1] = '---'
            displayed_solution[2 * i - 1][2 * j] = '|'
        elif state == 2:
            displayed_solution[2 * i][2 * j - 1] = '---'
            displayed_solution[2 * i + 1][2 * j] = '|'
        elif state == 3:
            displayed_solution[2 * i][2 * j + 1] = '---'
            displayed_solution[2 * i + 1][2 * j] = '|'
        elif state == 4:
            displayed_solution[2 * i + 1][2 * j] = '|'
            displayed_solution[2 * i - 1][2 * j] = '|'
        elif state == 5:
            displayed_solution[2 * i][2 * j + 1] = '---'
            displayed_solution[2 * i][2 * j - 1] = '---'

    print('\nSolution:\n')

    for i in displayed_solution:
        for j in i:
            print(j, end='')
        print()


def solve():
    global slitherlink_game, n, m
    n = int(rows_entry.get())
    m = int(cols_entry.get())

    game = []
    for i in range(n):
        for j in range(m):
            value = matrix_entries[i][j].get()
            if value.isdigit():
                game.append((i, j, int(value)))

    slitherlink_game = game
    model = gp.Model("Slitherlink")

    model.setParam('OutputFlag', 0)

    x = {}
    for i in range(n + 1):
        for j in range(m + 1):
            for k in range(6):
                x[i, j, k] = model.addVar(name=f'x[{i}, {j}, {k}]', vtype=GRB.BINARY)

    for i in range(n + 1):
        for j in range(m + 1):
            model.addConstr(gp.quicksum(x[i, j, k] for k in range(6)) <= 1.0)

    for j in range(m + 1):
        model.addConstr(x[0, j, 0] == 0)
        model.addConstr(x[0, j, 1] == 0)
        model.addConstr(x[0, j, 4] == 0)

        model.addConstr(x[n, j, 2] == 0)
        model.addConstr(x[n, j, 3] == 0)
        model.addConstr(x[n, j, 4] == 0)

    for i in range(n + 1):
        model.addConstr(x[i, 0, 0] == 0)
        model.addConstr(x[i, 0, 2] == 0)
        model.addConstr(x[i, 0, 5] == 0)

        model.addConstr(x[i, m, 1] == 0)
        model.addConstr(x[i, m, 3] == 0)
        model.addConstr(x[i, m, 5] == 0)

    for i in range(n):
        for j in range(m):
            model.addConstr(x[i, j, 2] + x[i, j, 3] + x[i, j, 4] == x[i + 1, j, 0] + x[i + 1, j, 1] + x[i + 1, j, 4])
            model.addConstr(x[i, j, 1] + x[i, j, 3] + x[i, j, 5] == x[i, j + 1, 0] + x[i, j + 1, 2] + x[i, j + 1, 5])

    for i in range(n):
        model.addConstr(x[i, m, 2] + x[i, m, 3] + x[i, m, 4] == x[i + 1, m, 0] + x[i + 1, m, 1] + x[i + 1, m, 4])

    for j in range(m):
        model.addConstr(x[n, j, 1] + x[n, j, 3] + x[n, j, 5] == x[n, j + 1, 0] + x[n, j + 1, 2] + x[n, j + 1, 5])

    for value in slitherlink_game:
        i, j, val = value
        I = i + 1
        J = j + 1
        model.addConstr(
            x[i, j, 1] + x[i, j, 2] + 2 * x[i, j, 3] + x[i, j, 4] + x[i, j, 5]
            + 2 * x[I, J, 0] + x[I, J, 1] + x[I, J, 2] + x[I, J, 4] + x[I, J, 5] == val
        )

    model.setObjective(gp.quicksum(x[i, j, k] for i in range(n + 1) for j in range(m + 1) for k in range(6)),
                       GRB.MINIMIZE)

    start_time = time.time()
    model.optimize()

    if model.status == gp.GRB.INFEASIBLE:
        print("###################\n### No Solution ###\n###################")
        end_time = time.time()
        print(f'\nSolving time: {end_time - start_time} seconds\n')

        return

    while not len(find_random_connected_component(x)) == int(model.objVal):
        random_connected_component = find_random_connected_component(x)
        model.addConstr(
            gp.quicksum(x[i, j, k] for i, j, k in random_connected_component) <= len(random_connected_component) - 1)
        model.optimize()
        if model.status == gp.GRB.INFEASIBLE:
            print("###################\n### No Solution ###\n###################")
            end_time = time.time()
            print(f'\nSolving time: {end_time - start_time} seconds\n')
            return

    end_time = time.time()

    optimal_strategy = []

    for i in range(n + 1):
        for j in range(m + 1):
            for k in range(6):
                if x[i, j, k].x > 0.75:
                    optimal_strategy.append([i, j, k])

    display_solution(optimal_strategy)

    print(f'\nSolving time: {end_time - start_time} seconds\n')


if __name__ == '__main__':
    slitherlink_game = []
    n = m = 0

    root = tk.Tk()
    root.title("Slitherlink Game")

    size_frame = tk.Frame(root)
    size_frame.pack(pady=50)

    rows_label = tk.Label(size_frame, text="Number of Rows:")
    rows_label.grid(row=0, column=0, padx=10)
    rows_entry = tk.Entry(size_frame, justify='center', width=15)
    rows_entry.grid(row=0, column=1, padx=10)

    cols_label = tk.Label(size_frame, text="Number of Columns:")
    cols_label.grid(row=0, column=2, padx=10)
    cols_entry = tk.Entry(size_frame, justify='center', width=15)
    cols_entry.grid(row=0, column=3, padx=10)

    size_button = tk.Button(size_frame, text="Create Game", command=create_game, width=15)
    size_button.grid(row=0, column=4, padx=10)

    solve_button = tk.Button(root, text="Solve", command=solve, width=20)

    matrix_frame = tk.Frame(root)
    matrix_frame.pack(pady=50)

    matrix_entries = None
    rows, cols = None, None

    root.mainloop()