# hits-sdo-packager
Packaging AI/ML ready data for HITS/SDO



# List of Augmentations
## EUV (Solar Image Intensity in Extreme UV Wavelength)
- Brightness
- Translation
- Zoom
- Rotation
- Blurring
- Horizontal/Vertical Flipping

## MAG (Spatial Distribution of Solar Magnetic Field)
- Translation
- Zoom
- Rotation
- Blurring
- Horizontal/Vertical Flipping
- Polarity Flipping

# Augmentation Methodology 
 1. Receive file name from user (64 x 64 image)
    - e.g. tile_20230206_000634_1024_0171_0320_0768.p
 2. Check avaliablity of adjacent images for applying the superimage
 3. Apply superimage on the file name to make a 192 x 192 image
    - A superimage is needed to provide context on certain transformation (e.g. Rotation) to fill in the blank void
 4. Apply augmentations on super image
    - Augmentations can be randomly applied from a random distribution or the user can specify the augmentations to apply
 5. Crop the centeral part of the augmented super image to output a 64 x 64 image

<!--
1. First list item
   - First nested list item
     - Second nested list item

- George Washington
* John Adams
+ Thomas Jefferson
-->