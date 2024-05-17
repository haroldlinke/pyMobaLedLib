
from distutils.core import setup
import py2exe

setup( name = "textRouter",
       console = ["textRouter.py"],
       data_files = [ ("docs", 
                      ["docs/textRouter_help.html", "docs/readme.html"]),
                      (".",
                      ["strings.txt", "readme.txt", "textRouter.rsrc.py", 
                       "tr.ico"]) 
                    ]
       )

