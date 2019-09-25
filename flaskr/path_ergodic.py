# import matplotlib.pyplot as plt
import numpy as np

def path_plan(method, w=17, h=30):
    W_cell = w//10
    H_cell = h//10
    start_point = [W_cell / 2, H_cell / 2]
    areas = {}
    counter = 0
    last_i = 0
    last_j = 0
    Hph = int(np.ceil(h / H_cell))
    Wpw = int(np.ceil(w / W_cell))
    # fig, ax = plt.subplots()
    if 'tilt' in method:
        counter = [[0,0]] if 'row' in method else []
        control_order = 'i - j + 1' if 'row' in method else 'i - j'
        for i in range(Hph + Wpw):
            for j in range(Hph):
                if eval(control_order) >= Hph or eval(control_order) < 0:
                    continue
                if i % 2 == 0:
                    counter.append([eval(control_order), j])
                elif i % 2 != 0:
                    counter.append([j, eval(control_order)])
        counter = np.array(counter, dtype='float')
        counter[:, 0] *= W_cell
        counter[:, 1] *= H_cell
        counter[:, 0] += W_cell / 2
        counter[:, 1] += H_cell / 2
        counter = np.array(list(filter(lambda y: y[1] < h, filter(lambda x: x[0] < w, counter))))
        # plt.plot(counter[:, 0], counter[:, 1])
        # plt.scatter(counter[:, 0], counter[:, 1])
        # for i in range(counter.shape[0]):
        #     ax.annotate(i + 1, (counter[:, 0][i], counter[:, 1][i]))
        return counter
        # plt.show()
    else:
        if method == 'row':
            for j in range(0, h, H_cell):
                for i in range(0, w, W_cell):
                    start_point = [start_point[0] + i - last_i, start_point[1] + j - last_j]
                    areas[counter] = start_point
                    counter += 1
                    last_j = j
                    last_i = i
        if method == 'col':
            Wpw = int(np.ceil(h / H_cell))
            Hph = int(np.ceil(w / W_cell))
            for i in range(0, w, W_cell):
                for j in range(0, h, H_cell):
                    start_point = [start_point[0] + i - last_i, start_point[1] + j - last_j]
                    areas[counter] = start_point
                    counter += 1
                    last_j = j
                    last_i = i
        points = np.array(list(areas.values()))

        # plt.scatter(points[:, 0], points[:, 1])

        # for i in range(points.shape[0]):
        #     ax.annotate(i + 1, (points[:, 0][i], points[:, 1][i]))
        raw_list = []
        for i in range(Hph):
            raw_list.extend(list(range(i * Wpw, (i + 1) * Wpw))) if i % 2 == 0 else raw_list.extend(
                list(range((i + 1) * Wpw - 1, i * Wpw - 1, -1)))
        raw_ok = []
        for i in raw_list:
            raw_ok.append(areas[i])
        raw_ok = np.array(raw_ok)
        # plt.plot(raw_ok[:, 0], raw_ok[:, 1])
        # plt.show()
        return raw_ok

if __name__ == '__main__':
    a = path_plan('row')
    print(a)
    # path_plan('tilt row')
    # path_plan('row')
    # path_plan('col')