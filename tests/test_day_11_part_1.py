import unittest

from aoc2023 import day_11_part_1


class TestDay11Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_11_example.txt", 374),
            ("input/day_11.txt", 10422930),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_11_part_1.solution(input_file_rel_uri), exp_solution
                )
