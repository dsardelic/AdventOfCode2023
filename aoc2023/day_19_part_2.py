import collections
import math

MIN_RATING = 1
MAX_RATING = 4000

Condition = collections.namedtuple("Condition", "rating operator limit")

Rule = collections.namedtuple("Rule", "condition next_workflow")


def solution(input_rel_uri):
    with open(input_rel_uri, encoding="utf-8") as ifile:
        workflow_to_rules = {
            workflow_tokens[0]: tuple(parse_rules(workflow_tokens[1]))
            for line in ifile.read().split("\n\n")[0].split("\n")
            if (workflow_tokens := line.replace("}", "").split("{"))
        }
    return sum(
        math.prod(len(part_category[rating]) for rating in "xmas")
        for part_category in acceptable_part_categories(workflow_to_rules)
    )


def parse_rules(rules_str):
    for rule_str in rules_str.split(","):
        rating, operator, limit = None, None, None
        if len(tokens := rule_str.split(":")) == 2:
            condition_str, next_workflow = tokens
            rating, operator, limit = condition_str.partition("<")
            if not operator:
                rating, operator, limit = condition_str.partition(">")
            condition = Condition(rating, operator, int(limit))
        else:
            next_workflow = tokens[0]
            condition = None
        yield Rule(condition, next_workflow)


def acceptable_part_categories(workflow_to_rules):
    acceptable = {rating: set(range(MIN_RATING, MAX_RATING + 1)) for rating in "xmas"}
    stack = [(acceptable, iter(workflow_to_rules["in"]))]
    while stack:
        category, rules = stack.pop()
        condition, next_workflow = next(rules, None)
        if condition:
            rating, operator, limit = condition
            failed = {k: set(v) for k, v in category.items()}
            if operator == "<":
                category[rating] &= set(range(1, limit))
                failed[rating] &= set(range(limit, MAX_RATING + 1))
            else:  # operator == ">"
                category[rating] &= set(range(limit + 1, MAX_RATING + 1))
                failed[rating] &= set(range(1, limit + 1))
            stack.append((failed, rules))
        if next_workflow == "A":
            yield category
        elif next_workflow != "R":
            stack.append((category, iter(workflow_to_rules[next_workflow])))


if __name__ == "__main__":
    # print(solution(f"input/{__file__[-16:][:6]}_example.txt"))
    print(solution(f"input/{__file__[-16:][:6]}.txt"))
