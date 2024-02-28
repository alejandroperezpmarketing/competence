import connPOO
import psycopg2

db = connPOO.Conn()

db.user = "alpepea1_admin"
db.password = "Scoutalex1995_"
db.port = 5432
db.database = "alpepea1_training"
db.host = "158.42.250.241"

#db.connectdb(user, password, host, port, database)
