
BASE_IMAGE_URL = 'http://pythoncard.sourceforge.net'

# may need to expand the logic to support
# a conditional smaller image for the main page
# with a link to a larger image
# perhaps just having an extra item in the list will work
#['description', 'imageURL', 'optionalSmallImageURL'],

# tools will probably have their own dir
# but the images might be in the same list
"""
'textEditor':[
        ['A simple text editor', '/images/textEditor01.jpg'],
    ],
"""

images = {
'addresses':[
        ['A direct port of the layout and data from the HyperCard Addresses stack', 
        '/images/addresses_01.png'],
    ],
'chat':[
        ['', '/images/chat_01.png'],
    ],
'codeEditor':[
        ['Editing the minimal.py sample', '/images/codeEditor_01.png'],
        ['File Menu', '/images/codeEditorFileMenu.png'],
        ['Edit Menu', '/images/codeEditorEditMenu.png'],
        ['View Menu', '/images/codeEditorViewMenu.png',],
    ],
'companies':[
        ['', '/images/companies_01.png'],
    ],
'conversions':[
        ['', '/images/conversions_01.jpg'],
    ],
'custdb':[
        ['', '/images/custdb_01.png'],
    ],
'dbBrowser':[
        ['The initial login dialog', '/images/dbBrowser01.jpg'],
        ['A record from a MySQL database', '/images/dbBrowser02.jpg'],
    ],
'dialogs':[
        ['', '/images/dialogs_01.png'],
        ['', '/images/test_dialogs_02.jpg'],
        ['', '/images/test_dialogs_03.jpg'],
    ],
'doodle':[
        ['A simple bitmap drawing program', '/images/doodle01.jpg'],
    ],
'flatfileDatabase':[
        ['', '/images/flatfileDatabase_01.png'],
    ],
'hopalong':[
        ['', '/images/hopalong_02.jpg'],
    ],
'life':[
        ['Main window', '/images/life_01.png'],
        ['Lexicon window', '/images/life_02.png'],
        ['Patterns window', '/images/life_03.png'],
    ],
'minimal':[
        ['Windows', '/images/large/Minimal.gif'],
        ['Linux', '/images/snapminimal_01.png'],
    ],
'pictureViewer':[
        ['', '/images/pictureViewer_01.png'],
    ],
'proof':[
        ['Windows', '/images/large/Proof.gif'],
        ['Linux', '/images/snapproof_01.png'],
    ],
'pysshed':[
        ['Session Manager', '/images/pysshed_01.jpg'],
        ['Session Defaults', '/images/pysshed_02.jpg'],
    ],
'radioclient':[
        ['', '/images/radioclient_01.png'],
    ],
'redemo':[
        ['', '/images/redemo_01.png'],
    ],
'rpn':[
        ['', '/images/rpn_01.png'],
    ],
'samples':[
        ['', '/images/large/SamplesLauncher.gif'],
    ],
'searchexplorer':[
        ['', '/images/large/SearchExplorer.gif'],
    ],
'simpleBrowser':[
        ['', '/images/simpleBrowser_01.png'],
    ],
'slideshow':[
        ['', '/images/slideshow_01.png'],
    ],
'sounds':[
        ['', '/images/large/Sounds.gif'],
    ],
'SourceForgeTracker':[
        ['', '/images/SourceForgeTracker_01.jpg'],
    ],
'spirograph':[
        ['', '/images/spirograph_01.png'],
    ],
'stockprice':[
        ['', '/images/stockprice_01.png'],
    ],
'textIndexer':[
        ["Dan Winkler's original test converted from tkinter", '/images/textIndexer01.jpg'],
    ],
'textRouter':[
        ['', '/images/textRouter01.jpg'],
    ],
'tictactoe':[
        ['Noughts and Crosses', '/images/tictactoe_01.jpg'],
    ],
'turtle':[
        ['4bugs', '/images/turtle_4bugs_01.jpg'],
        ['3turtles', '/images/turtle_3turtles_01.jpg'],
        ['bytedesign', '/images/turtle_bytedesign_01.jpg'],
        ['pentest', '/images/turtle_pentest_01.jpg'],
        ['Manipulating the turtle from the shell', '/images/turtle_shell_01.jpg'],
    ],
'webgrabber':[
        ['', '/images/webgrabber_01.png'],
    ],
'widgets':[
        ['Windows', '/images/widgets_01.png'],
        ['Linux', '/images/snapwidgets_01.png'],
    ],
'worldclock':[
        ['', '/images/large/WorldClock.jpg'],
    ],
}
