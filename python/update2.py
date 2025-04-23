
import os

# for testing update

filedir = os.path.dirname(os.path.realpath(__file__))
print("test python update: filedir")
if os.path.exists(os.path.combine(filedir,"../python_update")):
    print("umbennenen python in python_bak")
    os.rename("../python", "../python_bak")
    print("umbennenen python_update in python")
