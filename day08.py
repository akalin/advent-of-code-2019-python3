import itertools

def get_pixel(layers, i):
    for layer in layers:
        if layer[i] != '2':
            return layer[i]
    raise Exception('what')

def compute_day08(input, m, n):
    layers = [input[i*m*n:(i+1)*m*n] for i in range(len(input)//(m*n))]
    min_layer = min(layers, key=lambda l: l.count('0'))
    part1 = min_layer.count('1') * min_layer.count('2')

    image = [get_pixel(layers, i) for i in range(m*n)]
    rows = [''.join(image[i*m:(i+1)*m]) for i in range(len(image)//m)]
    return part1, '\n'.join(rows)

if __name__ == '__main__':
    with open('day08.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day08(input, 25, 6)
        print(f'part 1: {p1}, part 2:\n{p2}')
