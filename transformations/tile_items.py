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
        # Calc number of rows and cols of tiles

        # parent_height = ParentTransformationsFromTile.parent_img_height_after_padding
        # parent_width = ParentTransformationsFromTile.parent_img_width_after_padding


        parent_height = 4096
        parent_width = 4096

        num_rows_parent = parent_height // self.tile_height
        num_cols_parent = parent_width // self.tile_width

        img_path = "./user_sample_data/latest_4096_0193.jpg"
        parent_image = Image.open(img_path)


        for row in range(num_rows_parent):
            for col in range(num_cols_parent):
                start_x = col * self.tile_width
                start_y = row * self.tile_height
                width = self.tile_width + start_x
                height = self.tile_height + start_y
                
                # print(start_x)
                # print(start_y)
                # print(width)
                # print(height)


                # crop duplicate
                temp_image = parent_image.crop((start_x, start_y, width, height))

                # save as new tile to a folder called tiles in /user_sample_data/
                temp_image.save(f"stupid/tile_{row}_{col}.jpg", "JPEG")
                

        
        # temp1 = parent_image.crop((0, 0, 1024, 1024))
        # temp2 = parent_image.crop((1024, 1024, 2048, 2048))

        # temp1.save("tile1.jpg")
        # temp2.save("tile2.jpg")
        


        # #return list
        # pass

    def reconstruct_parent_img(self):
        pass

    def export_tiles_local(self, tile_set: tuple, path_to_save_to):
        """Export entire tile set to a selected directory"""

        #Image.save(fp, format=None)

        pass


    


if __name__ == "__main__":
    tc = TilerClass(None ,64 ,64)
    tc.cut_up_tiles()


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
