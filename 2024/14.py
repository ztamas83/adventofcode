import re
import numpy as np


# setting path
from puzzle import Puzzle
from matplotlib import pyplot as plt
from matplotlib import animation


SUBMIT = False
REMOTE = True

COST_A = 3
COST_B = 1


class Day(Puzzle):
    def __init__(self):
        super(Day, self).__init__(2024, 14)
        self.init_data(remote=REMOTE)

    def move_robot(self, robot, seconds=1, max_x=11, max_y=7):
        new_x = (robot["position"]["x"] + robot["velocity"]["x"] * seconds) % max_x
        new_y = (robot["position"]["y"] + robot["velocity"]["y"] * seconds) % max_y
        return (new_x, new_y)

    def solve_a(self):
        (size_x, size_y) = (101, 103) if REMOTE else (11, 7)

        matrix = np.zeros((size_y, size_x), dtype=int)
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

        for robot in robots:
            (x, y) = self.move_robot(robot, 100, size_x, size_y)
            print(robot, x, y)
            matrix[y][x] += 1
            # input("Press Enter to continue...")  # Wait for user to press Enter

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

        print("Top Left Quadrant:")
        print(top_left)
        print("Top Right Quadrant:")
        print(top_right)
        print("Bottom Left Quadrant:")
        print(bottom_left)
        print("Bottom Right Quadrant:")
        print(bottom_right)

        return sum

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

# print(f"Solution A: {solution.solve_a()}")
print(f"Solution B: {solution.solve_b()}")
if SUBMIT:
    solution.submit(sub_a=True, sub_b=False)
