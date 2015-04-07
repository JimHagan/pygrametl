"""
This is a slightly modified test script based on one at http://pygrametl.org/.
I've modified it for compatibility with MySQL.  The pygrametl package relies on
PEP 249 data connections.  I've used MySQLdb which is said to be mostly PEP 249
compliant.

One caveat about pygrametl is that it does not initialize schemae.
Therefore it is necessary to run the companion sql create
script found in the companion file example2.sql.
"""
import MySQLdb
import pygrametl
from pygrametl.tables import SlowlyChangingDimension

# Input is a list of "rows" which in pygrametl is modelled as dict
products = [
    {'name' : 'Calvin and Hobbes', 'category' : 'Comic', 'price' : '20',
     'date' : '1990-10-01'},
    {'name' : 'Calvin and Hobbes', 'category' : 'Comic', 'price' : '10',
     'date' : '1990-12-10'},
    {'name' : 'Calvin and Hobbes', 'category' : 'Comic', 'price' : '20',
     'date' : '1991-02-01'},
    {'name' : 'Cake and Me', 'category' : 'Cookbook', 'price' : '15',
     'date' : '1990-05-01'},
    {'name' : 'French Cooking', 'category' : 'Cookbook', 'price' : '50',
     'date' : '1990-05-01'},
    {'name' : 'Sushi', 'category' : 'Cookbook', 'price' : '30',
     'date' : '1990-05-01'},
    {'name' : 'Nineteen Eighty-Four', 'category' : 'Novel', 'price' : '15',
     'date' : '1990-05-01'},
    {'name' : 'The Lord of the Rings', 'category' : 'Novel', 'price' : '60',
     'date' : '1990-05-01'}
]

# The actual database connection is handled using a PEP 249 connection
mysqlconn = MySQLdb.connect(host='127.0.0.1', db='test', user='', passwd='')

# This ConnectionWrapper will be set as default and is then implicitly used.
# A reference to the wrapper is saved to allow for easy access of it later
conn = pygrametl.ConnectionWrapper(connection=mysqlconn)

# The slowly changing dimension is created as type 2 only, as a new row is
# inserted with a from and to timestamps for each change in the dataset
# without changing any attributes in the existing rows, except validto
# which is a time stamp indicating when the row is no longer valid.
# As additional parameters, the object is initialised with information
# about which attribute holds a time stamp for when the row's validity
# starts and ends. The parameter fromfinder is also given, which is must be
# set to the function that should be used to compute the time stamp for
# when the row becomes valid and given as input the name of the row which
# value it should use. In this example, the function datareader from
# pygrametl is used which converts time stamp from a string to a Python
# datetime.date object to simplify the conversion to the Postgres Date type.
productDimension = SlowlyChangingDimension (
    name='product_with_date',
    key='productid',
    attributes=['name', 'category', 'price', 'validfrom', 'validto',
                'version'],
    lookupatts=['name'],
    fromatt='validfrom',
    fromfinder=pygrametl.datereader('date'),
    toatt='validto',
    versionatt='version')

# scdensure extends the existing ensure methods to provide support for
# updating slowly changing attributes for rows where lookupparts match, but
# other differences exist. This is done by increamenting the version
# attribute for the new row, and assigning the new rows fromatt to the old
# rows toatt, indicating that the validity of the old row has ended.
for row in products:
    productDimension.scdensure(row)

# To ensure all cached data is inserted and the transaction committed
# both the commit and close function should be called when done
conn.commit()
conn.close()