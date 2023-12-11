import itertools


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        space = tuple(line.strip("\n") for line in ifile)
    return total_distance_between_galaxies(space)


def total_distance_between_galaxies(space):
    galaxies = tuple(
        (x, y)
        for x, space_row in enumerate(space)
        for y, content in enumerate(space_row)
        if content == "#"
    )
    galaxies = shift_coordinates(galaxies, space)
    return sum(
        abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        for g1, g2 in itertools.combinations(galaxies, 2)
    )


def shift_coordinates(galaxies, space):
    galaxy_to_shifted_galaxy = {galaxy: list(galaxy) for galaxy in galaxies}
    for x, row in enumerate(space):
        if not sum(content == "#" for content in row):
            for galaxy in galaxies:
                if galaxy[0] > x:
                    galaxy_to_shifted_galaxy[galaxy][0] += 1
    for y in range(len(space[0])):
        if not sum(space_row[y] == "#" for space_row in space):
            for galaxy in galaxies:
                if galaxy[1] > y:
                    galaxy_to_shifted_galaxy[galaxy][1] += 1
    return galaxy_to_shifted_galaxy.values()


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
