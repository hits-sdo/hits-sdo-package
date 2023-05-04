"""TileItem utilizes NamedTuple"""
import os
import json
import pyprojroot
from dataclasses import dataclass
from typing import NamedTuple 
from PIL import Image
from parent_transform_from_tile import ParentTransformationsFromTile 

base_path = pyprojroot.find_root(pyprojroot.has_dir(".git"))

# {parent_dim: (w,h), parent_padded: (w,h), tile_width....}
class TileItem(NamedTuple):
    tile_width:int
    tile_height:int
    origin_row: int
    origin_col: int
    tile_fname: str

#populate with functions in TilerClass

tempDict = {
    "instrument": "AIA",
    "date": "APRIL 4, 2021",
    "time": "12:00:00",
    "wavelength": "193.4823420",
    "AIA_or_HMI": "AIA",
    "padding": "(2,34,5)",
    "number_child_tiles": "100",
    "tile_list": (),
    "center": (0,0),
    "radius": 5

}
@dataclass
class TilerClass:
    """
    This class divides the parent image into tiles which get
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
    tile_meta_dict_path: str
    tile_item_list: list
    radius: int
    center: tuple
    output_dir: str
    parent_file_name: str

    # If the tile_width and tile_height are bigger than the radius, throw an exception
    # def __post_init__(self):
    #     if self.tile_width > self.radius or self.tile_height > self.radius:
    #         raise ValueError("The tile width and height cannot be greater than the radius")


    def cut_set_tiles(self):
        """This function takes the parent image from parent_transform_from_tile
        and divides it up using the tile width and height from TileItem"""

        num_rows_parent = self.parent_height // self.tile_height
        num_cols_parent = self.parent_width // self.tile_width

        parent_image = Image.open(f"{base_path}/{self.parent_path_input}")
        #transformations/tempTiles
        # create a folder called tiles
        os.makedirs(self.tile_path_output, exist_ok=True)

        for row in range(num_rows_parent):
            for col in range(num_cols_parent):
                start_x = col * self.tile_width
                start_y = row * self.tile_height
                width = self.tile_width + start_x
                height = self.tile_height + start_y

                # Crop duplicate
                temp_image = parent_image.crop((start_x, start_y, width, height))

                # Save as new tile to a folder called tiles in /user_sample_data/
                temp_image.save(f"{self.tile_path_output}/tile_{start_y}_{start_x}.jpg", "JPEG")
           
                # Create a TileItem
                tile_item = TileItem(self.tile_width, self.tile_height, start_y, start_x, \
                    tile_fname=f"tile_{start_y}_{start_x}.jpg")
                self.tile_item_list.append(tile_item)


    def cut_subset_tiles(self):
        """
        Create a user defined set of tiles that are less than the total in the parent image
        """
        parent_image = Image.open(f"{base_path}/{self.parent_path_input}")
        # Transformations/tempTiles
        # Create a folder called tiles
        os.makedirs(self.tile_path_output, exist_ok=True)

        rad_bound_x = 0
        itr_x = 0
        rad_bound_y = 0
        itr_y = 0

        while rad_bound_x < self.radius and rad_bound_x < self.parent_width:
            print('rad_bound_x: ', rad_bound_x)
            rad_bound_x += self.tile_width
            itr_x += 1
        print("Parent Width: ", self.parent_width)

        while rad_bound_y < self.radius and rad_bound_y < self.parent_height:
            print('rad_bound_y: ', rad_bound_y)
            rad_bound_y += self.tile_height
            itr_y += 1
        print("Parent Height: ", self.parent_height)

        #make sure it works for different size rects. ^^^^

        x_1 = self.center[0] - itr_x * self.tile_width
        y_1 = self.center[1] - itr_y * self.tile_height

        #print('x & y: ', x_1, y_1)

        for row in range(x_1, x_1 + 2 * itr_x * self.tile_width, self.tile_width):
            for col in range(y_1, y_1 + 2 * itr_y * self.tile_height, self.tile_height):
                
                #print('row & col: ', row, col)
                start_x = col
                start_y = row
                width = self.tile_width + start_x
                height = self.tile_height + start_y

                # Crop duplicate
                temp_image = parent_image.crop((start_x, start_y, width, height))


                # Save as new tile to a folder called tiles in /user_sample_data/
                tile_f_name = f"{self.tile_path_output}/{self.parent_file_name}\
                    _tile_{start_y}_{start_x}.jpg"
                temp_image.save(tile_f_name, "JPEG")
                # Create a TileItem
                tile_item = TileItem(self.tile_width, self.tile_height, start_y, start_x, \
                    tile_fname=f"tile_{start_y}_{start_x}.jpg")
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
        self.tile_meta_dict["center"] = (None) #assuming this is completed in other class
        self.tile_meta_dict["radius"] = self.radius #assuming this is completed in other class
        return self.tile_meta_dict
    
    def convert_export_dict_to_json(self):
        """Convert metadata to json"""
        dicti = self.tile_meta_dict
        with open(f"{self.tile_meta_dict_path}/{self.parent_file_name}_metadata.json", "w") as outfile:
            json.dump(dicti, outfile)
        
        return

    def generate_tile_fpath_write(self):
        """Generate file path to write tile to"""
        #data/raw/latest_4096_0193.jpg
        #   V
        #mkdir / replace raw with pre-processed / remove .jpg
        #   V
        #data/pre-processed/latest_4096_0193/
        #
        # pretend inside folder latest_4096_0193/
        #       1) padded image (altered from parent)
        #       2) folder of tiles
        #      2a)      tiles
        #       3) folder of metadata
        #      3a)      json
        self.output_dir = f"{base_path}/{self.parent_path_input}"
        self.output_dir = self.output_dir.replace("raw", "pre-processed")
        self.output_dir = self.output_dir.replace(".jpg", "")

        self.tile_path_output = self.output_dir + "/tiles"

        self.tile_meta_dict_path = self.output_dir + "/tile_meta_data"

        self.parent_file_name = self.parent_path_input.find("raw/")
        self.parent_file_name = self.parent_path_input[self.parent_file_name + 4:]
        self.parent_file_name = self.parent_file_name.replace(".jpg", "")


        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.tile_path_output, exist_ok=True)
        os.makedirs(self.tile_meta_dict_path, exist_ok=True)

        pass

    def reconstruct_parent_img(self):
        """Reconstruct parent image from tiles"""
        
        pass


    


if __name__ == "__main__":
    #parent_height = ParentTransformationsFromTile.parent_img_height_after_padding
    #parent_width = ParentTransformationsFromTile.parent_img_width_after_padding

    #these are example values set the init
    # parent_height = 4096
    # parent_width = 4096
    # dicti = generate_tile_metadata()
    cx = 4096//2
    cy = 4096//2
    tc = TilerClass(None, 512, 512, "", 4096, 4096, "data/raw/latest_4096_0193.jpg",
        tempDict, "", [], 1200, (cx,cy), "", "")

    tc.generate_tile_fpath_write()
    tc.cut_subset_tiles()
    # tc.cut_set_tiles()
    tc.tile_meta_dict = tc.generate_tile_metadata()
    tc.convert_export_dict_to_json()

    # parent_image: bytearray
    # tile_width: int
    # tile_height: int
    # tile_path_output: str
    # parent_height : int
    # parent_width : int
    # parent_path_input : str
    # tile_meta_dict: dict
    # tile_meta_dict_path: str
    # tile_item_list: list[TileItem]
    # radius: int
    # center: tuple
    # output_dir: str

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
