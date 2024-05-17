This is a very simple Jabber client. I combined some of the capabilities of the command-line jabberpy example client and the PythonCard chat sample. The current version of jabberChat can only send and receive messages. It doesn't implement the entire Jabber protocol, but it does use Queue so that there isn't a conflict between the jabberpy callback handlers and the GUI event loop. I'm checking this code in with hopes that someone else will make the app more complete.

You'll need the jabberpy package.

http://sourceforge.net/projects/jabberpy

In particular, you'll want the latest versions of the jabber.py and xmlstream.py files from cvs

http://cvs.sourceforge.net/cgi-bin/viewcvs.cgi/jabberpy/jabberpy/

Those files should be placed somewhere on your PYTHONPATH.

If you don't already have one, you should get a more full-featured Jabber client from

http://www.jabbercentral.org/clients/

so that you can setup your account, subscriptions, and test sending and receiving messages. You should be able to use any Jabber server account, not just jabber.org.

For a list of public servers and the gateways (AOL, MSN, Yahoo, ICQ) they support, see:

http://www.jabber.org/user/publicservers.php

Further Jabber information can be found at:

http://www.jabber.org/


You can set the font used by the chat windows and also whether to play a sound for an incoming message by changing the jabberChat.ini file with something like this:

[ChatWindow]
font = {'faceName': 'Arial', 'family': 'sansSerif', 'size': 10}

[Options]
playsound = 1

The sound played is called incoming.wav and you can use another sound file as long as you rename it to incoming.wav.

The idle timeout is also under the [Options] config heading

[Options]
idletime = 5

The default timeout is for 5 minutes, but it can be turned off by setting idletime = 0. There will eventually be menu items and an options dialog for controlling the various .ini file options.

I added some basic support for nicknames or full names, whatever you want to use. I eventually would like to support vCards or some other standard format for the contacts. For now, you can create a names.txt file that contains lines of the format:

jid,Name

such as:

altis@jabber.org,Kevin Altis

The name will be used in the roster list and chat windows.
