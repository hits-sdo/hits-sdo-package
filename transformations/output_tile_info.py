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

    def calc_padding_height(self) -> tuple:
        """If the tile doesn't divide evenly into the parent height, then calculates excess padding"""
        
        leftover_padding = self.parent_img_height % self.tile_pixel_height
        if leftover_padding == 0:
            return (0, 0)
        else:
            leftover_padding = self.tile_pixel_height - leftover_padding
       
        top_padding = leftover_padding // 2
        bottom_padding = leftover_padding - top_padding
        padding = (top_padding, bottom_padding)
        return padding
    
    def calc_overall_padding(self):
        raise NotImplementedError

        # team yellow - parent: 1024 x 1024 
        # - tiles: 64 x 64

        # team red - We don't actually need to save the tiles as long as we have the (width x height)
        # and (starting row x starting column)

        #=======Intention for Fri 3/31/23=======
        # using the amount of padding we need (now global variables) to calculate
        # the number of pixels we need to add for padding
        # also add in the width and height padding methods a statement to redefine
        # the value of the padding variables