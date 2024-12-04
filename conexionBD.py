import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="bi9leynoezww1rlttbhg-mysql.services.clever-cloud.com",
        user="uelsnbat9itfjdbu",
        password="xRYdJd9vYky0AUyukEOw",
        database="lbi9leynoezww1rlttbhg"
    )
