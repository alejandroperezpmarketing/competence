'''
Created on 27 feb. 2024

@author: vagrant
'''
import psycopg2
import json

class Conn():
    conn=None
    cursor=None
    def __init__(self):
        self._user = None
        self._password = None
        self._port = None
        self._host = None
        self._database = None
        self._conn = None
        self._cursor = None
        self._q = None

    def __repr__(self):
        report = {
           'user': self._user,
           'password': '*******',
           'port': self._port,
           'host': self._host,
           'database': self._database
           }
        
        report = json.dumps(report, indent=4)
        
        return report

    #Properties ******
    
    #DATABASE **************
        
    def _set_database(self,code):
        self._database = code
    def _get_database(self):
        return self._database
    
    database = property(fget=_get_database,fset=_set_database)
    
    #USER **************

    def _set_user(self,code):
        self._user =code
    def _get_user(self):
        return self._user
    user = property(fget=_get_user,fset=_set_user)

    #PASWORD **************

    def _set_password(self,code):
        self._password = code
    def _get_password(self):
        return self._password
    password = property(fget=_get_password,fset=_set_password)

    #PORT **************

    def _set_port(self,code):
        self._port=code
    def _get_port(self):
        return self._port
    port = property(fget=_get_port,fset=_set_port)

    #HOST ***********

    def _set_host(self,code):
        self._host = code
    def _get_host(self):
        return self._host
    host = property(fget=_get_host,fset=_set_host)
    
     # select text

    def _set_q(self, code):
        self._q = code
    
    def _get_q(self):
        return self._q
    
    q = property(fget=_get_q, fset=_set_q)

    
    ######## CONNECT TO THE DATABASE
    
    def _connectdb(self):
        
        global cursor
        
        self._conn = psycopg2.connect(user=self._user, password=self._password, host=self._host, port=self._port, database=self._database)
        
        
        return self._conn

    
    
    ## USER METHODS

    def _operation(self):
        self._cursor = self._conn.cursor()

        if self._q == None:
            print("Insert a operation to do")
        else:
            self._cursor.execute(self._q)

    def _closedb(self):
        self._conn.close()

    def execute(self):
        
        self._connectdb()
        self._operation()
        self._closedb()
        print('Connection successful')
        
    