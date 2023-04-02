from enum import Enum
 
class ImageEnum(Enum):

    DoctorNotarizedImage = 1    
    Avatar =2

    @classmethod
    def __tupple__(cls):
        arr=[]
        for i in cls.__iter__():
            arr.append((i.value,i.name))
        return tuple(arr)
    

