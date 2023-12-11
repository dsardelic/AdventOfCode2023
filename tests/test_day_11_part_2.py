import unittest

from aoc2023 import day_11_part_2


class TestDay11Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_11_example.txt", 10, 1030),
            ("input/day_11_example.txt", 100, 8410),
            ("input/day_11.txt", 1000000, 699909023130),
        )
        for input_file_rel_uri, shift_magnitude, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                day_11_part_2.SHIFT_MAGNITUDE = shift_magnitude
                self.assertEqual(
                    day_11_part_2.solution(input_file_rel_uri), exp_solution
                )
