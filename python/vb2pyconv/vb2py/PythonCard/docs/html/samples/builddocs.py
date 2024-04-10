
import os
import imageList
from PythonCard import util

# this is just a copy and paste of the list in samples.rsrc.py
# and should be updated as new samples are added

SAMPLES = ['addresses', 'chat', 'companies', 'conversions', 'custdb', 'dbBrowser', \
             'dialogs', 'doodle', 'flatfileDatabase', 'gadflyDatabase', \
             'hopalong', 'jabberChat', 'life', 'minimal', 'minimalStandalone', 'noresource', \
             'pictureViewer', 'proof', 'pysshed', 'radioclient', 'redemo', 'rpn', \
             'samples', 'saveClipboardBitmap', 'searchexplorer', \
             'simpleBrowser', 'simpleIEBrowser', 'slideshow', 'sounds', 'SourceForgeTracker', \
             'spirograph', 'stockprice', 'textIndexer', 'textRouter', \
             'tictactoe', 'turtle', 'webgrabber', 'webserver', 'widgets', 'worldclock']

# used to auto-generate a batch file that can be 
# run to upload all the newly generated files
UPLOAD_COMMAND = 'c:\cvshome\pscp %s.html kasplat@pythoncard.sourceforge.net:/home/groups/p/py/pythoncard/htdocs/samples/%s.html\n'

# this could be done easier
# with a regular expression
# suggestions welcome
def expandUrls(text):
    newtext = ''
    for s in text.splitlines():
        stripped = s.strip()
        if stripped.startswith('http://'):
            url = '  <a href="%s">%s</a>' % (stripped, stripped)
            newtext += url + "\n"
        else:
            newtext += s + "\n"
    return newtext

def readFile(path):
    fp = open(path)
    data = fp.read()
    fp.close()
    return data

def writeFile(path, data):
    fp = open(path, 'w')
    fp.write(data)
    fp.close()

def main():
    html_template = readFile(os.path.join('templates', 'sample_template.html'))
    contents_template = readFile(os.path.join('templates', 'contents_template.html'))

    samplesDir = os.path.join('..', '..', '..', 'samples')

    batch = ''
    contents = '<b>Samples</b><br>\n'
    
    max = len(SAMPLES) - 1
    for i in range(len(SAMPLES)):
        name = SAMPLES[i]
        contents += '<a href="%s.html">%s</a><br>\n' % (name, name)

    for i in range(len(SAMPLES)):
        name = SAMPLES[i]
        if name == 'samples':
            path = os.path.join(samplesDir, 'readme.txt')
        else:
            path = os.path.join(samplesDir, name, 'readme.txt')

        readme = readFile(path)

        html = html_template
        html = html.replace('[title]', name)
        if i == 0:
            previousSample = SAMPLES[-1]
            nextSample = SAMPLES[i + 1]
        elif i == max:
            previousSample = SAMPLES[i - 1]
            nextSample = SAMPLES[0]
        else:
            previousSample = SAMPLES[i - 1]
            nextSample = SAMPLES[i + 1]

        data = ''
        template = ''
        try:
            images = imageList.images[name]
            for i in range(len(images)):
                figure, url = images[i]
                if figure == '':
                    figure = "Figure %d" % (i + 1)
                else:
                    figure = "Figure %d: %s" % (i + 1, figure)
                if not url.startswith('http:'):
                    url = imageList.BASE_IMAGE_URL + url
                template += '<p><IMG SRC="%s" BORDER=0></p>\n<b>%s</b><br>\n' % (url, figure)
        except:
            pass
        
        html = html.replace('[contents]', contents)
        html = html.replace('[images]', template)
        html = html.replace('[previous_sample]', previousSample)
        html = html.replace('[next_sample]', nextSample)
        # using a slightly longer wrap hopefully
        # avoids problems when the readme.txt has its
        # own line feeds
        readme = expandUrls(util.wordwrap(readme, 86))
        html = html.replace('[readme.txt]', readme)
        
        writeFile(name + '.html', html)

        #contents += '<a href="%s.html">%s</a><br>\n' % (name, name)
        batch += UPLOAD_COMMAND % (name, name)
        i += 1

    contents_template = contents_template.replace('[contents]', contents)
    writeFile('index.html', contents_template)
    batch += UPLOAD_COMMAND % ('index', 'index')

    writeFile('upload.bat', batch)

    
if __name__ == '__main__':
    main()
