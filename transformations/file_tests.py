import unittest
import input_file_info
import os
from pyprojroot import here
import sys

root = here(".here")   # naked party
sys.path.append(str(root))
JPG_FILE = 'blahg.jpg'      
TXT_FILE = 'dummy.txt'

class Test_File_Methods(unittest.TestCase): 
    """Class to unit test file methods.

    Attributes:
        InputFileItem: user defined type
    """
    def setUp(self) -> None:
        """  This function sets up all the test variables for our Test_File_Methods.    
        Args: None
        Returns: None

        """
        self.input_file = input_file_info.InputFileItem(name=JPG_FILE, image_type="jpg",
        is_valid = True, time_stamp="blah", f_path="./here", is_remote=True)

        self.input_file2 = input_file_info.InputFileItem(name=TXT_FILE, image_type="txt",
        is_valid = True, time_stamp="blah", f_path="./here", is_remote=True)


    def test_isJpg(self):
        
        tempfile = self.input_file.name.lower()
        self.assertRegex(tempfile, "\.*jpg|\.*jpeg")

    def test_fileExists(self):
        with open(self.input_file2.name):
            self.assertIsNotNone(self.input_file2.name)

    def test_fileisNamed(self):
        self.assertIsInstance(self.input_file.name, str)
        
    def test_pathExists(self):
        #self.assertIsInstance(os.path.exists(self.input_file.f_path), str)
         self.assertTrue(os.path.exists(os.path.join(self.input_file.f_path, "transformations")))

    def test_same_image(self):
        #self.assertEqual()
        pass


    def tearDown(self):
        self.dummy = "dummy"
        
        
        
    # https://docs.python.org/3/library/unittest.html
    

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)		
    

if __name__ == "__main__":
    unittest.main()

