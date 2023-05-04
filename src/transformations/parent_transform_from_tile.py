"""
Uses dataclasses to simplify attribute assignment..? read python guide

#TODO
    1) Implement calc_padded_parent_center_pixel() //done
    2) Specify order of operations for member functions // done
        - Use this process to sniff out bad code smells
        - Check for unused data attributes and redundant function calls & input parameters
    3) Standardize terminology for file path variables naming conventions & where they should be constructed
        - Need to avoid losing parts of the path so we can export it
        - Need to avoid the path being too specific/rigid and system agnostic
    4) Create a script for main() that tests the class' member functions
        - This is last, not sure if separately or in a single team
    5) 🤑 Profit 🤑
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

    # parent_file_is_valid: bool
    # parent_file_file_type: str
    parent_file_source: str

    file_meta_dict: dict

    row_offsetted_center_pixel: int
    col_offsetted_center_pixel: int



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

        file_name_stem_list = file_name.split(".")
        file_name_stem = file_name_stem_list[0] + "." + file_name_stem_list[1]

        # Get the top, bottom, left, and right padding values as strings
        top_and_bottom = self.calc_padding_height(tile_pixel_height=tile_pixel_height)
        (top, bottom) = top_and_bottom

        left_and_right = self.calc_padding_width(tile_pixel_width=tile_pixel_width)
        (left, right) = left_and_right

        padding_values = f"{top}_{bottom}_{left}_{right}"

        # Reconstruct the file name by concatenating the stem and the extension
        file_name_stem += "_"
        file_name_stem += padding_values
        updated_file_name = file_name_stem + ".jpg"

        return updated_file_name



    def export_padded_parent_meta(self, updated_file_name: str) -> None:
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
        file_name_values = updated_file_name.split("_")

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
            "row_offsetted_center_pixel": self.row_offsetted_center_pixel,
            "col_offsetted_center_pixel": self.col_offsetted_center_pixel
        }

    def calc_padded_parent_center_pixel(self)->None:
        """
        This function calculates the center pixel with the offset
            Assume that center of img is the center of the sun
            The offset center pixel coordinate is then entered into the dictionary
            The pixel will be calculated with floor division
        """
        self.row_offsetted_center_pixel = self.parent_img_width_after_padding//2
        self.col_offsetted_center_pixel = self.parent_img_height_after_padding//2

    def get_padded_parent_center_pixel(self)->tuple:
        """"
        This function returns a tuple of the row and col of the offsetted center pixel of the parent
            image after it's been padded.
        """
        return (self.row_offsetted_center_pixel, self.col_offsetted_center_pixel)

    def export_padded_parent_to_file(self, file_name:str, tile_pixel_width:int, tile_pixel_height:int)->None:
        """
        This function returns a boolean 
        """
        #filepath_output is the full path, contains file_stem/updated_file_name
        #file directory is the folder
        #file path is the directory + updated_file_name
        #updated_file_name is the name of the file
        try:
            parent_image = Image.open(self.parent_file_source)

            # Need to make sure new_size isnt (0,0)
            new_size = (self.parent_img_width_after_padding, self.parent_img_height_after_padding)

            padded_parent_image = Image.new("RGB", new_size)
            box_param = (self.calc_padding_width(tile_pixel_width=tile_pixel_width), self.calc_padding_height(tile_pixel_height=tile_pixel_height))

            Image.Image.paste(parent_image, padded_parent_image, box=box_param[0])
            new_name = self.generate_file_name_from_parent(file_name, tile_pixel_width, tile_pixel_height)

            filepath_output = f"user_sample_data/{new_name}"
            parent_image.save(filepath_output, "JPEG")      # Need to paste onto original image - Jasper

        except FileNotFoundError:
            print("😦 File not found 😦")

def main():
    """
    Driver function to test our class
    """
    trans_img = ParentTransformationsFromTile(
        parent_img_width=254,
        parent_img_height=254,
        parent_img_width_after_padding=1,
        parent_img_height_after_padding=1,
        parent_file_source = "./user_sample_data/20100905_000036_aia.lev1_euv_12s_4k.jpg",
        file_meta_dict = {},
        row_offsetted_center_pixel=0,
        col_offsetted_center_pixel=0
    )

    h = trans_img.calc_padding_height(tile_pixel_height=64)
    w = trans_img.calc_padding_width(tile_pixel_width=64)

    print("😱 Height: ", h, "Width: ", w, '😱')

    corner_piece = trans_img.calc_corner_pieces(tile_pixel_height=64, tile_pixel_width=64)
    print('😤', corner_piece, '😤')

    overall = trans_img.calc_overall_padding(tile_pixel_height=64, tile_pixel_width=64)
    print('🤩', overall, '🤩')

    generate = trans_img.generate_file_name_from_parent(file_name='20100905_000036_aia.lev1_euv_12s_4k.jpg', tile_pixel_width=64, tile_pixel_height=64)
    print('😭', generate, '😭')
    
    trans_img.export_padded_parent_meta(generate)
    print('🥰 Exported padded parent meta img 🥰')
    
    trans_img.calc_padded_parent_center_pixel()
    print('🤯 Calculated padded parent center pixel 🤯')
    
    get_center_pix = trans_img.get_padded_parent_center_pixel()
    print('🤓', get_center_pix, '🤓')

    trans_img.export_padded_parent_to_file(generate, tile_pixel_height=64, tile_pixel_width=64)
    print('🤨 Exported padded parent to file 🤨')



    # 🤨 TODO 4/28/23 🤨
    # call for export_padded_parent_to_file()
        # fix the image.save



if __name__ == '__main__':
    main()