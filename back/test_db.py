from database import engine

try:
    connection = engine.connect()
    print("Conectado correctamente")
    connection.close()
except Exception as e:
    print("Error:", e)