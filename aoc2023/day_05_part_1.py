def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        seeds_line, _, remaining_lines = ifile.read().partition("\n\n")
    numbers = [int(number_str) for number_str in seeds_line.split(": ")[1].split()]
    for line_group in remaining_lines.split("\n\n"):
        span_to_translator = {}
        for line in line_group.split("\n")[1:]:
            new_span_begin, span_begin, span_length = (
                int(number_str) for number_str in line.split(" ")
            )
            span_to_translator[
                (span_begin, span_begin + span_length)
            ] = lambda el, nsb=new_span_begin, sb=span_begin: nsb + (el - sb)
        numbers = [translate(element, span_to_translator) for element in numbers]
    return min(numbers)


def translate(element, span_to_translator):
    return next(
        (
            translator(element)
            for span, translator in span_to_translator.items()
            if element in range(*span)
        ),
        element,
    )


if __name__ == "__main__":
    print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    # print(solution(f"input/{__file__[-16:][:6]}.txt"))
