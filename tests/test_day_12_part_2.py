import unittest

from aoc2023 import day_12_part_2


class TestDay12Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_12_example.txt", 525152),
            ("input/day_12.txt", 15454556629917),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_12_part_2.solution(input_file_rel_uri), exp_solution
                )
