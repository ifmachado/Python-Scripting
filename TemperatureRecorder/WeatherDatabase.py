
import sqlite3


class WeatherDatabase:

    # class constructor will create sq3lite database with named passed when object is created.
    # it also initiates the cursor.
    def __init__(self, path):
        self.db = sqlite3.connect(path)
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

    # this method adds data to the table. Arguments passed must match the columns in database,
    # which are city, date and temperature.
    def add_info(self, city, date, temperature):
        # insert into city, date and temperarture columns the values passed as arguments.
        self.cursor.execute('''INSERT INTO temperatures(city, date, temperature) values(?,?,?)''',
                            (city, date, temperature))
        self.db.commit()

    # this method gets info from specific table lines where conditions are met.
    # table, primary column are main parameters and therefore required so specific lines can be found.
    # method also allows for secondary column, max_column and group values to be passed (default values set to None)
    # so it will only return lines that have the highest value in max_column within the specified group.
    def get_info(self, table, primary_col, value, secondary_col=None, max_col=None, group=None):
        # no max_col and group col have been passed,
        # so method will return all lines that match the primary column and value conditions
        if max_col is None and group is None:

            # query will be formatted with table name and primary column passed as arguments.
            query = f'''SELECT * FROM {table} where {primary_col} = ? '''

            # cursor will execute query with the value passed as argument (this value integrates the conditional
            # statement - ie. 'where column = value')
            self.cursor.execute(query, (value,))

            # look for all lines that match and add to array.
            my_list = self.cursor.fetchall()

        # max value and order have been passed as arguments
        else:
            # query will group lines according to group argument,
            # check for all lines that have value (passed as argument) in the primary_column
            # and then return only the line that has the highest value in max_col
            query = f'''SELECT {primary_col}, {secondary_col},MAX({max_col}) FROM {table} WHERE {primary_col} = ? GROUP BY {group}'''
            self.cursor.execute(query, (value,))

            # look for all lines that conditions and add to array.
            my_list = self.cursor.fetchall()

        # check if the array length is bigger than 0, which means at least one line in the table match the conditions.
        if len(my_list) != 0:
            # Return list with all values from lines where conditions where matched.
            return my_list

        # line doesn't exist in the table. return False
        else:
            return False

    # this method updates information from a specific line
    def update_table(self, table, replace_col, id_col, replace_info, id_info):
        # query will be formatted with table name, column where value must be replaced and column that identifies the
        # line where value must be replaced (identifier).
        query = '''UPDATE %s SET %s = ? WHERE %s = ? ''' % (table, replace_col, id_col)

        # cursor will execute query with the values passed as parameter(the value that must the replaced the
        # one currently in the identifier column).
        self.cursor.execute(query, (replace_info, id_info))
        self.db.commit()

    # this method deletes a specific line in the table.
    def delete_info(self, table, col, id_info):
        # query will be formatted with table name and column (identifier) passed as parameters.
        query = '''DELETE FROM %s WHERE %s = ?; ''' % (table, col)

        # cursor will execute query with the value passed as parameter (this value integrates the conditional
        # statement - ie. 'where column = value')
        self.cursor.execute(query, (id_info,))
        self.db.commit()

    # this method checks a specific value passed is unique. It does so by selecting a particular column and value,
    # which will be the identifiers and checks the newly added information is in the database already.
    def is_unique(self, table, id_col, col, id_info, info):
        # query will be formatted with table name, identifier column and column (where the new info would be stored)
        # passed as parameters.
        query = '''SELECT * FROM %s WHERE %s = ? AND %s = ?''' % (table, id_col, col)

        # cursor will execute query with the value passed as parameter (this value integrates the conditional
        # statement - ie. 'where column = value')
        self.cursor.execute(query, (id_info, info))

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
