import unittest

from aoc2023 import day_20_part_1


class TestDay20Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_20_example.txt", 32000000),
            ("input/day_20_example1.txt", 11687500),
            ("input/day_20.txt", 912199500),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_20_part_1.solution(input_file_rel_uri), exp_solution
                )
