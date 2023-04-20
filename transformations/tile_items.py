"""TileItem utilizes NamedTuple"""
from PIL import Image
from dataclasses import dataclass
from typing import Typing
from typing import NamedTuple
from parent_transform_from_tile import ParentTransformationsFromTile 

# {parent_dim: (w,h), parent_padded: (w,h), tile_width....}
class TileItem(NamedTuple):
    tile_width:int
    tile_height:int
    origin_row: int
    origin_col: int

#populate with functions in TilerClass
@dataclass
class TilerClass:
    """This class divides the parent image into tiles which get
    packaged into TileItems
    """
    parent_image: bytearray
    tile_width: int
    tile_height: int
    tile_list: list[TileItem]

    #tile_image: 2D array 
    

    #tile_group: tuple #user can specify which groupings of tiles they want from parent image

    #in this case, tile1 = TileItem(width, )
    
    def create_subset_tiles(self, user_coordinate,):
        """Create a user defined set of tiles 
        that are less than the total  in the parent
        image
        """
        pass
        # ????
        # parent_image = Image.open(image_path)

    def cut_up_tiles(self):
        """This function takes the parent image from parent_transform_from_tile
        and divides it up using the tile width and height from TileItem"""
        # Calc number of rows and cols of tiles

        parent_height = ParentTransformationsFromTile.parent_img_height_after_padding
        parent_width = ParentTransformationsFromTile.parent_img_width_after_padding

        num_rows_parent = parent_height // self.tile_height
        num_cols_parent = parent_width // self.tile_width

        # Loop goes here
            # Extract tiles goes here

        #return list
        pass

    def reconstruct_parent_img(self):
        pass

    def export_tiles_local(self, tile_set: tuple, path_to_save_to):
        """Export entire tile set to a selected directory"""

        #Image.save(fp, format=None)

        pass

# creating a class
# class Website(NamedTuple):
#     name: str
#     url: str
#     rating: int
  
# # creating a NamedTuple
# website1 = Website('GeeksforGeeks',
#                    'geeksforgeeks.org',
#                    5)
  
# # displaying the NamedTuple
# print(website1)
