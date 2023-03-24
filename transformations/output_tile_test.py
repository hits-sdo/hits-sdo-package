import unittest
import output_tile_info
import pyprojroot


class Test_Tile_Items(unittest.TestCase):
    def setUp(self) -> None:
        """This class contains the unit tests that the tile object is valid."""
        self.tile_item = output_tile_info.TileItem( 
            tile_name="Name", 
            tile_image_type="jpeg", 
            tile_is_valid=False,
            tile_time_stamp="blah",  
            tile_f_out_path=pyprojroot.here(),  
            tile_pixel_width=3,
            tile_pixel_height=2,
            is_padded=False,
            parent_img_width=25,
            parent_img_height=4,
            parent_file_isValid=True,
            parent_file_file_type="blah",
            parent_file_source="blah")

    def test_tile_division_width(self):
        """This test will check if the tiles width evenly divides into the parent image(s) width"""
        self.assertTrue(self.tile_item.parent_img_width % self.tile_item.tile_pixel_width == 0)

    def test_tile_division_height(self):
        """This test will check if the tiles height evenly divides into the parent image(s) height"""
        self.assertTrue(self.tile_item.parent_img_height % self.tile_item.tile_pixel_height == 0)

    def test_tile_smaller_than_parent_width(self):
        """check to see if tile dimensions are less than parents dimensions"""
        self.assertTrue(self.tile_item.tile_pixel_width < self.tile_item.parent_img_width) 
    
    def test_tile_smaller_than_parent_height(self):
        """check to see if tile dimensions are less than parents dimensions"""
        self.assertTrue(self.tile_item.tile_pixel_height < self.tile_item.parent_img_height)

    def test_return_value_from_CPW(self):
        self.assertEqual((1,1), self.tile_item.calc_padding_width())
        print(self.test_tile_smaller_than_parent_width)

if __name__ == "__main__":
    unittest.main()
