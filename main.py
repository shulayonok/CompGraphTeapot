import numpy as np
import matplotlib.pyplot as plt
import math as m

# Список для будущих вершин и граней
versh = []
gr = []

with open("teapot.obj", "r") as file:
    for line in file:
        if line.find("v") != -1:
            split = line.split()
            split.remove("v")    # Если в строке находится буква 'v', то делим строку по пробелам и
            split.pop(2)         # удаляем координату по z и
            versh.append(split)  # удаляем элемент списка с буквой, оставляя только координаты вершин (в строковом виде)
        elif line.find("f") != -1:
            split = line.split()
            split.remove("f")  # Та же ситуация с буквой 'f' и гранями
            gr.append(split)

# Превращаем списки в массивы, так как размерность уже известна
versh = np.array(versh, dtype=float)
gr = np.array(gr, dtype=int)  # Меняем тип данных массива с гранями со строкового на целочисленный

print(gr)

# Размер
n = 1920

# Создаём numpy массив размерности (N,N,3)
base_colour = 139  # DarkRed
img = np.zeros((n, n, 3), dtype=np.uint8)  # Изначально фон чёрный
for i in range(n):                         # Изменим цвет фона
    for j in range(n):
        for k in range(3):
            img[i][j][k] = 255

# Масштабируем до размера изображения
coord_x = []
for point in versh:
    coord_x.append(abs(point[0]))

coord_y = []
for point in versh:
    coord_y.append(abs(point[1]))

Max = max(coord_x)

int_points = []
for point in versh:
    point[0] += Max
    point[0] *= n / (2.1 * Max)
    point[1] += Max
    point[1] *= n / (2.1 * Max)
    point = (int(point[0]), int(point[1]))
    int_points.append(point)


# Алгоритм Брезенхема
def Bresenham(x0, y0, x1, y1, N, image, color):
    dx = x1 - x0
    dy = y1 - y0
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if abs(dx) > abs(dy):
        sx, sy, m_abs, b_abs = sign_x, 0, abs(dy), abs(dx)
    else:
        sx, sy, m_abs, b_abs = 0, sign_y, abs(dx), abs(dy)
    error = b_abs / 2
    image[N - 1 - int(y0), int(x0)] = [(color * (1 - m.sqrt((N / 2 - x0) ** 2 + (N / 2 - x0) ** 2) / N)), 0, 0]
    for i in range(b_abs):
        error -= m_abs
        if error < 0:
            error += b_abs
            x0 += sign_x
            y0 += sign_y
        else:
            x0 += sx
            y0 += sy
        image[N - 1 - int(y0), int(x0)] = [(color * (1 - m.sqrt((N / 2 - x0) ** 2 + (N / 2 - x0) ** 2) / N)), 0, 0]

# Его реализация
for g in gr:
    Bresenham(int_points[g[0] - 1][0], int_points[g[0] - 1][1], int_points[g[1] - 1][0],
              int_points[g[1] - 1][1], n, img, base_colour)
    print(int_points[g[0] - 1][0], int_points[g[0] - 1][1], int_points[g[1] - 1][0],
          int_points[g[1] - 1][1])
    Bresenham(int_points[g[1] - 1][0], int_points[g[1] - 1][1], int_points[g[2] - 1][0],
              int_points[g[2] - 1][1], n, img, base_colour)
    Bresenham(int_points[g[2] - 1][0], int_points[g[2] - 1][1], int_points[g[0] - 1][0],
              int_points[g[0] - 1][1], n, img, base_colour)

# Отображение и сохранение в файл
plt.figure()
plt.imshow(img)
plt.show()
plt.imsave('teapot.png', img)
