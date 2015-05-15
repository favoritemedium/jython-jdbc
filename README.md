# jython-jdbc
Example of connecting to a database with Jython

This script
- Creates a new sqlite database called "solarsys.db" in the same directory as this script.
- Inserts some random data.
- Queries the database and prints out data to the console.

To run it
- Install jython (for e.g., using brew, "brew install jython")
- Download the latest stable sqlite-jdbc driver (https://bitbucket.org/xerial/sqlite-jdbc/downloads)
- Add the driver to your classpath
	- export CLASSPATH=`pwd`/sqlite-jdbc-3.8.7.jar
- Run using jython sample.py