import unittest

from aoc2023 import day_23_part_2


class TestDay23Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_23_example.txt", 154),
            ("input/day_23.txt", 6622),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_23_part_2.solution(input_file_rel_uri), exp_solution
                )
