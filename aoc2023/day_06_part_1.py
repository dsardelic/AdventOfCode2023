import math
import re


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return math.prod(
            number_of_ways_to_beat_the_race(time, record_distance)
            for time, record_distance in zip(
                *(
                    (int(number) for number in re.findall(r"\d+", line))
                    for line in ifile
                )
            )
        )


def number_of_ways_to_beat_the_race(time, record_distance):
    return sum(
        (time - charging_time) * charging_time > record_distance
        for charging_time in range(time + 1)
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
