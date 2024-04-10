Module  : gadflyDatabase
Date    : 21st December, 2002
Author  : Andy Todd <andy47@halfcooked.com>

gadflyDatabase extends the flatfileDatabase module and sample. It implements a different kind of persistent storage, using the relational database gadfly.

This provides all of the usual ACID properties of a relational database to the generic storage framework of PythonCard.

The main classes, GadflyDatabase and Document in the module gadflyDatabase.py are direct sub classes of the classes in flatfileDatabase.py. They share, where possible, method names and properties. The major difference is that the flatfileDatabase sample needs an initialisation property called dataFile whereas gadflyDatabase requires three properties; dbDir, dbName and tableName.

For it to work properly you will need to have gadfly installed. Get it from;
  http://gadfly.sourceforge.net/

