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
        self._databases_list = None
        self._db_create = None

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

    #  Create database

    def _set_db_create(self, code):
        self._db_create = code
    
    def _get_db_create(self):
        return self._db_create
    
    db_create = property(fget=_get_db_create, fset=_set_db_create)

    ######## CONNECT TO THE DATABASE
    
    def _connectdb(self):
        
        global cursor
        
        self._conn = psycopg2.connect(user=self._user, password=self._password, host=self._host, port=self._port, database=self._database)
        
        
        return self._conn

    
    
    ## SYSTEM METHODS ************

    def _operation(self):
        self._cursor = self._conn.cursor()

        if self._q == None:
            print("Insert a operation to do")
        else:
            self._cursor.execute(self._q)

    def _closedb(self):
        with self._conn as curs:
            curs.close()

        

    def _check_db_availability(self):
        # 1.  get a list of databases on the server

        databases_list = []
        db_list =  "SELECT datname FROM pg_database"
        with self._conn.cursor() as curs:
            curs.execute(db_list)
            for db in curs.fetchall():
                datname = db[0]
                databases_list.append(datname.upper())
        self._databases_list = databases_list
        print(self._databases_list)
        return self._databases_list

   
    
    # USER METHODS
        
    def _execute_connection(self):
        
        self._connectdb()
    
    def check_db_availability(self):
        self._check_db_availability()
    
    def createdb(self):
        self._createdb()

    def connect(self):
        self._execute_connection()
        
        #########**************
        #verify the conection is success
        if self._connectdb():
            print('True: Connection successful')
            print(f'Conection info : {self._conn}')
        else:
            print('False')

        ####***************
    def closedb(self):
        self._closedb()
        
        
    
class Table_operations():

    def __init__(self,tablename:str,conn:Conn) -> None:

        self._X = None
        self._Y = None
        self._Z = None
        self._M = None
        self._EPSG = None
        self._operationtype = None
        self._tablename = tablename
        self._conn:Conn=conn

        


   
    def insertintable(self, descripcion, geomWkt)->int:
        
        q =f"insert into project.{self._tablename} (descripcion,area, geom) values (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830))"
        with self._conn.cursor() as curs:
            curs.cursor.execute(q,[descripcion,geomWkt, geomWkt])
            curs.conn.commit()
 
    """
    #1 funcion que haga seleccione u tipo de tablas polygon, lines, points, values

    ###### ********* POINT

    POINT(X,Y)

    ###### ********* LINES

    ('LineString(X,Y)')

    ###### ********* POLYGON

    ('POLYGON((X,Y))')

    






    #2 . funcion que me haga una de las 4 operaciones

    insertar  -- INSERT
    seleccionar -- SELECT
    eliminar -- DELETE
    actualizar -- UPDATE
    """
conn=Conn()
w = Table_operations(tablename='Buildings',conn=conn)
w.insertintable(descripcion='test',geomWkt='test')






