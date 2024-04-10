import time
now = time.localtime(time.time())
dateStr = time.strftime("%A, %B %d, %Y,  %I:%M %p", now)
comp.fldDocument.replaceSelection(dateStr)
