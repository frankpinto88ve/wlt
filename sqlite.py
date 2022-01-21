import sqlite3
from sqlite3 import Error

class SQLiteClient():
    """
    SQLite Client used to interact with SQLite DB
    """
    def __init__(self, db_name):
        """
        params:
            db_name (string): name of the SQLite database. If none exist at the moment of initiating
                              the client object, a new one will be created.
        """
        try:
            conn = sqlite3.connect(db_name)
            self.connection = conn
        except Error as e:
            print(e)

    def table_creator(self, table_name, column_list):
        """
        params:
            table_name (string): name of table to be created. If table already exists, then the
                                 command is ignored
            column_list (list[string]): list made up of elements that contains column name, data type and
                                        additional configuration paramenters to be created
                                        (ie: ['TWEET_ID INT NOT NULL', 'TWEET_TEXT TEXT'])
        """
        sql = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(table_name, ",".join(column_list))
        try:
            self.connection.execute(sql)
        except Error as e:
            print(e)
            return False
        else:
            return True

    def table_updater(self, table_name, data):
        """"
        params:
            table_name (string): table name where data will be appended
            data (string): list made up of the data to be appended in the required table. Must
                           Must have the same amount of elements and data types as those found
                           in the table.
        """
        col_names_table = [value[0] for value in self.connection.execute("SELECT * FROM {}".format(table_name)).description]
        sql_insert = """
        INSERT INTO {0} ({1})
        VALUES ({2})
        """.format(table_name, ",".join(col_names_table), ",".join(["?" for value in col_names_table]))
        try:
            self.connection.execute(sql_insert, data)
            self.connection.commit()
        except Error as e:
            print(e)
            return False
        else:
            return True

    def table_getter(self, sql_select):
        """
        params:
            sql_select (string): select statement
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_select)
        except Error as e:
            print(e)
            return None
        else:
            return cursor.fetchall()

if __name__ == "__main__":
    a = SQLiteClient("test.db")

    #print(a.table_creator('tweets', ['TWEET_ID TEXT NOT NULL', 'TWEET_TEXT TEXT', 'CREATED_AT TEXT NOT NULL', 'USER_NAME TEXT NOT NULL']))
    #print(a.table_updater('tweets',[]))
    #print(a.table_updater('tweets', ['4', 'a', '3','3']))
    print(a.table_getter('SELECT * FROM TWEETS'))
    #print(a.table_creator())

    #a.table_updater("user_info", ['PoleoRafael', 698859, 47362])
