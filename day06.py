import networkx as nx

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

def make_graph(input):
    return nx.Graph(line.strip().split(')') for line in input.strip().split('\n'))

def count_orbits_nx(input):
    G = make_graph(input)
    return sum(nx.shortest_path_length(G, n, 'COM') for n in G.nodes)

def count_transfers_nx(input):
    G = make_graph(input)
    return nx.shortest_path_length(G, 'YOU', 'SAN') - 2

if __name__ == '__main__':
    with open('day06.input', 'r') as input_file:
        input = input_file.read()
        num_orbits = count_orbits(input)
        total_hops = count_transfers(input)
        print(f'num orbits: {num_orbits}, total hops: {total_hops}')
        num_orbits_nx = count_orbits_nx(input)
        total_hops_nx = count_transfers_nx(input)
        print(f'(nx) num orbits: {num_orbits_nx}, total hops: {total_hops_nx}')
