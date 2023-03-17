from augmentation import Augmentations
import json
import random

class AugmentationList():
    '''
    user sends json obj to server, reads through json obj in AugmentationList class. 
    AugmentationList class asks Augmentation class 

    Vary the augmentations available depending on the instrument
    euv: no p flip
    mag: no brighten
    '''
    def __init__(self, instrument):
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
        print(self.keys) #print all the keys
        #random.shuffle(self.keys)
        
        num = random.randint(1,len(self.keys))
        print(num)
        augs = random.sample(self.keys, num)

        dic = {}
        
        print(augs)
        for key in augs:
            if(key == 'brighten'):
                #random.uniform(low=0.0, high=1.0, size=None)
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

        print(dic)
            # get a random bool:
            # bool(random.getrandbits(1))
            
        
        return dic
        
    # def getRandomParam(self, key):
    #     pass
        
        

if __name__=='__main__':
    A = AugmentationList(instrument="mag")
    # dic = A.randomize()
    # print(dic.keys())