from augmentation import Augmentations
import json
import random
from typing import Any

class AugmentationList():
    '''
    Class for generating random AugmentationList dictionaries
    '''
    
    def __init__(self, instrument: str):
        '''
        Initialize an object of the AugmentationList class
        Parameters:
            instrument (str):
                type of instrument used, either euv or magnetograms        
        Returns:
            None
        '''
        self.augmentations = Augmentations()
        self.keys = self.augmentations.method_names
        
        if instrument == 'euv':
            self.keys.remove('p_flip')
        if instrument == 'mag':
            self.keys.remove('brighten')

        self.zoom_range =             (0.8, 1.2)
        self.brighten_range =         (0.5, 1.5)      
        self.rotate_range =           (-180, 180)     
        self.blur_range =             ((1,1),(2,2))
        self.translate_range =        (-10,10)
            
        
    def randomize(self):
        '''
        Randomize a dictionary based on the number, order, and amount of augmentations
        Parameters:
            None
        Returns:
            dict(str, Any):
                randomized dictionary
        '''
        num = random.randint(1,len(self.keys))
        augs = random.sample(self.keys, num)
        dic = {}
        for key in augs:
            if(key == 'brighten'):
                dic[key] = random.uniform(self.brighten_range[0], self.brighten_range[1])
            if(key == 'zoom'):
                dic[key] = random.uniform(self.zoom_range[0], self.zoom_range[1])
            if(key == 'rotate'):
                dic[key] = random.uniform(self.rotate_range[0], self.rotate_range[1])
            if(key == 'blur'):
                dic[key] = self.blur_range[bool(random.getrandbits(1))]
            if(key == 'translate'):
                a = random.uniform(self.translate_range[0], self.translate_range[1])
                b = random.uniform(self.translate_range[0], self.translate_range[1])
                dic[key] = (int(a),int(b))
            if(key == 'h_flip'):
                dic[key] = True
            if(key == 'p_flip'):
                dic[key] = True
            if(key == 'v_flip'):
                dic[key] = True
        return dic
        
        
        

if __name__=='__main__':
    A = AugmentationList(instrument="mag")
    print(A.randomize())