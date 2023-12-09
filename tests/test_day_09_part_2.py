import unittest

from aoc2023 import day_09_part_2


class TestDay09Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_09_example.txt", 2),
            ("input/day_09.txt", 903),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_09_part_2.solution(input_file_rel_uri), exp_solution
                )
