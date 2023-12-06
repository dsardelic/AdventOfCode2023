import unittest

from aoc2023 import day_06_part_2


class TestDay06Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_06_example.txt", 71503),
            ("input/day_06.txt", 36872656),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_06_part_2.solution(input_file_rel_uri), exp_solution
                )
