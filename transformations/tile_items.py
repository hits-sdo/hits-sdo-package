"""TileItem utilizes NamedTuple"""
from PIL import Image
import os
from dataclasses import dataclass
#from typing import Typing
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
    tile_path_output: str
    parent_height : int
    parent_width : int
    parent_path_input : str
    tile_meta_dict: dict
    tile_item_list: list[TileItem]

    #tile_list: list[TileItem]

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

    def cut_up_tiles(self):
        """This function takes the parent image from parent_transform_from_tile
        and divides it up using the tile width and height from TileItem"""

        num_rows_parent = self.parent_height // self.tile_height
        num_cols_parent = self.parent_width // self.tile_width

        parent_image = Image.open(self.parent_path_input)
        #transformations/tempTiles
        # create a folder called tiles
        os.makedirs(self.tile_path_output, exist_ok=True)

        for row in range(num_rows_parent):
            for col in range(num_cols_parent):
                start_x = col * self.tile_width
                start_y = row * self.tile_height
                width = self.tile_width + start_x
                height = self.tile_height + start_y

                # crop duplicate
                temp_image = parent_image.crop((start_x, start_y, width, height))


                # save as new tile to a folder called tiles in /user_sample_data/
                temp_image.save(f"{self.tile_path_output}/tile_{start_y}_{start_x}.jpg", "JPEG")
                
                # create a TileItem
                tile_item = TileItem(self.tile_width, self.tile_height, start_y, start_x)
                self.tile_item_list.append(tile_item)


        # return list
        # pass
        # {
        #     INSTRUMENT: jacob will do
        #     DATE : APRIL 4, 2021
        #     TIME : 12:00:00
        #     WAVELENGTH : 193.4823420
        #     AIA_or_HMI : AIA
        #     PADDING : (2,34,5)
        #     NUMBER_CHILD_TILES : 100
        #     TILES : TILELIST  (OUR LIST OF NAMED TUPLES)
        #     CENTER : (X,Y)
        #     ~RADIUS : 5
        # }
    def generate_tile_metadata(self) -> dict:
        """Generate metadata for tiles"""
        self.tile_meta_dict["number_child_tiles"] = len(self.tile_item_list)
        self.tile_meta_dict["tile_list"] = self.tile_item_list
        #self.tile_meta_dict["center"] = parent_transform_from_tile.center #assuming this is completed in other class
        #self.tile_meta_dict["radius"] = parent_transform_from_tile.radius #assuming this is completed in other class
        pass
    
    def convert_dict_to_json(self):
        """Convert metadata to json"""
        dict = self.tile_meta_dict

        pass

    def generate_tile_fpath_write(self):
        """Generate file path to write tile to"""
        pass

    def reconstruct_parent_img(self):
        pass

    def export_tiles_local(self, tile_set: tuple, path_to_save_to):
        """Export entire tile set to a selected directory"""

        #Image.save(fp, format=None)

        pass


    


if __name__ == "__main__":
    # parent_height = ParentTransformationsFromTile.parent_img_height_after_padding
    # parent_width = ParentTransformationsFromTile.parent_img_width_after_padding

    #these are example values set the init
    # parent_height = 4096
    # parent_width = 4096
    tc = TilerClass(None ,64 ,64, 4096, 4096)
    tc.cut_up_tiles()


# TODO: RADIUS FUNCTION
# convert to json
# Subtract radius from center x, center y. Do image.crop with those new values
# generate file path to write tile to
# export tiles to local
# reconstruct parent image


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
