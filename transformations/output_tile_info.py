from dataclasses import dataclass

@dataclass

class TileItem:
    """This will keep track of an output tile file"""
    tile_name: str
    tile_image_type: str
    tile_is_valid: bool
    tile_time_stamp: str  #change to date/time later
    tile_f_out_path: str
    #tile_is_out_remote: bool
    tile_pixel_width: int
    tile_pixel_height: int
    is_padded: bool

    parent_img_width: int
    parent_img_height: int
    parent_file_isValid: bool
    parent_file_file_type: str
    parent_file_source: str

    def calc_padding_width(self) -> tuple:
        """If the tile doesn't divide evenly into the parent width, then calculates excess padding"""
        
        leftover_padding = self.parent_img_width % self.tile_pixel_width
        if leftover_padding == 0:
            return (0, 0)
        else:
            leftover_padding = self.tile_pixel_width - leftover_padding
        # returns 1
        # we want 2 to be returned
        
        """"""""""""""""
        3 (tile width) 

        need parent image to be divisible by 3.

        parent image has width of 25

            Two choices, 

                25 - 1 = 24 which is divisible by 3

                25 + 2 = 27 which is divisible by 3

                We need the second choice, but python returns the first one by default. 
                subtracting -1 is bad because it kills a pixel of our parent image.
                
                We would rather add extra pixels than removing pixels, as removing pixels
                might cause us to lose data.
        """

        left_padding = leftover_padding // 2
        right_padding = leftover_padding - left_padding
        padding = (left_padding, right_padding)
        return padding

