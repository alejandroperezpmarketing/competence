import connPOO as conndb

db = conndb.Conn()

###FIRST STEP ¿WHICH DATABASE I NEED TO CONNECT?

db.database="desweb"
db.user="postgres"
db.password="postgres"
db.host="localhost"
db.port=5432

db.connectdb()

### SECOND STEP ¿WHICH TABLE DO I NEED TO USE?

#db.tabledb = ""

print(db)
#db.connectdb(user, password, host, port, database)
