^  *-*      
# Steps from reading file to outputting and saving tiles in a directory
- [ ] File source (location)
    - local directory
    - server (define db)
- check what kind of file it is jpeg, fits and make sure the images are only those two 
- check if the file path exists depending on what machine egnostic their on
- Make sure the python package we install can run on multiple operating systems
- Make test to check for file corruption
- [ ] Define File Class
  - [ ] Source
  - [ ] File/image type
  - [ ] isValid bool to check for errors
  - [ ] Member Functions
	- [ ] Getter functions
      - Get file name
      - Get image type
      - Get isValid
      - Get numpy array
    - [ ] Setter functions
      - Set file name
      - Set image type
      - Set isValid (not publicly exposed)
      - Set numpy array
      - handle both png or fits, converting into numbpy <== revisit
    - [ ] __string__ (observer function)
      - Print fucntion to check to see if the variables were assigned 

- [ ] Define Dataloader

      
	  
  - Does TensorFlow work for PNG and FITS? => Both images are converted to 'tensors' (vector array STL container: https://www.tensorflow.org/guide/tensor)

- [] Open a file
  - Check if file exists and in specified directory
- [] Define how much the file is being read


    -





- [ ] Save tiles into an output directory
  - Check if directory exists...