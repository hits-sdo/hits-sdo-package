import unittest
# import io

class Test_File_Methods(unittest.TestCase): 
    def test_isJpg(self):
        file =  'blahg.jpg'
        self.assertRegex(file, "\.*jpg|\.*jpeg")

    def test_openFile(self):
        file = 'dummy.txt'
        self.assertRaises(err, open(file, 'r'))
        

    
    

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)		
    

if __name__ == "__main__":
    unittest.main()

