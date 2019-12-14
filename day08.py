from more_itertools import sliced

def compute_day08(input, m, n):
    layers = list(sliced(input.strip(), m*n))
    min_layer = min(layers, key=lambda l: l.count('0'))
    part1 = min_layer.count('1') * min_layer.count('2')

    image = [next(x for x in p if x != '2') for p in zip(*layers)]
    disp_image = ''.join(image).replace('0', ' ').replace('1', '⋅')
    part2 = '\n'.join([r for r in sliced(disp_image, m)])
    return part1, part2

if __name__ == '__main__':
    with open('day08.input', 'r') as input_file:
        input = input_file.read()
        p1, p2 = compute_day08(input, 25, 6)
        print(f'part 1: {p1}, part 2:\n{p2}')
