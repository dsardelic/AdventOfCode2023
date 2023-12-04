import unittest

from aoc2023 import day_04_part_2


class TestDay04Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_04_example.txt", 30),
            ("input/day_04.txt", 23806951),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_04_part_2.solution(input_file_rel_uri), exp_solution
                )
