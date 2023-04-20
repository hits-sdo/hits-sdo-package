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

# =====TODO for 4/19/23=====
1. Design choice One tile class will hold all tiles associated with one parent image
2. Test cases for TilerClass member functions
3. (lower priority) If time, GitHub actions yaml written to run all test     cases we've already written upon push/pull request
4. Ask Andres if there is a Earth observation data that we can use to select a ROI

# =====TODO for 4/21/23=====
1. Ask team red and yellow about JSON file
2. Ask Andres if there is a Earth observation data that we can use to select a ROI
3. Continue cut_up_tiles function in tile_items.py
4. Do reconstruct_tile_parent function in tile_items.py
5. Do export_tiles_local function in tile_items.py
6. Write unit tests for tile_items module under test_tile_items.py (ex: visualizing the tiles reconstructed vs original parent)
