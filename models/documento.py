class Documento:
    def __init__(self, id_documento: int | None,
                 titulo: str,
                 contenido_raw: str,
                 contenido_procesador: str,
                 fecha_creacion: str | None):
        self.id_documento = id_documento
        self._titulo = titulo
        self.contenido_raw = contenido_raw
        self.contenido_procesado = contenido_procesador
        self.fecha_creacion = fecha_creacion

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self,titulo: str):
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("Error: Titulo Vacio")
        self._titulo = titulo

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id_documento},titulo={self._titulo})"