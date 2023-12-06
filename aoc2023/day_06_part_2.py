def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return number_of_ways_to_beat_the_race(
            *(int(line.strip("\n").replace(" ", "").split(":")[1]) for line in ifile)
        )


def number_of_ways_to_beat_the_race(time, record_distance):
    lo, hi = None, None
    i = 0
    while not (lo and hi):
        # observe speed * travel time
        if not lo and i * (time - i) > record_distance:
            lo = i
        if not hi and (time - i) * i > record_distance:
            hi = time - i
        i += 1
    return hi - lo + 1


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
