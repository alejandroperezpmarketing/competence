import connPOO
import psycopg2

db = connPOO.Conn()

user = "postgres"
password = "postgres"
port = 5432
database = "desweb"
host = "localhost"

db.connectdb()