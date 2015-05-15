################################################################################
#
#  sqlite_using_jdbc - An example of using straight JDBC mechanisms to
#                      interact with a SQLite database.
#                      Creates a 'planet' table in a SQLite database
#                      named 'solarsys.db', populates it with some data and 
#                      then executes a query to retrieve data from that table.
#
#  Works with Jython 2.5, must have the zentus sqlitejdbc.jar in your
#  CLASSPATH at execution time.
#  Known to work with sqlitejdbc-v056.jar
#
################################################################################

import sys

from java.lang import Class
from java.sql  import DriverManager, SQLException

################################################################################

DATABASE    = "solarsys.db"
JDBC_URL    = "jdbc:sqlite:%s"  % DATABASE
JDBC_DRIVER = "org.sqlite.JDBC"

TABLE_NAME      = "planet"
TABLE_DROPPER   = "drop table if exists %s;"                      % TABLE_NAME
TABLE_CREATOR   = "create table %s (name, size, solar_distance);" % TABLE_NAME
RECORD_INSERTER = "insert into %s values (?, ?, ?);"              % TABLE_NAME
PLANET_QUERY = """
select name, size, solar_distance
from %s
order by size, solar_distance desc
""" % TABLE_NAME

PLANET_DATA = [('mercury' , 'small' ,    57),  # distance in million kilometers
               ('venus'   , 'small' ,   107),
               ('earth'   , 'small' ,   150),
               ('mars'    , 'small' ,   229),
               ('jupiter' , 'large' ,   777),
               ('saturn'  , 'large' ,   888),
               ('uranus'  , 'medium',  2871),
               ('neptune' , 'medium',  4496),
               ('pluto'   , 'tiny'  ,  5869),
              ]

################################################################################

def main():
    dbConn = getConnection(JDBC_URL, JDBC_DRIVER)
    stmt = dbConn.createStatement()
    try:
        stmt.executeUpdate(TABLE_DROPPER)
        stmt.executeUpdate(TABLE_CREATOR)
    except SQLException, msg:
        print msg
        sys.exit(1)

    if populateTable(dbConn, PLANET_DATA):
        resultSet = stmt.executeQuery(PLANET_QUERY)
        while resultSet.next():
            name = resultSet.getString("name")
            size = resultSet.getString("size")
            dist = resultSet.getInt   ("solar_distance")
            print "%-16.16s  %-8.8s  %4d" % (name, size, dist)
   
    stmt.close()
    dbConn.close()
    sys.exit(0)

################################################################################

def getConnection(jdbc_url, driverName):
    """
        Given the name of a JDBC driver class and the url to be used 
        to connect to a database, attempt to obtain a connection to 
        the database.
    """
    try:
        Class.forName(driverName).newInstance()
    except Exception, msg:
        print msg
        sys.exit(-1)

    try:
        dbConn = DriverManager.getConnection(jdbc_url)
    except SQLException, msg:
        print msg
        sys.exit(-1)

    return dbConn

################################################################################

def populateTable(dbConn, feedstock):
    """
        Given an open connection to a SQLite database and a list of tuples
        with the data to be inserted, insert the data into the target table.
    """
    try:
        preppedStmt = dbConn.prepareStatement(RECORD_INSERTER)
        for name, size, distance in feedstock:
            preppedStmt.setString(1, name)
            preppedStmt.setString(2, size)
            preppedStmt.setInt   (3, distance)
            preppedStmt.addBatch()
        dbConn.setAutoCommit(False)
        preppedStmt.executeBatch()
        dbConn.setAutoCommit(True)
    except SQLException, msg:
        print msg
        return False

    return True

################################################################################
################################################################################

if __name__ == '__main__':
    main()