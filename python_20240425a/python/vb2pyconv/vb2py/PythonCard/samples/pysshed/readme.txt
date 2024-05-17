PySSHed Version 0.3.1 README file

PySSHed is a simple SSH session manager for use on Linux and Windows platforms.
It allows you to store and manage your most frequently used sessions without
editing (and potentially invalidating) the default SSH config file on your PC.

PySSHed is intended primarily for use on a Linux machine, since most Windows
based SSH clients already have some sort of session manager built in. Just
to show how good Python and PythonCard are for cross platform development,
though, it will also interoperate with the free Windows SSH client, Putty.
This version of PySSHed was written in conjunction with a fresh install of
Putty-0.53, so if you have any success (or, indeed, failures) using it with
other versions of Putty under Windows, I'd be happy to hear about it.

The first time you run PySSHed, you'll be asked to specify some default
settings - any subsequent sessions you create will use the defaults as a
starting point, but you can change anything that's inappropriate on a
per-session basis.

Please refer to the changelog.txt file for a detailed revision history.
