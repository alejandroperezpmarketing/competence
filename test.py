import connPOO as conndb
import connPOO
import operations_in_tables as oit

db = conndb.Conn()
operation = connPOO.Table_operations
###FIRST STEP ¿WHICH DATABASE I NEED TO CONNECT?

#db.database="desweb"
db.database="postgres"
db.user="postgres"
db.password="admin"
db.host="localhost"
db.port=5432

db.db_create = 'test'


db.connect()
#db.check_db_availability()

#operation.insert_in_table()
#db.createdb()


