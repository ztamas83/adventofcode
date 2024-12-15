import re
import numpy as np

# setting path
from puzzle import Puzzle


SUBMIT = False
REMOTE = True

COST_A = 3
COST_B = 1


class Day(Puzzle):
    def __init__(self):
        super(Day, self).__init__(2024, 15)
        self.init_data(remote=REMOTE)

    def move_items(self, items: list[str], start, dir):
        curr_pos = start
        next_pos = start + dir
        print(items)
        if items[next_pos] == "#":
            return items

        if items[next_pos] == "O":
            items = self.move_items(items, next_pos, dir)

        if items[next_pos] == ".":
            items[next_pos] = items[curr_pos]
            items[curr_pos] = "."

        return items

    def move_robot(self, robot_pos: tuple[int, int], move: str, warehouse):
        if move == ">":
            new_row = self.move_items(warehouse[robot_pos[0], :], robot_pos[1], 1)
            warehouse[robot_pos[0]] = new_row

        if move == "<":
            new_row = self.move_items(warehouse[robot_pos[0], :], robot_pos[1], -1)
            warehouse[robot_pos[0]] = new_row

        if move == "^":
            new_col = self.move_items(warehouse[:, robot_pos[1]], robot_pos[0], -1)

            warehouse[:, robot_pos[1]] = new_col

        if move == "v":
            new_col = self.move_items(warehouse[:, robot_pos[1]], robot_pos[0], 1)
            warehouse[:, robot_pos[1]] = new_col

        robot_row, robot_col = np.where(warehouse == "@")
        robot_pos = (int(robot_row[0]), int(robot_col[0]))
        print(robot_pos)
        print(warehouse)
        return robot_pos

    def solve_a(self):
        lines = self._data.splitlines()
        warehouse_floor = [wh_row for wh_row in lines if wh_row.startswith("#")]
        (wh_rows, wh_columns) = (len(warehouse_floor), len(warehouse_floor[0]))

        warehouse = np.zeros((wh_rows, wh_columns), dtype=str)

        moves = lines[wh_columns + 1 :]
        moves = "".join(moves)
        print(moves)

        robot_pos = (0, 0)
        for row_idx, row in enumerate(warehouse_floor):
            for col_idx, cell in enumerate(row):
                warehouse[row_idx][col_idx] = cell
                if cell == "@":
                    robot_pos = (row_idx, col_idx)

        print(warehouse)

        for move in moves:
            print(move)
            robot_pos = self.move_robot(robot_pos, move, warehouse)

        boxes = np.where(warehouse == "O")

        coordinates = list(zip(boxes[0], boxes[1]))
        print(coordinates)

        gps_sum = 0
        for x, y in coordinates:
            gps_coord = int(x) * 100 + int(y)
            gps_sum += gps_coord

            print(f"x: {x}, y: {y}, gps: {gps_coord}")

        return gps_sum

    def solve_b(self):
        (size_x, size_y) = (101, 103) if REMOTE else (11, 7)

        matrix = np.zeros((size_y, size_x), dtype=int)
        data = []

        robots = []
        for line in self._data.splitlines():
            print(line)
            robot = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)
            if robot:
                robots.append(
                    {
                        "position": {"x": int(robot[0][0]), "y": int(robot[0][1])},
                        "velocity": {"x": int(robot[0][2]), "y": int(robot[0][3])},
                    }
                )

        for i in range(0, 14000):
            matrix = np.zeros((size_y, size_x), dtype=int)
            for robot in robots:
                (x, y) = self.move_robot(robot, i, size_x, size_y)
                matrix[y][x] += 1
            # Ignore the middle column and row
            top_left = matrix[: size_y // 2, : size_x // 2]
            top_right = matrix[: size_y // 2, size_x // 2 + 1 :]
            bottom_left = matrix[size_y // 2 + 1 :, : size_x // 2]
            bottom_right = matrix[size_y // 2 + 1 :, size_x // 2 + 1 :]

            sum = (
                np.sum(top_left)
                * np.sum(top_right)
                * np.sum(bottom_left)
                * np.sum(bottom_right)
            )

            data.append(
                (
                    matrix,
                    sum,
                    np.sum(top_left),
                    np.sum(top_right),
                    np.sum(bottom_left),
                    np.sum(bottom_right),
                )
            )
        min_ = min(data, key=lambda x: x[1])
        print(min_)

        index = next((i for i, item in enumerate(data) if item[1] == 133929936), None)

        fig, ax1 = plt.subplots()
        ax1.imshow(min_[0], interpolation="nearest")
        plt.show()

        return index
        # fig, ax1 = plt.subplots()

        # robots_plot = ax1.imshow(data[0], interpolation="nearest")
        # text = ax1.text(80, 80, "t: 0", bbox=dict(facecolor="red", alpha=0.5))

        # def update(frame):
        #     print(frame)
        #     robots_plot.set_array(data[frame])
        #     text.set_text(f"t: {frame}")
        #     return [text, robots_plot]

        # ani = animation.FuncAnimation(fig, update, len(data), interval=10, blit=True)

        # ani.save("animation.gif", writer="imagemagick")
        # plt.show()

    def solve(self):
        return (self.solve_a(), self.solve_b())


solution = Day()

print(f"Solution A: {solution.solve_a()}")
# print(f"Solution B: {solution.solve_b()}")
if SUBMIT:
    solution.submit(sub_a=True, sub_b=False)
