"""VB2Py - VB to Python + vb2py.PythonCard conversion

This application converts VB projects to Python and vb2py.PythonCard projects.
The form layouts are converted and you can optionally convert the VB
to Python, including translation of the VB events.

The VB conversion is very preliminary!

So is the layout...

"""
import vb2py.projectconverter as conv

def main():
    """Main application"""
    print("start project converter")
    conv.vb2py()
    
if __name__ == "__main__" :
    main()
    
    

