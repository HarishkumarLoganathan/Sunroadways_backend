

import os

# Get the absolute path to the file



def get_LrNumber(filepath):
    flag = True
    file = open(filepath, 'r')
    data=file.readlines()
    writefile=open(filepath,'w')
    Lr_Number=""
    for x in data:
        if x.startswith("A") and  flag:
            flag=False
            modified =x.replace("A", "U")
            print (modified)
            writefile.write(modified)
            Lr_Number=x.split(',')[1].strip()

        else:
            writefile.write(x)
    return Lr_Number






