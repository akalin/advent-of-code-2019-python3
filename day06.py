def count_orbits(input):
    pairs = [ line.strip().split(')') for line in input.strip().split('\n') ]
    parents = { child: parent for parent, child in pairs }

    num_orbits = 0
    for child in parents.keys():
        x = child
        while x in parents:
            num_orbits += 1
            x = parents[x]

    return num_orbits

def count_transfers(input):
    lines = input.strip().split('\n')
    orbits = {}

    for line in lines:
        orbitee, orbiter = line.strip().split(')')
        orbits[orbiter] = orbitee

    hit = {}
    hops = 0
    x = orbits['YOU']
    while x in orbits:
        hit[x] = hops
        hops += 1
        x = orbits[x]

    x = orbits['SAN']
    total_hops = 0
    while x in orbits:
        if x in hit:
            total_hops += hit[x]
            break
        total_hops += 1
        x = orbits[x]

    return total_hops

if __name__ == '__main__':
    with open('day06.input', 'r') as input_file:
        input = input_file.read()
        num_orbits = count_orbits(input)
        total_hops = count_transfers(input)
        print(f'num orbits: {num_orbits}, total hops: {total_hops}')
