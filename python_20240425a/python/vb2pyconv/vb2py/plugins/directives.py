"""Plug-in to implement directives"""

from vb2py import vbparser
import re
from vb2py import parserclasses

try:
    import vb2py.extensions as extensions
except ImportError:
    import extensions

class VBDirectives(extensions.SystemPlugin):
    """Convert directives (eg #If #Else #End If"""

    __enabled = 1

    #directive_blocks = re.compile(
    #    r'(.*?)^#\s*If\s+(.*?)\sThen\s*$(.*?)^#End\s+If\s*$(.*)',
    #    re.DOTALL+re.M
    #)
    VB2PY_directive_ignore = re.compile(
        r'(.*?)VB2PY-Ignore(.*?)VB2PY-IgnoreEnd$(.*)',
        re.DOTALL+re.M
    )
    
    VB2PY_Python_directive = re.compile(
         r'(.*?)^#If Python Then\s*(.*?)^#End If..Python$(.*)',
        re.DOTALL+re.M
    )    
    
    directive_blocks = re.compile(
        r'(.*?)^#\s*If\s+(.*?)\sThen\s*(.*?)^#End\s+If\s*$(.*)',
        re.DOTALL+re.M
    )    
    warner = parserclasses.VBNamespace()

    def preProcessVBText(self, text):
        """Preprocess the text"""
        # handle VB2PY-Ignore text
        match = self.VB2PY_directive_ignore.match(text)
        
        while match:
            
            message = "'" + self.warner.getWarning('CheckDirective', 'VB2PY directive Ignore Text\n')                    
            text = match.group(1) + message + match.group(3).lstrip()
            match = self.VB2PY_directive_ignore.match(text)
            
        match = self.VB2PY_Python_directive.match(text)

        while match:
            
            message = "'" + self.warner.getWarning('CheckDirective', 'VB2PY Python directive\n')
            text1=match.group(1)
            text2=match.group(2)
            text3=match.group(3)
            parts = re.split('#Else..Python', match.group(2))
            text = match.group(1) + message + parts[0].lstrip() + match.group(3).lstrip()
            match = self.VB2PY_directive_ignore.match(text)        

        match = self.directive_blocks.match(text)

        #path = int(vbparser.Config['Directives', 'Path'])
        path_str = vbparser.Config['Directives', 'Path']
        if path_str.isnumeric():
            path=int(path_str)
            path_list=[]
            use_path_list=False
        else:
            path_list = path_str.split(",")
            use_path_list = True
        
        while match:
            directive = match.group(2)
            parts = re.split('#Else.*', match.group(3))
            if use_path_list:
                if directive in path_list:
                    path=1
                    self.log.info('Matched directive: %s' % match.group(2))
                    message = "'" + self.warner.getWarning('CheckDirective', 'VB directive took path %s on %s\n' % (
                        (path, match.group(2))))                    
                    text = match.group(1) + message + parts[path - 1].lstrip() + match.group(4).lstrip()
                else:
                    path=2
                    self.log.info('Not Matched directive: %s' % match.group(2))
                    message = "'" + self.warner.getWarning('CheckDirective', 'VB directive took path %s on %s\n' % (
                        (path, match.group(2))))                    
                    if len(parts)>1:
                        text = match.group(1) + message + parts[path - 1].lstrip() + match.group(4).lstrip()
                    else:
                        text = match.group(1) + message  + match.group(4).lstrip()
            match = self.directive_blocks.match(text)

        return text