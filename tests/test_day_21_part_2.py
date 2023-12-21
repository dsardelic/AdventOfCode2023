import unittest

from aoc2023 import day_21_part_2


class TestDay21Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            # ("input/day_21_example.txt", None),
            # ("input/day_21.txt", 601113643448699),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_21_part_2.solution(input_file_rel_uri), exp_solution
                )
