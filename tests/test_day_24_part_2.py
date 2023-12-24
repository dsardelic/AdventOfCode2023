import unittest

from aoc2023 import day_24_part_2


class TestDay24Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_24_example.txt", 47),
            ("input/day_24.txt", 765636044333842),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_24_part_2.solution(input_file_rel_uri), exp_solution
                )
