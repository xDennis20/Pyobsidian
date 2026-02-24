import psycopg2
from psycopg2 import Error
from models.documento import Documento

class DatabaseManager:
    def __init__(self):
        # Configura tus credenciales reales aquí
        self.conexion_params = {
            "host": "localhost",
            "database": "pyobsidian_db",
            "user": "postgres",
            "password": "1234", # Reemplaza con tu clave
            "port": "5432"
        }

    def obtener_conexion(self):
        try:
            conexion = psycopg2.connect(**self.conexion_params)
            return conexion
        except Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            return None

    def insertar_documento(self, documento: Documento) -> int:
        conexion = self.obtener_conexion()

        if not conexion:
            print("No se pudo establecer la conexión para insertar.")
            return None

        # query de psycopg2
        query = """
            INSERT INTO documentos (titulo, contenido_raw, contenido_procesado)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        valores = (documento.titulo, documento.contenido_raw, documento.contenido_procesado)
        id_generado = None

        try:
            cursor = conexion.cursor()
            cursor.execute(query, valores)
            resultado = cursor.fetchone()
            if resultado:
                id_generado = resultado[0]
            conexion.commit()
            print(f"Documento '{documento.titulo}' guardado con éxito (ID: {id_generado})")

        except Error as e:
            conexion.rollback()
            print(f"Error al insertar el documento: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return id_generado