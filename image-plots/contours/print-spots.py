
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import animation


def print_usage():
    print(sys.argv[0] + " <point-list-file>")

def main():
#    print(sys.argv[0])

    if (len(sys.argv) == 1):
        print_usage()
        sys.exit(100)

    piont_files = sys.argv[1]
    if (not os.path.exists(piont_files)):
        print("[" + piont_files + "] not found.")
        sys.exit(101)

    polys = []
    with open(piont_files) as fp:
        Xs = []
        Ys = []
        for line in fp:
            if (len(line.strip()) == 0):
                Xs.append(Xs[0])
                Ys.append(Ys[0])
                poly = [Xs, Ys]
                polys.append(poly)
                Xs = []
                Ys = []
            else:
                points_str = line.strip().split(" ")
                pt = [int(p) for p in points_str]
                Xs.append(pt[0])
                Ys.append(pt[1])
        Xs.append(Xs[0])
        Ys.append(Ys[0])
        poly = [Xs, Ys]
        polys.append(poly)


    fig = plt.figure()
    plt.xlabel('x')
    plt.ylabel('y')

    for poly in polys:
        plt.plot(poly[0], poly[1])

    ax = plt.gca()
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    plt.title('points')

#    print(polys[3])
#    scat = ax.scatter(polys[3][0][0], polys[3][1][0])

#    print(polys)

    print_points = []
    for p_arr in polys:
        xs = p_arr[0]
        ys = p_arr[1]
        for i in range(len(xs)):
            p = [xs[i], ys[i]]
            print_points.append(p)

    def update_points(frame):
        return ax.scatter(print_points[frame][0], print_points[frame][1])

    ani=animation.FuncAnimation(fig, update_points, frames=len(print_points), interval=30)

    plt.show()

if __name__ == "__main__":
    main()
