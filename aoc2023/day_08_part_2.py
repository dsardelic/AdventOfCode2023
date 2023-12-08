import collections
import itertools
import re

CycleEntryData = collections.namedtuple(
    "CycleEntryData", "entry_node instruction_index cycle_period steps_before_entry"
)


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        instructions, node_to_neighbors_lines = ifile.read().split("\n\n")

    instructions = tuple(
        int(char) for char in instructions.replace("L", "0").replace("R", "1")
    )

    node_to_neighbors = {
        match_.group(1): (match_.group(2), match_.group(3))
        for line in node_to_neighbors_lines.split("\n")
        if (match_ := re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line))
    }

    start_nodes = tuple(node for node in node_to_neighbors if node[2] == "A")

    cycle_entry_data_per_node = {
        start_node: cycle_entry_data(start_node, node_to_neighbors, instructions)
        for start_node in start_nodes
    }

    max_steps_before_cycle_entry = max(
        cycle_entry_data.steps_before_entry
        for cycle_entry_data in cycle_entry_data_per_node.values()
    )

    # one z-distance for each z-node in the cycle
    z_distances_per_node = {
        start_node: entry_node_z_distances(
            cycle_entry_data.entry_node,
            node_to_neighbors,
            (
                *instructions[cycle_entry_data.instruction_index :],
                *instructions[: cycle_entry_data.instruction_index],
            ),
            cycle_entry_data.cycle_period,
        )
        for start_node, cycle_entry_data in cycle_entry_data_per_node.items()
    }

    # those who entered a cycle early will move within the cycle until everybody is in
    for start_node in z_distances_per_node:
        steps_inside_cycle = (
            max_steps_before_cycle_entry
            - cycle_entry_data_per_node[start_node].steps_before_entry
        )
        # decrease distance to each z-node
        z_distances_per_node[start_node] = [
            z_distance
            - (steps_inside_cycle % cycle_entry_data_per_node[start_node].cycle_period)
            for z_distance in z_distances_per_node[start_node]
        ]
        # get rid of possible negative distances
        z_distances_per_node[start_node] = [
            z_distance % cycle_entry_data_per_node[start_node].cycle_period
            for z_distance in z_distances_per_node[start_node]
        ]

    # set up data for solving the linear system of congruences
    z_distances = list(
        itertools.product(
            *(z_distances_per_node[start_node] for start_node in start_nodes)
        )
    )
    cycle_periods = tuple(
        cycle_entry_data_per_node[start_node].cycle_period for start_node in start_nodes
    )
    return next(
        max_steps_before_cycle_entry + lsc_solution[0]
        for z_distance in z_distances
        if (
            lsc_solution := linear_system_of_congruences_solution(
                tuple(zip(z_distance, cycle_periods))
            )
        )
    )


def instruction_at_index(instructions, index):
    return instructions[index % len(instructions)]


def cycle_entry_data(start_node, node_to_neighbors, instructions):
    node = start_node
    distance_per_visited = {}
    steps = 0
    while True:
        neighbor = node_to_neighbors[node][instruction_at_index(instructions, steps)]
        to_be_executed_instruction_index = (steps + 1) % len(instructions)
        if prev_distance := distance_per_visited.get(
            (neighbor, to_be_executed_instruction_index)
        ):
            return CycleEntryData(
                entry_node=neighbor,
                instruction_index=to_be_executed_instruction_index,
                cycle_period=steps + 1 - prev_distance,
                steps_before_entry=prev_distance,
            )
        distance_per_visited[(neighbor, to_be_executed_instruction_index)] = steps + 1
        node = neighbor
        steps += 1


def entry_node_z_distances(entry_node, node_to_neighbors, instructions, cycle_period):
    # account for more than 1 z-node within a cycle
    node = entry_node
    z_distances = []
    for i in range(cycle_period):
        if node[2] == "Z":
            z_distances.append(i)
        node = node_to_neighbors[node][instruction_at_index(instructions, i)]
    return z_distances


def linear_system_of_congruences_solution(
    equations_data,
):  # pylint: disable=too-complex
    # pylint: disable=use-implicit-booleaness-not-comparison-to-zero,invalid-name,singleton-comparison,consider-using-assignment-expr
    """Taken over with love and gratitude from https://github.com/ZeroBone/chrem.\n
    Takes in a sequence of (a, m) pairs.\n
    Returns solutions for X in the form of (a, m) where X ≡ a (mod m).
    """

    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        if b == 0:
            return (a, 1, 0)
        unPrev = 1
        vnPrev = 0
        unCur = 0
        vnCur = 1
        while True:
            qn = a // b
            newR = a % b
            a = b
            b = newR
            if b == 0:
                return (a, unCur, vnCur)
            # Update coefficients
            unNew = unPrev - qn * unCur
            vnNew = vnPrev - qn * vnCur
            # Shift coefficients
            unPrev = unCur
            vnPrev = vnCur
            unCur = unNew
            vnCur = vnNew

    def chrem(congruence1, congruence2):
        (a1, n1) = congruence1
        (a2, n2) = congruence2
        (moduloGcd, u, v) = extended_gcd(n1, n2)
        if moduloGcd == 1:
            solution_ = n1 * a2 * u + n2 * a1 * v
            modulo = n1 * n2
            return (solution_ % modulo, modulo)
        if (a1 - a2) % moduloGcd != 0:
            # Unsolvable
            return None
        moduloLcm = (n1 // moduloGcd) * n2
        k = (a1 - a2) // moduloGcd
        solution_ = a1 - n1 * u * k
        return (solution_ % moduloLcm, moduloLcm)

    def chrem_multiple(congruences):
        solution_ = chrem(congruences[0], congruences[1])
        if solution_ == None:
            return None
        for congruence in congruences[2:]:
            solution_ = chrem(solution_, congruence)
            if solution_ == None:
                return None
        return solution_

    return chrem_multiple(equations_data)


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example2.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
