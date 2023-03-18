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




