from math import hypot
import random
import sys
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
    return data

def load_indexes():
    indexes = list(range(SIZE * SIZE))
    random.shuffle(indexes)
    return indexes

def main(path):
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
    image = Image.fromarray(np.array(colors.reshape(SIZE, SIZE, 3)))
    image.save('output.png')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python main.py input.png')
    else:
        main(sys.argv[1])
