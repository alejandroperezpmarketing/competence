'''
Created on 27 feb. 2024

@author: vagrant
'''
from connPOO import Conn


def insertBuilding(conn:Conn, descripcion, geomWkt)->int:
    q ="insert into d.buildings (descripcion,area, geom) values (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830))"
    conn.cursor.execute(q,[descripcion,geomWkt, geomWkt])
    conn.conn.commit()
 
 
def updateBuilding(conn:Conn, gid, descripcion, geomWkt)->int:
    q ="update d.buildings set (descripcion,area, geom) = (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) where gid = %s"
    conn.cursor.execute(q,[descripcion,geomWkt, geomWkt, gid])
    conn.conn.commit() 
    
class Buildings():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert(self,descripcion, geomWkt)->int:
        q ="insert into d.buildings (descripcion,area, geom) values (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[descripcion,geomWkt, geomWkt])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return gid
     
     
    def update(self,gid, descripcion, geomWkt)->int:
        q ="update d.buildings set (descripcion,area, geom) = (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) where gid = %s"
        self.conn.cursor.execute(q,[descripcion,geomWkt, geomWkt, gid])
        self.conn.conn.commit()     
    
