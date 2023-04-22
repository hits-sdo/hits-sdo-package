"""
Uses dataclasses to simplify attribute assignment..? read python guide
"""
from PIL import Image
from dataclasses import dataclass

@dataclass

class ParentTransformationsFromTile:
    """This will keep track of an output tile file"""

    parent_img_width: int
    parent_img_height: int

    parent_img_width_after_padding: int
    parent_img_height_after_padding: int

    parent_file_is_valid: bool
    parent_file_file_type: str
    parent_file_source: str



    def calc_padding_width(self, tile_pixel_width:int) -> tuple:
        """If the tile doesn't divide evenly into the parent width then calculates excess padding"""

        leftover_padding = self.parent_img_width % tile_pixel_width
        if leftover_padding == 0:
            return (0, 0)
        leftover_padding = tile_pixel_width - leftover_padding

        left_padding = leftover_padding // 2
        right_padding = leftover_padding - left_padding
        padding = (left_padding, right_padding)
        return padding

    def calc_padding_height(self, tile_pixel_height:int) -> tuple:
        """If the tile doesn't divide evenly into the parent height,
        then calculates excess padding"""

        leftover_padding = self.parent_img_height % tile_pixel_height
        if leftover_padding == 0:
            return (0, 0)

        leftover_padding = tile_pixel_height - leftover_padding

        top_padding = leftover_padding // 2
        bottom_padding = leftover_padding - top_padding
        padding = (top_padding, bottom_padding)
        return padding

    def calc_corner_pieces(self, tile_pixel_width:int, tile_pixel_height:int) -> tuple:
        """Using the padding from width and height to
            calculate the padding for the corners of the image.
            Returns a tuple of 2 tuples
        """
        pad_width = self.calc_padding_width(tile_pixel_width)
        pad_height = self.calc_padding_height(tile_pixel_height)

        top_left = pad_width[0] * pad_height[0]
        top_right = pad_width[1] * pad_height[0]
        bot_left = pad_width[0] * pad_height[1]
        bot_right = pad_width[1] * pad_height[1]
        corner_padding = ((top_left,top_right), (bot_left,bot_right))
        return corner_padding


    def calc_overall_padding(self, tile_pixel_width:int, tile_pixel_height:int) -> int:
        """using the amount of padding we need (now global variables) to calculate the number of
        pixels we need to add for padding also add in the width and height padding methods a
        statement to redefine the value of the padding variables"""
        calc_width = self.calc_padding_width(tile_pixel_width)
        calc_height = self.calc_padding_height(tile_pixel_height)
        left_width_padding_pixels = calc_width[0] * self.parent_img_height
        right_width_padding_pixels = calc_width[1] * self.parent_img_height
        top_height_padding_pixels = calc_height[0] * self.parent_img_width
        bottom_height_padding_pixels = calc_height[1] * self.parent_img_width

        corner_padding = self.calc_corner_pieces(tile_pixel_width, tile_pixel_height)

        total_padding = left_width_padding_pixels + top_height_padding_pixels + \
                        right_width_padding_pixels + bottom_height_padding_pixels + \
                        corner_padding[0][0] + corner_padding[0][1] + corner_padding[1][0] + \
                              corner_padding[1][1]

        return total_padding
    
    def generate_file_name_from_parent(self):
        raise NotImplementedError


    def export_padded_parent_meta(self):
        pass





    def export_padded_parent_to_file(self, filepath_output:str, tile_pixel_width:int, tile_pixel_height:int)->bool:
        
        try:
            parent_image = Image.open(self.parent_file_source)
            new_size = (self.parent_img_width_after_padding, self.parent_img_height_after_padding)
            padded_parent_image = Image.new("RGB", new_size)
            box_param = (self.calc_padding_width(tile_pixel_width=tile_pixel_width), self.calc_padding_height(tile_pixel_height=tile_pixel_height))
            padded_parent_image = Image.paste(parent_image, box=box_param)
        #   new_name = generate_file_name_from_parent()
        #   padded_parent_image.save(new_name, format="JPG")
            padded_parent_image.save("blah.jpg", format="JPG")
        except:
            return False

            # FileNotFound exception


        return True


    
