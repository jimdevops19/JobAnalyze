import psycopg2

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


            #Action
            self.cursor.execute(query)
            self.connection.commit()
            print("QUERY SUCCESS")

        except(Exception, psycopg2.Error) as error:
            raise Exception("Error while connecting to PostgreSQL", error)

        finally:
            if (self.connection != None):
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL connection is closed")

