def can_be_password(n):
    digits = [int(d) for d in str(n)]
    pairs = zip(digits, digits[1:])
    found_pair = False
    found_decrease = False
    curr_pair = 1
    for x, y in pairs:
        if x == y:
            curr_pair += 1
        else:
            if curr_pair == 2:
                found_pair = True
            curr_pair = 1
        if y < x:
            found_decrease = True
#        print(x, y, found_pair, found_decrease)
    if curr_pair == 2:
        found_pair = True
#    print(curr_pair, found_pair)
    return found_pair and not found_decrease

def compute_day04(input):
    min_n, max_n = [int(x) for x in input.split('-')][0:2]
    count = 0
    for n in range(min_n, max_n+1):
        if can_be_password(n):
            count += 1
    return count

if __name__ == '__main__':
    with open('day04.input', 'r') as input_file:
        input = input_file.read()
        for x in [111111, 223450, 123789, 112233, 123444, 111122]:
            print(f'{x} {can_be_password(x)}')
        output = compute_day04(input)
        print(f'output: {output}')
