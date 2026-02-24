
from models.documento import Documento

class GestorNotas:
    def __init__(self):
        self.documentos: dict[int,Documento] = {}

    def agregar_documento(self,documento: Documento) -> None:
        if not isinstance(documento,Documento):
            raise ValueError("Error: El valor no es tipo objeto Documento")
        if not isinstance(documento.id_documento, int):
            raise ValueError("Error: ID del documento tiene que ser int")
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