from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# Global Variables
SQLITE                  = 'sqlite'

# Table Names
USERS           = 'users'
ADDRESSES       = 'addresses'