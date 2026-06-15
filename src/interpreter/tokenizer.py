def dividir(texto: str) -> list[str]:
    """Divide el texto en tokens (lista de strings).

    Entrada:  "abrir firefox https://notion.so"
    Salida:   ["abrir", "firefox", "https://notion.so"]
    """
    return texto.strip().split()
