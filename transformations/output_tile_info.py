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
        leftover_padding = ((self.parent_img_width % self.tile_pixel_width) + self.tile_pixel_width) % self.tile_pixel_width
        # returns 1
        # we want 2 to be returned
        
        left_padding = leftover_padding / 2
        right_padding = leftover_padding - left_padding
        padding = (left_padding, right_padding)
        return padding

