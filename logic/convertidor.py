import markdown

class Convertidor:
    @staticmethod
    def convertir_a_html(texto_raw: str) -> str:
        if not texto_raw:
            return ""
        return markdown.markdown(texto_raw)