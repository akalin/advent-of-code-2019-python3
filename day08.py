import itertools

def count_digits(layer, d):
    return sum([1 for x in layer if x == d])

def get_pixel(layers, i):
    for layer in layers:
        if layer[i] != '2':
            return layer[i]
    raise Exception('what')

def compute_day08(input, m, n):
    layers = [input[i*m*n:(i+1)*m*n] for i in range(len(input)//(m*n))]
    min_i = -1
    min_count = m*n
    for i, l in enumerate(layers):
        c = count_digits(l, '0')
        if c < min_count:
            min_i = i
            min_count = c
    p1 = count_digits(layers[min_i], '1') * count_digits(layers[min_i], '2')

    image = [get_pixel(layers, i) for i in range(m*n)]
    rows = [''.join(image[i*n:(i+1)*n]) for i in range(len(image)//m)]
    return rows

if __name__ == '__main__':
    with open('day08.input', 'r') as input_file:
        input = input_file.read()
        output = compute_day08(input, 25, 6)
        print(f'output: {output}')
