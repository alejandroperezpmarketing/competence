from connPOO import Conn


class Operation_table():
    
    
    #Select betweet thre diferent tables
    def __init__(self) -> None:
        self._table_type = None
        self._q = None
        self._operationType = None



    #Properties
        
    def _set_table_type(self, code):
        self._table_type = code
    
    def _get_table_type(self):
        return self._table_type
    
    table_type = property(fget=_get_table_type, fset=_set_table_type)

    # select text

    def _set_q(self, code):
        self._q = code
    
    def _get_q(self):
        return self._q
    
    q = property(fget=_get_q, fset=_set_q)

    # Operation type

    def _set_operation_type(self, code):
        self._operationType = code
    def _get_operation_type(self):
        return self._operationType
    
    operation_type = property(fget=_get_operation_type, fset=_set_operation_type)




    ## 3 diferent types
    
    """
    one polygions
    one points
    one lines
    
    """

    def _operations(self):
        
        def insert(self,descripcion, geomWkt, q)->int:
            Conn._conn.cursor.execute(q,[descripcion,geomWkt, geomWkt])
            Conn._conn.conn.commit()
            gid = Conn._conn.cursor.fetchall()[0][0]
            return {'ok':True,'message':f'Edificio insertado. gid: {gid}','data':[[gid]]}

        #Buildings
        
        """

        if self._table_type.UPPER() in ["buildings"]:
            if self._operationType.UPPER() == "INSERT":

                def insert(self,descripcion, geomWkt, q)->int:
                    self._conn.cursor.execute(q,[descripcion,geomWkt, geomWkt])
                    self.conn.conn.commit()
                    gid = self.conn.cursor.fetchall()[0][0]
                    return {'ok':True,'message':f'Edificio insertado. gid: {gid}','data':[[gid]]}
                
            elif self._operationType.UPPER() == "DELETE":
                pass
            elif self._operationType.UPPER() == "UPDATE":
                pass
            else:
                print('ERROR: None operation inserted')
            """

        def db_operations(self):
            return self._operations()
        



