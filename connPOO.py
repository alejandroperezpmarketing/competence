'''
Created on 27 feb. 2024

@author: vagrant
'''
import psycopg2
import settings

class Conn():
    conn=None
    cursor=None
    def __init__(self):
        self._user = None
        self._password = None
        self._port = None
        self._host = None
        self._database = None


    
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
        self._port = code
    def _get_host(self):
        return self._port
    host = property(fget=_get_host,fset=_set_host)

    
    #SYSTEM METHODS
    
    def _connect(self, user, password, host, port, database):
        psycopg2.connect(database=self._database,
                         user=user,
                         password=self._password,
                         host=self._host,
                         port=self._port)
        

    # USER METHODS
        
    def connectdb(self):
        self._connect(self._user, self._password, self._host, self._port, self._database)

    def close(self):
        self.conn.close()
    





        
