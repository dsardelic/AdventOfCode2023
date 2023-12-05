from collections import namedtuple

TranslationDataItem = namedtuple(
    "TranslationDataItem",
    "span_begin span_end min_translated_span_begin",
)


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        seeds_line, _, remaining_lines = ifile.read().partition("\n\n")
    spans_data = [int(number_str) for number_str in seeds_line.split(": ")[1].split()]
    spans = [
        (spans_data[i], spans_data[i] + spans_data[i + 1])
        for i in range(0, len(spans_data), 2)
    ]
    for line_group in remaining_lines.split("\n\n"):
        translation_data = [
            TranslationDataItem(
                span_begin=line_numbers[1],
                span_end=line_numbers[1] + line_numbers[2],
                min_translated_span_begin=line_numbers[0],
            )
            for line in line_group.split("\n")[1:]
            if (line_numbers := [int(number_str) for number_str in line.split(" ")])
        ]
        spans = translate(spans, translation_data)
    return min(spans)[0]


def translate(spans, translation_data):  # pylint:disable=too-complex
    t_spans = []
    while spans:
        s_begin, s_end = spans.pop()
        for t_begin, t_end, min_t_span_begin in translation_data:
            if t_begin < s_begin:
                if s_begin < t_end < s_end:
                    t_spans.append(
                        (
                            min_t_span_begin + (s_begin - t_begin),
                            min_t_span_begin + (s_begin - t_begin) + (t_end - s_begin),
                        )
                    )
                    spans.append((t_end, s_end))
                    break
                if t_end >= s_end:
                    t_spans.append(
                        (
                            min_t_span_begin + (s_begin - t_begin),
                            min_t_span_begin + (s_begin - t_begin) + (s_end - s_begin),
                        )
                    )
                    break
            if t_begin == s_begin:
                if s_begin < t_end < s_end:
                    t_spans.append(
                        (
                            min_t_span_begin,
                            min_t_span_begin + (t_end - s_begin),
                        )
                    )
                    spans.append((t_end, s_end))
                    break
                if t_end >= s_end:
                    t_spans.append(
                        (
                            min_t_span_begin,
                            min_t_span_begin + (s_end - s_begin),
                        )
                    )
                    break
            if s_begin < t_begin < s_end:
                if t_end < s_end:
                    t_spans.append(
                        (
                            min_t_span_begin,
                            min_t_span_begin + (t_end - t_begin),
                        )
                    )
                    spans.append((s_begin, t_begin))
                    spans.append((t_end, s_end))
                    break
                if t_end >= s_end:
                    t_spans.append(
                        (
                            min_t_span_begin,
                            min_t_span_begin + (s_end - t_begin),
                        )
                    )
                    spans.append((s_begin, t_begin))
                    break
        else:
            t_spans.append((s_begin, s_end))
    return t_spans


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
