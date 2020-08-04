import psycopg2
import psycopg2.errors
import psycopg2.errorcodes
from converters import Converter

###
#This class is made to handle special Exception such as: Column not found!
#The Exception initializes a trigger to create the column by the time,
#some other query tried to insert a key-value with that exact column name
#When this Expection Raises, it will try to create the column.
###
class ColumnNotFoundException(Exception):
    def __init__(self, column, db_connection, table_name):
        self.column = column
        self.table_name = table_name
        self.db_connection = db_connection
        print(f'TRYING TO CREATE COLUMN:{self.column}...')
        self.db_connection.execute_query(query=Converter.add_column_query(
            table_name=table_name,
            column_name=self.column
        ))
    def __str__(self):
        return f'The column {self.column} does not exist!'

class DBSession():
    def __init__(self,user,password,host,port,database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

        self.connection = None
        self.cursor = None


    def connect(self):
        try:
            attempt_connection = psycopg2.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           port=self.port,
                                           database=self.database)
            return attempt_connection

        except:
            raise Exception('Connection Error')

    def execute_query(self, query):
        try:
            self.connection = self.connect()
            self.cursor = self.connection.cursor()
            print(self.connection.get_dsn_parameters(), "\n")


            self.cursor.execute(query)
            self.connection.commit()
            print('QUERY SUCCESS')
            return {'result':'SUCCESS',
                    'information': None}

        except (Exception,psycopg2.Error) as error:
            if error.pgcode and error.pgcode == psycopg2.errorcodes.UNDEFINED_COLUMN:
                undefined_column_name = str(error).split()[1].strip().replace('"','')
                print(f'UNDEFINED_COLUMN:{undefined_column_name}')
                return {'result':'COLUMN_NOT_FOUND_ERROR',
                        'information': undefined_column_name}
            else:
                print("Query Execution Error:", error)

                return {'result' : 'FAILURE',
                        'information': None}

        finally:
            if (self.connection != None):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")