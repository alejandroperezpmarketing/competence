'''
Created on 27 feb. 2024

@author: vagrant
'''
from connPOO import Conn
import buildingsPOO

#conn=Conn()
#buildingsPOO.insertBuilding(conn=conn, 
#                            descripcion='A ver si va', 
#                            geomWkt='POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))' )

#buildingsPOO.updateBuilding(conn=conn, 
#                            gid = 11, 
#                            descripcion= 'Soy el  11', 
#                            geomWkt = 'POLYGON((0 0, 100 0, 150 150, 0 100, 0 0))')

conn=Conn()
b=buildingsPOO.Buildings(conn)
gid=b.insert(descripcion='POO', geomWkt='POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))')
print(gid)
b.update(gid=10, descripcion='Soy el 10', geomWkt='POLYGON((0 0, 100 0, 150 150, 0 100, 0 0))')
conn.close()


print('Done')




