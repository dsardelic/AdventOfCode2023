# pylint: disable=eval-used

import dataclasses


@dataclasses.dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def xmas_rating(self):
        return sum(dataclasses.astuple(self))


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        workflow_to_rules_lines, parts_lines = ifile.read().split("\n\n")
    workflow_to_rules = {
        workflow_tokens[0]: tuple(parse_rules(workflow_tokens[1]))
        for line in workflow_to_rules_lines.split("\n")
        if (workflow_tokens := line.replace("}", "").split("{"))
    }
    parts = (
        eval(Part.__name__ + line.replace("{", "(").replace("}", ")"))
        for line in parts_lines.split("\n")
    )
    return sum(
        part.xmas_rating()
        for part in parts
        if is_accepted_part(part, workflow_to_rules)
    )


def parse_rules(rules_str):
    for rule_str in rules_str.split(","):
        if len(tokens := rule_str.split(":")) == 2:
            yield tuple(tokens)
        else:
            yield (None, tokens[0])


def is_accepted_part(part, workflow_to_rules):  # pylint: disable=unused-argument
    rules = iter(workflow_to_rules["in"])
    while True:
        condition, next_workflow = next(rules)
        if condition and not eval("part." + condition):
            # continue with the same workflow
            continue
        if next_workflow == "A":
            return True
        if next_workflow == "R":
            return False
        rules = iter(workflow_to_rules[next_workflow])


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
