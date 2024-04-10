#!/usr/bin/env python
#
# word_wrap.py
#
# this was originally based on some code I found on the net, but I
# couldn't get that to work so I just wrote it afresh.

"""
__version__ = "$Revision: 1.4 $"
__date__ = "$Date: 2002/12/27 17:26:40 $"
"""

def wrap_string(str, max, para = "\n\n"):
    paras = str.split(para)
    outStr = ""
    
    for paragraph in paras:
        paragraph = paragraph.replace("\n", " ")
        words = paragraph.split()
        outLine = ""
        lineCount = wordCount = 0
        
        for i in range(len(words)):
            if (len(outLine) + len(words[i])) > max:
                if lineCount:
                    outStr += "\n"
                outStr += outLine
                outLine = words[i]
                lineCount += 1
                wordCount = 1
            else:
                if wordCount:
                    outLine += " "
                outLine +=  words[i]
                wordCount += 1

        if lineCount:
            outStr += "\n"
        outStr += outLine
        outStr += para
        
    return outStr
