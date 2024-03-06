import connPOO as conndb
import operations_in_tables as oit

db = conndb.Conn()
oit = oit.Operation_table()

###FIRST STEP ¿WHICH DATABASE I NEED TO CONNECT?

#db.database="desweb"
db.database="postgres"
db.user="postgres"
db.password="admin"
db.host="localhost"
db.port=5432
oit.table_type="buildings"
oit.operation_type = "insert"
oit.q =f"{oit._operationType} into d.{oit._table_type} (descripcion,area, geom) values (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) returning gid"

db.connectdb()
oit._operations()



### SECOND STEP ¿WHICH TABLE DO I NEED TO USE?

#db.tabledb = ""

print(db)
#db.connectdb(user, password, host, port, database)
