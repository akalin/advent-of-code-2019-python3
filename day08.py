def chunked(l, n):
    return [l[i*n:(i+1)*n] for i in range(len(l) // n)]

def get_pixel(layers, i):
    for layer in layers:
        if layer[i] != '2':
            return layer[i]
    raise Exception(f'couldn\'t find non-transparent pixel at pos {i}')

def compute_day08(input, m, n):
    layers = chunked(input, m*n)
    min_layer = min(layers, key=lambda l: l.count('0'))
    part1 = min_layer.count('1') * min_layer.count('2')

    image = [get_pixel(layers, i) for i in range(m*n)]
    rows = chunked(image, m)
    part2 = '\n'.join([''.join(r) for r in rows])
    return part1, part2

if __name__ == '__main__':
    with open('day08.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day08(input, 25, 6)
        print(f'part 1: {p1}, part 2 (squint to read):\n{p2}')
