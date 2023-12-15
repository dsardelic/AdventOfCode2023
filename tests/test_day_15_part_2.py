import unittest

from aoc2023 import day_15_part_2


class TestDay15Part2(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_15_example.txt", 145),
            ("input/day_15.txt", 239484),
        )
        for input_file_rel_uri, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_15_part_2.solution(input_file_rel_uri), exp_solution
                )
