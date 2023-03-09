import unittest
import input_file_info
# import io
JPG_FILE = 'blahg.jpg'
TXT_FILE = 'dummy.txt'

class Test_File_Methods(unittest.TestCase): 
    def setUp(self) -> None:
        self.input_file = input_file_info.InputFileItem(name=JPG_FILE, imag_type="jpg",
        is_valid = True, time_stamp="blah", f_path="./here", is_remote=True)

        self.input_file2 = input_file_info.InputFileItem(name=TXT_FILE, imag_type="txt",
        is_valid = True, time_stamp="blah", f_path="./here", is_remote=True)

    def test_isJpg(self):
        tempfile = self.input_file.name.toUpper()
        self.assertRegex(tempfile, "\.*jpg|\.*jpeg")

    def test_fileExists(self):
        with open(self.input_file2.name):
            self.assertIsNotNone(self.input_file2.name)

    def test_fileisNamed(self):
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

