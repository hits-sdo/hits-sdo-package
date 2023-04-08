"""
Unittest to test functionality of our functions.
Importing parent_transform_from_tile so that we can access data members
Pyprojroot so we can work with relative paths instead of absolute paths
"""
import unittest
# import pyprojroot # in case we do need it
import parent_transform_from_tile


class TestParentTransformationsFromTile(unittest.TestCase):
    """
    Class to Test Parent Transformation From Tile
    This class contains the unit tests that the tile object is valid.
    """
    def setUp(self) -> None:
        """This function declares our variables"""
        self.parent_transform = parent_transform_from_tile.ParentTransformationsFromTile(
            #tile_pixel_width=3,
            #tile_pixel_height=2,
            parent_img_width=27,
            parent_img_height=4,
            parent_img_width_after_padding=0,
            parent_img_height_after_padding=0,
            parent_file_isValid=True,
            parent_file_file_type="blah",
            parent_file_source="blah")

    def test_tile_division_width(self):
        """This test will check if the tile's width evenly divides into the parent image(s) width"""
        self.assertTrue(self.parent_transform.parent_img_width % \
                        self.parent_transform.tile_pixel_width == 0)

    def test_tile_division_height(self):
        """This test will check if the tile's height 
        evenly divides into the parent image(s) height"""
        self.assertTrue(self.parent_transform.parent_img_height % \
                        self.parent_transform.tile_pixel_height == 0)

    def test_tile_smaller_than_parent_width(self):
        """check to see if tile dimensions are less than parents dimensions"""
        self.assertTrue(self.parent_transform.tile_pixel_width < \
                        self.parent_transform.parent_img_width)

    def test_tile_smaller_than_parent_height(self):
        """check to see if tile dimensions are less than parents dimensions"""
        self.assertTrue(self.parent_transform.tile_pixel_height < \
                        self.parent_transform.parent_img_height)

    def test_correct_padding_width(self):
        """function to test member function of TileItem which calculates padding width 
        to add null pixels to both columns ensuring the sun is centered."""
        print("\n\n\n", self.test_tile_smaller_than_parent_width, "\n\n\n")
        (test_left_padding, test_right_padding) = self.parent_transform.calc_padding_width()
        temp = (self.parent_transform.parent_img_width + test_left_padding + test_right_padding) % \
            self.parent_transform.tile_pixel_width
        self.assertEqual(0, temp)

    def test_correct_padding_height(self):
        """function to test member function of TileItem which calculates padding height 
        to add null pixels to both columns ensuring the sun is centered."""
        print("\n\n\n", self.test_tile_smaller_than_parent_height, "\n\n\n")
        (test_top_padding, test_bottom_padding) = self.parent_transform.calc_padding_height()
        temp = (self.parent_transform.parent_img_height + test_top_padding + test_bottom_padding) \
            % self.parent_transform.tile_pixel_height
        self.assertEqual(0, temp)

        self.parent_transform.tile_pixel_height = 5
        self.parent_transform.parent_img_height = 45
        self.assertEqual(self.parent_transform.calc_padding_height(), (0,0))

    def test_correct_padding(self):
        """function to test the calculated height and width is correct"""
        self.parent_transform.parent_img_height = 42
        self.parent_transform.parent_img_width = 40
        self.parent_transform.tile_pixel_height = 5
        self.parent_transform.tile_pixel_width = 7
        self.assertEqual(self.parent_transform.calc_padding_height(), (0,0))

if __name__ == "__main__":
    unittest.main()
