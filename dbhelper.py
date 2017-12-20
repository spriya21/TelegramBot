import sqlite3


class DBHelper:
    # Takes db name & creates db connection
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    # Creates table 'items' with column 'description'
    def setup(self):
        print("creating table")
        stmt = "Create table if not exists items(description text, owner text)"
        itemidx = "Create index if not exists itemIndex on items (description ASC)"
        ownidx = "Create index if not exists ownIndex ON items (owner ASC)"
        self.conn.execute(stmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.commit()

    # Takes text from item_text and inserts to database
    def add_item(self, item_text, owner):
        stmt = "Insert into items (description, owner) Values (?, ?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "Delete from items where Description = (?) AND owner = (?)"
        args = (item_text, owner)
        self.conn.execute(stmt, args)
        self.conn.commit()

    # get_items() returns a list of items from database
    # Using list comprehension, first element of each item
    # SqLite returns data in tuple format

    def get_items(self, owner):
        stmt = "Select description from items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]



