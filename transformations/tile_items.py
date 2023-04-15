import PIL
from dataclasses import dataclass
from typing import Typing
from typing import NamedTuple


class TileItem(NamedTuple):
    tile_width:int
    tile_height:int
    origin_row: int
    origin_col: int

class SeparateClass:
    """This class divides the parent image into tiles"""
    parent_image: bytearray
    #tile_image: 2D array 
    

    #tile_group: tuple #user can specify which groupings of tiles they want from parent image

    #in this case, tile1 = TileItem(width, )
    
    def grab_tiles():
        ...


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
