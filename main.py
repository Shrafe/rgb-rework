from math import hypot
import random
import sys
import wx
from PIL import Image
import numpy as np

try:
    import octree_c as octree
    print('using C octree')
except Exception:
    import octree
    print('using Python octree')

SIZE = 4096

def load_target(path):
    target = Image.open(path)
    data = np.array(target)
    print(f'image shape: {data.shape}')
    print(f'first element: {data[0]}')
    # r, g, b = data[::3], data[1::3], data[2::3]
    return data

def load_indexes():
    indexes = list(range(SIZE * SIZE))
    random.shuffle(indexes)
    # indexes = sorted(indexes, key=index_func)
    return indexes

def create_image_data(colors):
    result = [None] * (SIZE * SIZE)
    for index, (r, g, b) in enumerate(colors):
        result[index] = chr(r) + chr(g) + chr(b)
    return ''.join(result)

def rgb_int(colors):
    return [(r << 16) | (g << 8) | (b) for r, g, b in colors]

def int_rgb(colors):
    result = []
    for color in colors:
        r = 0xff & (color >> 16)
        g = 0xff & (color >> 8)
        b = 0xff & (color >> 0)
        result.append((r, g, b))
    return result

def main(path):
    app = wx.App()
    print('loading target image')
    target = load_target(path)
    reshapedTarget = target.reshape(4096*4096, 3)
    print('loading indexes')
    indexes = load_indexes()
    print('initializing octree')
    tree = octree.Octree()
    print('picking colors')
    colors = np.zeros([SIZE*SIZE,3], dtype=np.uint8)
    for i, index in enumerate(indexes):
        if i % 65536 == 0:
            pct = 100.0 * i / (SIZE * SIZE)
            print('{:.2f}'.format(pct)+' percent complete')
        value = tree.pop(*reshapedTarget[index])
        colors[index] = [value[0], value[1], value[2]]
    print('creating output image')
    # data = create_image_data(colors)
    image = Image.fromarray(np.array(colors.reshape(SIZE, SIZE, 3)))
    image.save('output.png')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py input.png')
    else:
        # array = np.zeros([SIZE*SIZE,3], dtype=np.uint8)
        # print(array)
        # print(array.reshape(SIZE*SIZE,3))
        # print(array.flatten())
        # img = Image.fromarray(array)
        # img.save('testrgb.png') 
        main(sys.argv[1])
