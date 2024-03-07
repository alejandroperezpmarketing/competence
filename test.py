import connPOO as conndb
import operations_in_tables as oit

db = conndb.Conn()

###FIRST STEP ¿WHICH DATABASE I NEED TO CONNECT?

#db.database="desweb"
db.database="postgres"
db.user="postgres"
db.password="admin"
db.host="localhost"
db.port=5432


db.connect()
db.check_db_availability()

