import random
import mysql.connector
from faker import Faker

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="172.23.0.1",
    user="root",
    password="root",
    database="data"
)

# Creamos un objeto Faker
fake = Faker()

# Generamos datos de usuarios y telecomunicaciones y los insertamos en la base de datos
cursor = conn.cursor()

# Creamos una tabla para usuarios
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")

# Creamos una tabla para registros de telecomunicaciones
cursor.execute("CREATE TABLE IF NOT EXISTS telecom_data (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, phone_number VARCHAR(20), call_duration INT)")

# Generamos 100 usuarios y los insertamos en la tabla
for _ in range(100):
    name = fake.name()
    email = fake.email()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    user_id = cursor.lastrowid
    
    # Generamos registros de telecomunicaciones para cada usuario
    for _ in range(random.randint(1, 10)):
        #phone_number = fake.phone_number()
        phone_number = fake.phone_number()[:20]  # Recortamos el número a 20 caracteres
        call_duration = random.randint(1, 60)  # Duración de la llamada en segundos
        cursor.execute("INSERT INTO telecom_data (user_id, phone_number, call_duration) VALUES (%s, %s, %s)", (user_id, phone_number, call_duration))

# Guardamos los cambios
conn.commit()

# Cerramos la conexión
cursor.close()
conn.close()
