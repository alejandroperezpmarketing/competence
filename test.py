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
db.q ="CREATE TABLE public.test (id serial PRIMARY KEY, num integer, data varchar);"

db.execute()

#oit._operations()
#q = "create schema project"
#q1 = "create table project.buildings (gid serial primary key,description varchar)"

#db._conn.cursor.execute(q)
#db._conn.conn.commit()
#gid = db._conn.cursor.fetchall()[0][0]
#message = {'ok':True,'message':f'Edificio insertado. gid: {gid}','data':[[gid]]}
#print(message)

### SECOND STEP ¿WHICH TABLE DO I NEED TO USE?

#db.tabledb = ""

print(db)
#db.connectdb(user, password, host, port, database)
