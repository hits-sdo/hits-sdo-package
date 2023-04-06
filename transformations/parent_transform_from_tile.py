from dataclasses import dataclass

@dataclass

class ParentTransformationsFromTile:
    """This will keep track of an output tile file"""

    parent_img_width: int
    parent_img_height: int

    parent_img_width_after_padding: int
    parent_img_height_after_padding: int

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
    
    def calc_corner_pieces(self) -> tuple:
        
        padWidth = self.calc_padding_width()
        padHeight = self.calc_padding_height()
        
        topLeft = padWidth[0] * padHeight[0]
        topRight = padWidth[1] * padHeight[0]
        BotLeft = padWidth[0] * padHeight[1]
        BotRight = padWidth[1] * padHeight[1]
        corner_padding = ((topLeft,topRight), (BotLeft,BotRight))
        return corner_padding


    def calc_overall_padding(self) -> int: 
        """using the amount of padding we need (now global variables) to calculate the number of 
        pixels we need to add for padding also add in the width and height padding methods a 
        statement to redefine the value of the padding variables"""

        left_width_padding_pixels = self.calc_padding_width()[0] * self.parent_img_height
        right_width_padding_pixels = self.calc_padding_width()[1] * self.parent_img_height
        top_height_padding_pixels = self.calc_padding_height()[0] * self.parent_img_width
        bottom_height_padding_pixels = self.calc_padding_height()[1] * self.parent_img_width

        corner_padding = self.calc_corner_pieces()

        total_padding = left_width_padding_pixels + top_height_padding_pixels + \
                        right_width_padding_pixels + bottom_height_padding_pixels + \
                        corner_padding[0][0] + corner_padding[0][1] + corner_padding[1][0] + corner_padding[1][1]
                        
        return total_padding


    # how we're going to use this & if it's going to be a helper function that helps add padding to the parent image

        # team yellow - parent: 1024 x 1024 
        # - tiles: 64 x 64

        # team red - We don't actually need to save the tiles as long as we have the (width x height)
        # and (starting row x starting column)

        #=======Intention for Fri 3/31/23=======
        # using the amount of padding we need (now global variables) to calculate
        # the number of pixels we need to add for padding
        # also add in the width and height padding methods a statement to redefine
        # the value of the padding variables