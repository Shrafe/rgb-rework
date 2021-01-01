from itertools import product
import sys
from PIL import Image
import numpy as np


def verify(path):
    image = Image.open(path)
    data = np.array(image)
    print(f'image shape: {data.shape}')
    print(f'first element: {data[0]}')
    if any(x < 0 or x > 255 for x in data.flatten()):
        raise Exception('Invalid: Values must be 0 <= x < 256.')
    rgb = data.reshape(4096*4096, 3)
    mappable = map(tuple, rgb)
    if len(rgb) != len(set(mappable)):
        raise Exception('Invalid: There are duplicate colors.')
    print('Valid!')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python verify.py input.png')
    else:
        verify(sys.argv[1])
