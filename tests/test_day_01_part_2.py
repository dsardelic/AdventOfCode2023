import unittest

from aoc2023 import day_01_part_2


class TestDay01Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_01_example1.txt", 281),
            ("input/day_01.txt", 54706),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_01_part_2.solution(input_file_rel_uri), exp_solution
                )
