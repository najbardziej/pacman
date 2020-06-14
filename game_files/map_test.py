"""Map module tests"""
import sys
import unittest
import parameterized

import constants, map


class MapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.map = map.Map("gamemap.txt")

    def test_setup(self):
        last_x = self.map.tiles[-1].x
        last_y = self.map.tiles[-1].y
        self.assertEqual(last_x, constants.GAMEMAP_WIDTH - 1)
        self.assertEqual(last_y, constants.GAMEMAP_HEIGHT - 1)
        self.assertEqual((last_x + 1) * constants.TILE_SIZE,
                         constants.GAMEMAP_WIDTH_PX)
        self.assertEqual((last_y + 1) * constants.TILE_SIZE,
                         constants.GAMEMAP_HEIGHT_PX)
        self.assertEqual(self.map.total_pellets, 244)

    @parameterized.parameterized.expand([
        [(0, 0), constants.WALL],
        [(0, 30), constants.WALL],
        [(27, 0), constants.WALL],
        [(27, 30), constants.WALL],
        [(1, 1), constants.PELLET],
        [(26, 23), constants.POWER_PELLET],
        [(12, 23), constants.INTERSECTION2],
    ])
    def test_get_tile(self, input_value, expected_value):
        x, y = input_value
        self.assertEqual(self.map.get_tile(x, y), expected_value)

    @parameterized.parameterized.expand([
        ['s', (13, 23)],
        ['b', (13, 11)],
        ['p', (13, 14)],
        ['i', (11, 14)],
        ['c', (15, 14)],
    ])
    def test_get_coordinates(self, input_value, expected_value):
        self.assertEqual(self.map.get_coordinates(input_value), expected_value)

    def test_get_pellets(self):
        pellets = sum(1 for i in self.map.get_pellets()
                      if i.cell == constants.PELLET or
                      i.cell == constants.INTERSECTION2)
        self.assertEqual(pellets, 240)
        power_pellets = sum(1 for i in self.map.get_pellets()
                        if i.cell == constants.POWER_PELLET)
        self.assertEqual(power_pellets, 4)

    def test_get_barriers(self):
        barriers = sum(1 for i in self.map.get_barriers())
        self.assertEqual(barriers, 2)
        self.assertIn(self.map.get_coordinates("e"),
                      self.map.get_barriers())

    @parameterized.parameterized.expand([
        [(22, 9,  0)],
        [(5,  2,  1)],
        [(27, 30, 2)],
        [(20, 27, 3)],
        [(27, 2,  4)],
        [(3,  27, 5)],
    ])
    def test_get_walls(self, expected_value):
        self.assertIn(expected_value, self.map.get_walls())


if __name__ == "__main__":
    unittest.main()