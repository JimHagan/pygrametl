"""
This is a slightly modified test script based on one at http://pygrametl.org/.
I've modified it for compatibility with MySQL.  The pygrametl package relies on
PEP 249 data connections.  I've used MySQLdb which is said to be mostly PEP 249
compliant.

One caveat about pygrametl is that it does not initialize schemae.
Therefore it is necessary to run the companion sql create
script found in the companion file example.sql.
"""
import MySQLdb
import pygrametl
from pygrametl.tables import Dimension

# Input is a list of "rows" which in pygrametl is modelled as dict
products = [
    {'name' : 'Calvin and Hobbes 1', 'category' : 'Comic', 'price' : '10'},
    {'name' : 'Calvin and Hobbes 2', 'category' : 'Comic', 'price' : '10'},
    {'name' : 'Calvin and Hobbes 3', 'category' : 'Comic', 'price' : '10'},
    {'name' : 'Cake and Me', 'category' : 'Cookbook', 'price' : '15'},
    {'name' : 'French Cooking', 'category' : 'Cookbook', 'price' : '50'},
    {'name' : 'Sushi', 'category' : 'Cookbook', 'price' : '30'},
    {'name' : 'Nineteen Eighty-Four', 'category' : 'Novel', 'price' : '15'},
    {'name' : 'The Lord of the Rings', 'category' : 'Novel', 'price' : '60'}
]

mysqlconn = MySQLdb.connect(host='127.0.0.1', db='test', user='', passwd='')


# This ConnectionWrapper will be set as default and is then implicitly used.
# A reference to the wrapper is saved to allow for easy access of it later
conn = pygrametl.ConnectionWrapper(connection=mysqlconn)

# The instance of Dimension connects to the table "product" in the
# database using the default connection wrapper we just created, the
# argument "lookupatts" specifies the column which needs to match
# when doing a lookup of the key from this dimension
productDimension = Dimension(
    name='product',
    key='productid',
    attributes=['name', 'category', 'price'],
    lookupatts=['name'])

# Filling a dimension is simply done by using the insert method
for row in products:
    productDimension.insert(row)
conn.commit()
conn.close()
