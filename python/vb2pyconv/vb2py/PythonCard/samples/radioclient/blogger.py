"""Blogger interface for Python

http://sourceforge.net/projects/pyblogger/

This module allows you to post to a weblog and manipulate its
settings.  It was originally designed to work with Blogger
(http://www.blogger.com/), but other weblog systems have since
implemented this API, and this module can talk to any of them.
Whichever system you use, you'll need an account.
- Blogger: http://www.blogger.com/
- Manila: http://www.manilasites.com/
- LiveJournal: http://www.livejournal.com/

Note that LiveJournal does not support this API directly; you'll
need to use a Blogger-to-LiveJournal gateway, described here:
  http://www.tswoam.co.uk/index.php?n_go=14

Many functions take the following common arguments:
- blogID:
  - If connecting to Blogger, this is your blog's ID number on
    blogger.com; to get this, log in on blogger.com, click on your blog
    to edit it, and look in the query string of the URL.
  - For Manila, this is the base URL of your weblog.
  - For LiveJournal, this is the journal name.  Can be left blank
    and the user's default journal will be used.
- username: your weblog system username.
- password: your weblog system password.

Example:
>>> import blogger
>>> username = "YOUR_BLOGGER_USERNAME"
>>> password = "YOUR_BLOGGER_PASSWORD"
>>> blogs = blogger.listBlogs(username, password)
>>> myFirstBlog = blogs[0]
>>> url = myFirstBlog["url"]
>>> blogID = myFirstBlog["blogid"]
>>> postID = blogger.newPost(blogID, username, password, "First post!", 1)
>>> print "New post is available at %s#%s" % (url, postID)
"""

__author__ = "Mark Pilgrim (f8dy@diveintomark.org)"
__version__ = "$Revision: 1.2 $"
__date__ = "$Date: 2003/01/10 07:37:50 $"
__copyright__ = "Copyright (c) 2001-2 Mark Pilgrim"
__license__ = "Python"

# Requires Pythonware's XML-RPC library
# This comes standard in Python 2.2
# Users of earlier versions must download and install from
# http://www.pythonware.com/products/xmlrpc/
import xmlrpclib

class TemplateType:
    main = "main"
    archiveIndex = "archiveIndex"
    acceptableTypes = (main, archiveIndex)

class constants:
    # XML-RPC server.  We default to Blogger's server, but you
    # can set this to any Blogger-compatible server
    # - Manila: set to your base URL + "/RPC2"
    # - LiveJournal: set to your Blogger-LiveJournal gateway
    # Alternatively, you can pass the server to any of the
    # functions as the last parameter to override this setting.
    xmlrpcServer = "http://plant.blogger.com/api/RPC2"
    
    # The application key is required by Blogger;
    # other weblog systems ignore it
    applicationKey = "1973FAF4B76FC60D35E266310C6F0605456798"
    
    # Transport is only used for testing; should be None for production
    transport = None

def getUserInfo(username, password, serverURL=None):
    """Get information about a user
    
    Returns: dictionary
        {"nickname": "user's nickname",
         "userid": "user ID",
         "url": "user's URL",
         "email": "user's email",
         "lastname": "user's last name",
         "firstname": "user's first name"}
    
    Arguments:
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> info = blogger.getUserInfo("my_blogger_username", "my_secret_password")
    >>> for k, v in info.iteritems():
    ...     print k, v
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    info = server.blogger.getUserInfo(constants.applicationKey,
        username,
        password)
    return info

def listBlogs(username, password, serverURL=None):
    """Get a list of your blogs
    
    Returns: list of dictionaries
        [{"blogid": ID_of_this_blog,
          "blogName": "name_of_this_blog",
          "url": "URL_of_this_blog"}, ...]
    
    Arguments:
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogList = blogger.listBlogs("my_blogger_username", "my_secret_password")
    >>> for blog in blogList:
    ...     print "ID:", blog["blogid"]
    ...     print "Name:, blog["blogName"]
    ...     print "URL:", blog["url"]
    ...     print
    
    Manila notes:
    - Manila does not support this method, because it does not keep a centralized
      database of a user's blogs.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.getUsersBlogs(constants.applicationKey,
        username,
        password)
    return response
