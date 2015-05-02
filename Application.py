'''
Patrick Biggs
22nd April 2015
'''

import sys
from Graph import *
from TextGraph import *
from GcodeGraph import *

def cmdSave():
    f=open("save.txt","w")
    TextGroup.show(model,f)
    f.close()


print("Starting Application")

model = Group("model")
clipboard = Group("clipboard")
selected = Group("selected")

model.add(Line(100,100,150,200))
tg=TextGroup(model,sys.stdout)
tg.show()

#cmd_save()

print("Finishing Application")


    



