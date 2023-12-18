import unittest

from aoc2023 import day_19_part_1


class TestDay19Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_19_example.txt", 19114),
            ("input/day_19.txt", 418498),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_19_part_1.solution(input_file_rel_uri), exp_solution
                )
