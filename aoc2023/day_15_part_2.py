def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        return focusing_power(hashmap(ifile.read().split(",")))


def hash_(step):
    s = 0
    for char in step:
        s = (s + ord(char)) * 17 % 256
    return s


def hashmap(steps):
    lens_configuration = [{} for _ in range(256)]
    for step in steps:
        label, operation, focal_length = step.partition("=")
        if not operation:
            label, operation, focal_length = step.partition("-")
        if operation == "=":
            lens_configuration[hash_(label)][label] = int(focal_length)
        else:
            lens_configuration[hash_(label)].pop(label, None)
    return lens_configuration


def focusing_power(lens_configuration):
    return sum(
        box_value * slot_number * focal_length
        for box_value, box in enumerate(lens_configuration, 1)
        for slot_number, focal_length in enumerate(box.values(), 1)
    )


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
