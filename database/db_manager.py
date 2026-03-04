import psycopg2
from psycopg2 import Error
from models.documento import Documento

class DatabaseManager:
    def __init__(self):
        self.conexion_params = {
            "host": "localhost",
            "database": "pyobsidian_db",
            "user": "postgres",
            "password": "1234",
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

    def actualizar_datos(self, id_documento: int, texto_raw: str) -> bool:
        conexion = self.obtener_conexion()
        if not conexion:
            print("No se pudo establecer la conexión para actualizar.")
            return False

        query = """
                UPDATE documentos
                SET contenido_raw = %s
                WHERE id = %s; \
                """
        valores = (texto_raw, id_documento)
        exito = False

        try:
            cursor = conexion.cursor()
            cursor.execute(query, valores)

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"Documento (ID: {id_documento}) actualizado con éxito en PostgreSQL.")
                exito = True
            else:
                print(f"Advertencia: No se encontró el documento con ID {id_documento}.")
                conexion.rollback()

        except Error as e:
            conexion.rollback()
            print(f"Error crítico en PostgreSQL al actualizar: {e}")
            raise

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return exito

    def eliminar_documento(self, id_documento: int) -> bool:
        conexion = self.obtener_conexion()
        if not conexion:
            print("No se pudo establecer la conexión para eliminar.")
            return False

        # Query de borrado filtrando estrictamente por el ID
        query = "DELETE FROM documentos WHERE id = %s;"
        valores = (id_documento,)
        exito = False

        try:
            cursor = conexion.cursor()
            cursor.execute(query, valores)

            # Verificamos si Postgres eliminó alguna fila
            if cursor.rowcount > 0:
                conexion.commit()  # Confirmamos la destrucción del dato
                print(f"Documento (ID: {id_documento}) eliminado físicamente de PostgreSQL.")
                exito = True
            else:
                print(f"Advertencia: No se encontró el documento con ID {id_documento} para eliminar.")
                conexion.rollback()  # Cancelamos por precaución

        except Error as e:
            conexion.rollback()
            print(f"Error crítico en PostgreSQL al intentar eliminar: {e}")
            raise

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return exito

    def obtener_todos(self) -> list[Documento]:
        conexion = self.obtener_conexion()
        if not conexion:
            print("No se pudo conectar a la base de datos para cargar las notas.")
            return []

        documentos_cargados = []

        query = "SELECT id, titulo, contenido_raw, fecha_creacion FROM documentos ORDER BY id ASC;"

        try:
            cursor = conexion.cursor()
            cursor.execute(query)

            filas = cursor.fetchall()

            for fila in filas:
                nota_recuperada = Documento(
                    id_documento=fila[0],
                    titulo=fila[1],
                    contenido_raw=fila[2],
                    fecha_creacion=fila[3]
                )
                documentos_cargados.append(nota_recuperada)

            print(f"Se cargaron {len(documentos_cargados)} documentos desde la base de datos.")

        except Error as e:
            print(f"Error al obtener los documentos de Postgres: {e}")

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return documentos_cargados