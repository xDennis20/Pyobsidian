from logic.convertidor import Convertidor

class Documento:

    def __init__(self, id_documento: int | None,
                 titulo: str,
                 contenido_raw: str,
                 fecha_creacion: str | None):
        self.id_documento = id_documento
        self.titulo = titulo
        self.contenido_raw = contenido_raw
        self.fecha_creacion = fecha_creacion

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self,titulo: str):
        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("Error: Titulo Vacio")
        self._titulo = titulo

    @property
    def contenido_procesado(self):
        return self._contenido_procesado

    @property
    def contenido_raw(self):
        return self._contenido_raw

    @contenido_raw.setter
    def contenido_raw(self,texto_raw: str):
        if not texto_raw or len(texto_raw.strip()) == 0:
            raise ValueError("Error: Texto vacio")
        self._contenido_raw = texto_raw
        self._contenido_procesado = Convertidor.convertir_a_html(texto_raw)

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id_documento},titulo={self._titulo})"