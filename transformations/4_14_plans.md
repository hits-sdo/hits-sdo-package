  # ====4/12/23 Discussion======
  - Removed the tile_pixel_width and height data attributes from the 
	test_parent_transform_from_tile.py file and instead implement getter functions
	in our class implementation
  - Set tile dimensions as input parameters because parent_transform_from_tile.py
    does not need anything beyond being able to call the functions that calculate the dimensions
    - Now that the information is being passed in, we have to change how test functions are called
    - tile dimensions are passed to parent_transform_from_tile, and then it gets passed from there

# =====TODO for 4/14/23=====
1. create a simple tile class
2. test_parent_transform_from_tile.py
- global variable option for tile_pixel_width & tile_pixel_height has attempted
- alternative option: revert back to data attributes (ex: self.parent_transform_tile_pixel_height)
    - create a tile object in setUp
        - call getter functions for width and height
    - replace all instances of tile pixel width and height in getter functions