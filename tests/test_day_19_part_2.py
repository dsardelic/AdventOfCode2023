import unittest

from aoc2023 import day_19_part_2


class TestDay19Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_19_example.txt", 167409079868000),
            ("input/day_19.txt", 123331556462603),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_19_part_2.solution(input_file_rel_uri), exp_solution
                )
