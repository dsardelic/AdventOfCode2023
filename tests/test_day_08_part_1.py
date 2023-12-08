import unittest

from aoc2023 import day_08_part_1


class TestDay08Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_08_example.txt", 2),
            ("input/day_08_example1.txt", 6),
            ("input/day_08.txt", 19667),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_08_part_1.solution(input_file_rel_uri), exp_solution
                )
