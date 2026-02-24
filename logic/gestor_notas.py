from database.db_manager import DatabaseManager
from models.documento import Documento

class GestorNotas:
    def __init__(self):
        self.documentos: dict[int,Documento] = {}

    def agregar_documento(self,documento: Documento) -> None:
        if not isinstance(documento,Documento):
            raise ValueError("Error: El valor no es tipo objeto Documento")
        id_generado = DatabaseManager().insertar_documento(documento)
        if not id_generado:
            raise Exception("Error interno: No se pudo guardar el documento en la base de datos.")
        documento.id_documento = id_generado
        self.documentos[documento.id_documento] = documento
        print("Documento agregado correctamente")

    def buscar_por_titulo(self, titulo: str) -> list[Documento]:
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("Error: Titulo vacio")
        documentos_coincidencias = []
        for documento in self.documentos.values():
            if documento.titulo.lower() == titulo.lower():
                documentos_coincidencias.append(documento)
        return documentos_coincidencias

    def actualizar_contenido(self,id_documento: int,texto_raw: str) -> None:
        if id_documento not in self.documentos:
            raise KeyError("Error: No existe el documento")
        if not texto_raw or (len(texto_raw.strip()) == 0):
            raise ValueError("Error: Texto vacio")
        documento = self.documentos.get(id_documento)
        documento.contenido_raw = texto_raw

    def eliminar_documento(self,id_documento: int) -> None:
        if id_documento not in self.documentos:
            raise KeyError("Error: No existe el documento")
        self.documentos.pop(id_documento)