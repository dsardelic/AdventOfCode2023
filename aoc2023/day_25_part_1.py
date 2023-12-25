import collections
import math
import random


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        graph = collections.defaultdict(
            list,
            {
                node: neighbors
                for line in ifile
                if (tokens := line.strip("\n").split(": "))
                and (node := tokens[0])
                and (neighbors := tokens[1].split(" "))
            },
        )

    # account for any incomplete edges
    for node in list(graph):
        for neighbor in graph[node]:
            if node not in graph[neighbor]:
                graph[neighbor].append(node)

    while not (
        supernode_to_component_group := karger_minimal_cut(
            graph={node: list(neighbors) for node, neighbors in graph.items()},
            target_cut_size=3,
            target_groups_len=2,
        )
    ):
        pass
    return math.prod(
        len(component_group)
        for component_group in supernode_to_component_group.values()
    )


def karger_minimal_cut(graph, target_cut_size, target_groups_len):
    # Using Karger's algorithm

    # Code backbone taken over with love and appreciation from
    # https://gist.github.com/meisly/7260c6a2dcea10666a8aa1c358318813

    def contract_graph(absorber, absorbed, supernode_to_component_group):
        for absorbed_neighbor in graph[absorbed]:
            if absorbed_neighbor != absorber:
                graph[absorber].append(absorbed_neighbor)
                graph[absorbed_neighbor].append(absorber)
            graph[absorbed_neighbor].remove(absorbed)
        supernode_to_component_group[absorber] |= supernode_to_component_group[absorbed]
        del supernode_to_component_group[absorbed]
        del graph[absorbed]

    supernode_to_component_group = {node: {node} for node in graph}
    while len(graph) > target_groups_len:
        absorber = random.choice(list(graph.keys()))
        absorbed = random.choice(graph[absorber])
        contract_graph(absorber, absorbed, supernode_to_component_group)
    if len(next(iter(graph.values()))) > target_cut_size:
        return None
    return supernode_to_component_group


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
