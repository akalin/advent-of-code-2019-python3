def make_parents(input):
    pairs = [ line.strip().split(')') for line in input.strip().split('\n') ]
    parents = { child: parent for parent, child in pairs }
    return parents

def count_orbits(input):
    parents = make_parents(input)

    num_orbits = 0
    for child in parents.keys():
        x = child
        while x in parents:
            num_orbits += 1
            x = parents[x]

    return num_orbits

def count_transfers(input):
    parents = make_parents(input)

    hops_from_you = {}

    hops = 0
    x = parents['YOU']
    while x in parents:
        hops_from_you[x] = hops
        hops += 1
        x = parents[x]

    hops = 0
    x = parents['SAN']
    while x in parents:
        if x in hops_from_you:
            return hops + hops_from_you[x]
        hops += 1
        x = parents[x]

    raise Error('not connected')

if __name__ == '__main__':
    with open('day06.input', 'r') as input_file:
        input = input_file.read()
        num_orbits = count_orbits(input)
        total_hops = count_transfers(input)
        print(f'num orbits: {num_orbits}, total hops: {total_hops}')
