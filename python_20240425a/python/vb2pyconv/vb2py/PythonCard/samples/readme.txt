The main purpose of the samples is to "stress" the PythonCard framework and
make sure that the framework is robust and full-featured, yet still simple
for the beginner to use. "We learn by doing". As users (programmers) write
more samples, we are able to identify which portions of the framework are
missing, too simplistic or too complex or just plain broken. The
PythonCard API changes as we identify these issues and fix the
framework and the samples always represent the latest version of the API.
We don't have a complete API yet, that is why we refer to the code as a
PythonCard prototype.

The ongoing list of things that needs to be added to PythonCard is
represented by the Feature Requests here:
http://sourceforge.net/tracker/?atid=369015&group_id=19015&func=browse
You can also view this list using the SourceForgeTracker sample.

It is essential that we create lots of samples to identify framework issues
in order to avoid creating a framework only suitable for simplistic "toy"
programs that are only one step beyond "hello world". Equally bad would be a
framework that is too general and requires the user to do a lot of work just
to write a basic program; simple programs should be simple to write; That is
the reason we aren't forcing a model-view-controller (MVC) paradigm on the
user, MVC is not easy to grasp or use correctly.

The samples also serve as a learning tool. Since there is little
documentation for PythonCard right now, the best way to learn to use
PythonCard is to copy and modify the samples. Note that due to the current
limitations of the framework, some samples use wxPython method calls
directly. The wxPython calls can usually be identified via the method name
which will start with a capital letter (e.g. GetSize instead of getSize).

Please help the PythonCard project, by submitting your own samples and
asking questions about PythonCard on the mailing list:
http://lists.sourceforge.net/lists/listinfo/pythoncard-users