getUsersBlogs = listBlogs

def listPosts(blogID, username, password, maxPosts=20, serverURL=None):
    """List recent posts in your blog
    
    Returns: list of dictionaries
        [{"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
          "userid": user who posted this entry,
          "postid": ID of this post,
          "content": text of this post
         }, ...]
        
        Posts are listed in chronological order, oldest to newest, so
        listPosts(...)[-1] is the newest post
    
    Arguments:
    - blogID: your weblog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - maxPosts: maximum number of posts to return
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.listPosts(my_blog_ID, "my_blogger_username", "my_blogger_password", 1)
    # returns the most recent post
    
    Notes:
    - The Blogger server will only return the 20 most recent posts.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.getRecentPosts(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        maxPosts)
    response.reverse()
    for i in range(len(response)):
        v = response[i]["dateCreated"].value
        response[i]["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response
getRecentPosts = listPosts

def getPost(postID, username, password, serverURL=None):
    """Get a single post by ID
    
    Returns: dictionary
        {"dateCreated": date/time of this post in tuple format (see http://python.org/doc/lib/module-time.html)
         "userid": user who posted this entry,
         "postid": ID of this post,
         "content": text of this post}
        
    Arguments:
    - postID: the ID of the post to get
    - username: your weblog username
    - password: your weblog password
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> blogger.getPost(postID, "my_blogger_username", "my_blogger_password")
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.getPost(constants.applicationKey,
        str(postID),
        str(username),
        str(password))
    v = response["dateCreated"].value
    response["dateCreated"] = (int(v[:4]), int(v[4:6]), int(v[6:8]), int(v[9:11]), int(v[12:14]), int(v[15:17]), 0, 0, 0)
    return response

def newPost(blogID, username, password, text, publish=0, serverURL=None):
    """Post a new message to your blog
    
    Returns: string
        post ID: append this to your base blog URL to link to your new post
    
    Arguments:
    - blogID: your blog's ID number (see module docs for details)
    - username: your weblog username
    - password: your weblog password
    - text: the actual text you'd like to post
    - publish (optional): 0 = post but do not publish (default)
                          1 = post and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newPost(my_blog_ID, "my_blogger_username", "my_blogger_password, "First post!", 1)
    >>> print postID
    
    Blogger notes:
    - Posts are limited to 65536 characters by the Blogger server.
    - If you want to publish, you must set up your blog to remember your
      FTP username and password.  You must do this through the web interface
      at blogger.com; there is currently no way to do it through this API.
    
    Manila notes:
    - Manila does not have the concept of "post but don't publish"; all
      posts are published immediately.  So the "publish" flag is used as
      an approval flag for multi-member weblogs.  See
      http://frontier.userland.com/emulatingBloggerInManila
      for details.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    postID = server.blogger.newPost(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        str(text),
        publish and xmlrpclib.True or xmlrpclib.False)
    return postID

def editPost(postID, username, password, text, publish=0, serverURL=None):
    """Edit an existing message in your blog
    
    Returns: 1
    
    Arguments:
    - postID: ID of post to edit
    - username: your weblog username
    - password: your weblog password
    - text: the actual text you'd like to post
    - publish (optional): 0 = post but do not publish (default)
                          1 = post and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newPost(my_blog_ID, "my_blogger_username", "my_blogger_password, "First post!", 1)
    >>> blogger.editPost(postID, "my_blogger_username", "my_blogger_password, "This text overwrites the old text completely.", 1)
    
    Blogger notes:
    - Posts are limited to 65536 characters by the Blogger server.
    - If you want to publish, you must set up your blog to remember your
      FTP username and password.  You must do this through the web interface
      at blogger.com; there is currently no way to do it through this API.
    
    Manila notes:
    - Manila does not have the concept of "post but don't publish"; all
      posts are published immediately.  So the "publish" flag is used as
      an approval flag for multi-member weblogs.  See
      http://frontier.userland.com/emulatingBloggerInManila
      for details.
    
    LiveJournal notes:
    - Post IDs (item IDs) are not guaranteed to be unique across all of a
      user's journals, so the default journal is always used.  There is
      currently no way of editing entries on a secondary journal.  See
      http://www.tswoam.co.uk/index.php?n_go=14
      for details.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.editPost(constants.applicationKey,
        str(postID),
        str(username),
        str(password),
        str(text),
        publish and xmlrpclib.True or xmlrpclib.False)
    return response == xmlrpclib.True

def deletePost(postID, username, password, publish=0, serverURL=None):
    """Delete an existing message in your blog
    
    Returns: 1
    
    Arguments:
    - postID: ID of post to edit
    - username: your weblog username
    - password: your weblog password
    - publish (optional): 0 = delete but do not publish (default)
                          1 = delete and publish
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Example:
    >>> postID = blogger.newPost(my_blog_ID, "my_blogger_username", "my_blogger_password, "First post!", 1)
    >>> blogger.deletePost(postID, "my_blogger_username", "my_blogger_password, 1)
    
    Blogger notes:
    - Posts are limited to 7200 characters by the Blogger server.
    - If you want to publish, you must set up your blog to remember your
      FTP username and password.  You must do this through the web interface
      at blogger.com; there is currently no way to do it through this API.
    
    LiveJournal notes:
    - Post IDs (item IDs) are not guaranteed to be unique across all of a
      user's journals, so the default journal is always used.  There is
      currently no way of deleting entries on a secondary journal.  See
      http://www.tswoam.co.uk/index.php?n_go=14
      for details.
    """
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    response = server.blogger.deletePost(constants.applicationKey,
        str(postID),
        str(username),
        str(password),
        publish and xmlrpclib.True or xmlrpclib.False)
    return response == xmlrpclib.True

def getTemplate(blogID, username, password, templateType="main", serverURL=None):
    """Get HTML template for your blog
    
    Returns: string
        specified HTML template
    
    Arguments:
    - blogID: your blog's ID number
    - username: your blogger.com username
    - password: your blogger.com password
    - templateType: 'main' = get main page template (default)
                    'archiveIndex' = get archive index template
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    """
    if templateType not in TemplateType.acceptableTypes:
        raise ValueError, "invalid template type: %s" % templateType
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    htmlTemplate = server.blogger.getTemplate(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        templateType)
    return htmlTemplate

def setTemplate(blogID, username, password, text, templateType="main", serverURL=None):
    """Set HTML template for your blog
    
    Returns: 1
    
    Arguments:
    - blogID: your blog's ID number
    - username: your blogger.com username
    - password: your blogger.com password
    - text: complete HTML text of template
    - templateType: 'main' = set main page template (default)
                    'archiveIndex' = set archive index template
    - serverURL: URL of remote server (optional, defaults to constants.xmlrpcServer)
    
    Notes:
    - The given username must be marked as an administrator on the blog in order to
      set the template.  This is the default if you created the blog, but
      not the default if somebody else added you to a team blog.  Administrators
      can add other users to their blog and give them administrative access,
      but they need to do it through the web interface at blogger.com.
    """
    if templateType not in TemplateType.acceptableTypes:
        raise ValueError, "invalid template type: %s" % templateType
    server = xmlrpclib.Server(serverURL or constants.xmlrpcServer, constants.transport)
    server.blogger.setTemplate(constants.applicationKey,
        str(blogID),
        str(username),
        str(password),
        text,
        templateType)

if __name__ == "__main__":
    try:
        import pydoc
        pydoc.help("blogger")
    except ImportError:
        print __doc__
