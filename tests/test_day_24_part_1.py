import unittest

from aoc2023 import day_24_part_1


class TestDay24Part1(unittest.TestCase):
    def test_solution(self):
        data = (
            ("input/day_24_example.txt", 7, 27, 2),
            ("input/day_24.txt", 200000000000000, 400000000000000, 15558),
        )
        for input_file_rel_uri, min_boundary, max_boundary, exp_solution in data:
            with self.subTest(input_file=input_file_rel_uri):
                self.assertEqual(
                    day_24_part_1.solution(
                        input_file_rel_uri, min_boundary, max_boundary
                    ),
                    exp_solution,
                )
