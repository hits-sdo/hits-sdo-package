"""
Uses dataclasses to simplify attribute assignment..? read python guide

#TODO
    1) Implement calc_padded_parent_center_pixel()
    2) Specify order of operations for member functions
        - Use this process to sniff out bad code smells
        - Check for unused data attributes and redundant function calls & input parameters
    3) Standardize terminology for file path variables naming conventions & where they should be constructed
        - Need to avoid losing parts of the path so we can export it
        - Need to avoid the path being too specific/rigid and system agnostic
    4) Create a script for main() that tests the class' member functions
        - This is last, not sure if separately or in a single team
    
    * Paths are hard -> utils function because every team will struggle with this when pivoting to ML
"""
from PIL import Image
from dataclasses import dataclass
from datetime import datetime

@dataclass

class ParentTransformationsFromTile:
    """This will keep track of an output tile file"""

    parent_img_width: int
    parent_img_height: int

    parent_img_width_after_padding: int
    parent_img_height_after_padding: int

    parent_file_is_valid: bool
    parent_file_file_type: str
    parent_file_source: str

    file_meta_dict: dict



    def calc_padding_width(self, tile_pixel_width:int) -> tuple:
        """If the tile doesn't divide evenly into the parent width then calculates excess padding"""

        leftover_padding = self.parent_img_width % tile_pixel_width
        if leftover_padding == 0:
            return (0, 0)
        leftover_padding = tile_pixel_width - leftover_padding

        left_padding = leftover_padding // 2
        right_padding = leftover_padding - left_padding
        padding = (left_padding, right_padding)
        return padding

    def calc_padding_height(self, tile_pixel_height:int) -> tuple:
        """If the tile doesn't divide evenly into the parent height,
        then calculates excess padding"""

        leftover_padding = self.parent_img_height % tile_pixel_height
        if leftover_padding == 0:
            return (0, 0)

        leftover_padding = tile_pixel_height - leftover_padding

        top_padding = leftover_padding // 2
        bottom_padding = leftover_padding - top_padding
        padding = (top_padding, bottom_padding)
        return padding

    def calc_corner_pieces(self, tile_pixel_width:int, tile_pixel_height:int) -> tuple:
        """Using the padding from width and height to
            calculate the padding for the corners of the image.
            Returns a tuple of 2 tuples
        """
        pad_width = self.calc_padding_width(tile_pixel_width)
        pad_height = self.calc_padding_height(tile_pixel_height)

        top_left = pad_width[0] * pad_height[0]
        top_right = pad_width[1] * pad_height[0]
        bot_left = pad_width[0] * pad_height[1]
        bot_right = pad_width[1] * pad_height[1]
        corner_padding = ((top_left,top_right), (bot_left,bot_right))
        return corner_padding


    def calc_overall_padding(self, tile_pixel_width:int, tile_pixel_height:int) -> int:
        """using the amount of padding we need (now global variables) to calculate the number of
        pixels we need to add for padding also add in the width and height padding methods a
        statement to redefine the value of the padding variables"""
        calc_width = self.calc_padding_width(tile_pixel_width)
        calc_height = self.calc_padding_height(tile_pixel_height)
        left_width_padding_pixels = calc_width[0] * self.parent_img_height
        right_width_padding_pixels = calc_width[1] * self.parent_img_height
        top_height_padding_pixels = calc_height[0] * self.parent_img_width
        bottom_height_padding_pixels = calc_height[1] * self.parent_img_width

        corner_padding = self.calc_corner_pieces(tile_pixel_width, tile_pixel_height)

        total_padding = left_width_padding_pixels + top_height_padding_pixels + \
                        right_width_padding_pixels + bottom_height_padding_pixels + \
                        corner_padding[0][0] + corner_padding[0][1] + corner_padding[1][0] + \
                              corner_padding[1][1]

        return total_padding
    
    def generate_file_name_from_parent(self, file_name: str, tile_pixel_width: int, tile_pixel_height: int) -> str:
        """
        This function generates a filename from parent with the padding values
            - this function assumes that a CSV file with the name of every image in the directory exists

                20100905_000036_aia.lev1_euv_12s_4k.jpg
                date_time_instrument.___wavelength_timeseries_resolution?
                Take name as is and split on second '.' extension to make the file name a string w/o the 'jpg'
                Append '_' + padding, which contains the values for the 'top_bottom_left_right' padding and then reattach '.jpg'
        """

        file_name_stem = file_name.split(".", 1)[0]

        # Get the top, bottom, left, and right padding values as strings
        top_and_bottom = str(self.calc_padding_height(tile_pixel_height=tile_pixel_height))
        top = top_and_bottom[0]
        bottom = top_and_bottom[1]

        left_and_right = str(self.calc_padding_width(tile_pixel_width=tile_pixel_width))
        left = left_and_right[0]
        right = left_and_right[1]

        padding_values = f"{top}_{bottom}_{left}_{right}"

        # Reconstruct the file name by concatenating the stem and the extension
        file_name_stem += "_"
        file_name_stem += padding_values
        updated_file_name = file_name_stem + ".jpg"

        return updated_file_name



    def export_padded_parent_meta(self, file_name: str) -> None:
        """
        This function creates an empty dictionary and creates key values with the 
        information in the filename
        The function will then export the padded parent meta to the local directory
            - Convert date in string format to a datetime object
                datetime.strptime(date_string, format)
                - strptime returns a ValueError if it cannot be parsed
        
        Format of file name:
        Images captured by AIA: 20100905_000036_aia.lev1_euv_12s_4k_top_bottom_left_right.jpg
        Images captured by HMI: 20100905_000036_hmi.M_720s_4k_top_bottom_left_right.jpg
        
        Date format: YYYYMMDD_HHmmSS

        """

        #[20100905, 000036, aia.lev1, euv, 12s, 4k, top, bottom, left, right.jpg]
        #[20100905, 000036, hmi.M, 720s, 4k, top, bottom, left, right.jpg]
        file_name_values = file_name.split("_")

        # If the instrument is HMI, it lacks a wavelength value so we insert
        # an empty string to take its place
        if len(file_name_values) == 9 :
            file_name_values.insert(3, "")

        # Splitting the instrument and data series name
        file_name_values_index_two = file_name_values[2].split('.')
        # Splitting the right padding value and file extension name
        file_name_values_index_nine = file_name_values[9].split('.')

        # Datetime Object
        date_string = file_name_values[0] + file_name_values[1]

        # Creating the dictionary
        self.file_meta_dict = {
            "date_time": datetime.strptime(date_string, "%Y%m%d%H%M%S"),
            "instrument": file_name_values_index_two[0],
            "data_series_name": file_name_values_index_two[1],
            "wavelength": file_name_values[3],
            "timeseries": file_name_values[4],
            "resolution": file_name_values[5],
            "top_padding_value": int(file_name_values[6]),
            "bottom_padding_value": int(file_name_values[7]),
            "left_padding_value": int(file_name_values[8]),
            "right_padding_value": int(file_name_values_index_nine[0]),
            "file_format": file_name_values_index_nine[1],
            # "row_offsetted_center_pixel": int,      # These should be data members, but they aren't yet - 4/24
            # "col_offsetted_center_pixel": int,
        }

    def calc_padded_parent_center_pixel(self):
        """
        This function calculates the center pixel with the offset
            Assume that center of img is the center of the sun
            The offset center pixel coordinate is then entered into the dictionary
        """
        raise NotImplementedError



    def export_padded_parent_to_file(self, file_name:str, tile_pixel_width:int, tile_pixel_height:int)->bool:
        #filepath_output is the full path, contains file_stem/updated_file_name
        #file directory is the folder
        #file path is the directory + updated_file_name
        #updated_file_name is the name of the file
        try:
            parent_image = Image.open(self.parent_file_source)
            new_size = (self.parent_img_width_after_padding, self.parent_img_height_after_padding)
            padded_parent_image = Image.new("RGB", new_size)
            box_param = (self.calc_padding_width(tile_pixel_width=tile_pixel_width), self.calc_padding_height(tile_pixel_height=tile_pixel_height))
            padded_parent_image = Image.paste(parent_image, box=box_param)
            new_name = generate_file_name_from_parent(file_name, tile_pixel_width, tile_pixel_height)
            filepath_output = new_name + "what is stem" 
            padded_parent_image.save(filepath_output, format="JPG")
        except:
            return False

            # FileNotFound exception


        return True

def main():
    """
    Driver function to test our class
    """

if __name__ == '__main__':
    main()