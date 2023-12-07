import unittest

from aoc2023 import day_07_part_2


class TestDay07Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_07_example.txt", 5905),
            ("input/day_07.txt", 252113488),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_07_part_2.solution(input_file_rel_uri), exp_solution
                )
