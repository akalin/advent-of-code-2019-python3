def can_be_password(n):
    digits = [int(d) for d in str(n)]
    found_pair = False
    found_pair_or_greater = False
    run_length = 1
    for x, y in zip(digits, digits[1:] + [10]):
        if y < x:
            return False, False
        elif y == x:
            run_length += 1
        else:
            if run_length >= 2:
                found_pair_or_greater = True
                if run_length == 2:
                    found_pair = True
            run_length = 1

    return found_pair_or_greater, found_pair

def compute_day04(input):
    min_n, max_n = [int(x) for x in input.split('-')][0:2]
    part1_count, part2_count = 0, 0
    for n in range(min_n, max_n+1):
        part1, part2 = can_be_password(n)
        if part1:
            part1_count += 1
        if part2:
            part2_count += 1
    return part1_count, part2_count

if __name__ == '__main__':
    with open('day04.input', 'r') as input_file:
        input = input_file.read()
        part1_count, part2_count = compute_day04(input)
        print(f'part 1 count: {part1_count} part 2 count: {part2_count}')
