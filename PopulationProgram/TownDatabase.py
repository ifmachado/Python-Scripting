
import sqlite3


# create new class called TownDatabase
class TownDatabase:

    # class constructor will create sq3lite database with named passed when object is created.
    # it also initiates the cursor.
    def __init__(self, name):
        self.db = sqlite3.connect(name)
        self.cursor = self.db.cursor()

    # this method creates a new table. Table and columns names are passed as parameters
    def add_table(self, table, cols):
        # query will be formatted with table name and columns passed as parameters.
        query = '''CREATE TABLE IF NOT EXISTS %s %s ''' % (table, cols)
        self.cursor.execute(query)
        self.db.commit()

    # this method adds a value to a specific column.
    def add_to_row(self, table, cols, values):
        # query will be formatted with table name, column and values passed as parameters.
        query = '''INSERT INTO %s%s  VALUES%s''' % (table, cols, values)
        self.cursor.execute(query)
        self.db.commit()

    # this method adds an entry to the table.
    def add_entry(self, town, population):
        self.cursor.execute('''INSERT INTO population(name, amount) values(?,?)''', (town, population))
        self.db.commit()

    # this method returns the values in all rows
    def get_all(self, table):
        # query will be formatted with table name and column passed as parameters.
        query = '''SELECT * FROM %s ''' % (table)

        # cursor will execute query
        self.cursor.execute(query)

        # look for all lines and add to array.
        my_list = self.cursor.fetchall()

        # check if the array length is bigger than 0, which means table is not empty
        if len(my_list) != 0:
            return my_list

        # table is empty
        else:
            return False

    # this method returns the values in all rows in the table sorted according to specific parameter
    def get_all_sorted(self, table, my_order, direction):
        # query will be formatted with table name and column passed as parameters.
        query = '''SELECT * FROM %s ORDER BY %s %s''' % (table, my_order, direction)

        # cursor will execute query
        self.cursor.execute(query)

        # look for all lines and add to array.
        my_list = self.cursor.fetchall()

        # check if the array length is bigger than 0, which means table is not empty
        if len(my_list) != 0:
            return my_list

        # table is empty
        else:
            return False

    # this method gets all the info from a specific table line where conditions are met
    def get_entry(self, table, col, value):
        # query will be formatted with table name and column passed as parameters.
        query = '''SELECT * FROM %s where %s = ? ''' % (table, col)

        # cursor will execute query with the value passed as parameter (this value integrates the conditional
        # statement - ie. 'where column = value')
        self.cursor.execute(query, (value,))

        # look for all lines that match and add to array.
        my_list = self.cursor.fetchall()

        # check if the array length is bigger than 0, which means the line exist in the table.
        if len(my_list) != 0:
            for my_tuple in my_list:
                # returns the line's values as a tuple
                return my_tuple

        # line doesn't exist in the table. return False
        else:
            return False

    # this method updates information from a specific line
    def update_entry(self, table, replace_col, id_col, replace_info, id_info):
        # query will be formatted with table name, column where value must be replaced and column that identifies the
        # line where value must be replaced (identifier).
        query = '''UPDATE %s SET %s = ? WHERE %s = ? ''' % (table, replace_col, id_col)

        # cursor will execute query with the values passed as parameter(the value that must the replaced the
        # one currently in the identifier column).
        self.cursor.execute(query, (replace_info, id_info))
        self.db.commit()

    # this method deletes a specific line in the table.
    def delete_entry(self, table, col, name):
        # query will be formatted with table name and column (identifier) passed as parameters.
        query = '''DELETE FROM %s WHERE %s = ?; ''' % (table, col)

        # cursor will execute query with the value passed as parameter (this value integrates the conditional
        # statement - ie. 'where column = value')
        self.cursor.execute(query, (name,))
        self.db.commit()

    # this method checks if name passed is unique.
    def unique_name(self, table, col, name):
        # query will be formatted with table name and column (identifier) passed as parameters.
        query = '''SELECT * FROM %s where %s = ? ''' % (table, col)

        # cursor will execute query with the value passed as parameter (this value integrates the conditional
        # statement - ie. 'where column = value')
        self.cursor.execute(query, (name,))

        # look for all lines that match and add to array.
        item = self.cursor.fetchall()

        # check if the array length is smaller than 1, means the value doesn't exist in the table already.
        if len(item) < 1:
            return True
        else:
            return False

    # this method closes the database.
    def close_database(self):
        print("Database is closed.")
        self.db.close()
