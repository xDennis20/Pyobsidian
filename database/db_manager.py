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
            INSERT INTO documentos (titulo, contenido_raw, contenido_procesado, usuario_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """
        valores = (documento.titulo, documento.contenido_raw, documento.contenido_procesado, documento.usuario_id)
        id_generado = None

        cursor = None
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

    def actualizar_datos(self, id_documento: int, texto_raw: str, usuario_id: int) -> bool:
        conexion = self.obtener_conexion()
        if not conexion:
            print("No se pudo establecer la conexión para actualizar.")
            return False

        query = """
                UPDATE documentos
                SET contenido_raw = %s
                WHERE id = %s AND usuario_id = %s;
                """
        valores = (texto_raw, id_documento, usuario_id)
        exito = False
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(query, valores)

            if cursor.rowcount > 0:
                conexion.commit()
                print(f"Documento (ID: {id_documento}) actualizado con éxito en PostgreSQL.")
                exito = True
            else:
                print(f"Advertencia: No se encontró el documento con ID {id_documento} o no te pertenece.")
                conexion.rollback()

        except Error as e:
            conexion.rollback()
            print(f"Error crítico en PostgreSQL al actualizar: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return exito

    def eliminar_documento(self, id_documento: int, usuario_id: int) -> bool:
        conexion = self.obtener_conexion()
        if not conexion:
            print("No se pudo establecer la conexión para eliminar.")
            return False

        query = "DELETE FROM documentos WHERE id = %s AND usuario_id = %s;"
        valores = (id_documento, usuario_id)
        exito = False
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(query, valores)

            # Verificamos si Postgres eliminó alguna fila
            if cursor.rowcount > 0:
                conexion.commit()  # Confirmamos la destrucción del dato
                print(f"Documento (ID: {id_documento}) eliminado físicamente de PostgreSQL.")
                exito = True
            else:
                print(f"Advertencia: No se encontró el documento con ID {id_documento} o no tienes permiso para eliminarlo.")
                conexion.rollback()  # Cancelamos por precaución

        except Error as e:
            conexion.rollback()
            print(f"Error crítico en PostgreSQL al intentar eliminar: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return exito

    def obtener_todos(self, usuario_id: int) -> list[Documento]:
        conexion = self.obtener_conexion()
        if not conexion:
            print("No se pudo conectar a la base de datos para cargar las notas.")
            return []

        documentos_cargados = []

        query = """
                SELECT id, titulo, contenido_raw, fecha_creacion, usuario_id
                FROM documentos
                WHERE usuario_id = %s
                ORDER BY id ASC;
                """

        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(query, (usuario_id,))
            filas = cursor.fetchall()

            for fila in filas:
                nota_recuperada = Documento(
                    id_documento=fila[0],
                    titulo=fila[1],
                    contenido_raw=fila[2],
                    fecha_creacion=fila[3],
                    usuario_id=fila[4]
                )
                documentos_cargados.append(nota_recuperada)

            print(f"Se cargaron {len(documentos_cargados)} documentos para el usuario {usuario_id}.")

        except Error as e:
            print(f"Error al obtener los documentos de Postgres: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        return documentos_cargados