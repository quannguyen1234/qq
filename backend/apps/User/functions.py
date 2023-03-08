import random
def generate_id(length:int):
    s=''
    for i in range(length):
        s+=str(random.randint(0,9))
    return s