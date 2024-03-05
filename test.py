import connPOO as conndb

db = conndb.Conn()

db.database="desweb"
db.user="postgres"
db.password="postgres"
db.host="localhost"
db.port=5432

print(db)
#db.connectdb(user, password, host, port, database)
