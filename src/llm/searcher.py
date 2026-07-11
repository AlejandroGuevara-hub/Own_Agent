"""Búsqueda web con DuckDuckGo y resumen vía Ollama.

Usa duckduckgo-search para obtener resultados y llama a Ollama
para resumirlos en español.
"""

from ddgs import DDGS
import ollama

SEARCH_PROMPT = """Eres un asistente que resume resultados de búsqueda web.
El usuario hizo una consulta específica. Tienes resultados de búsqueda.

REGLAS ESTRICTAS:
- Responde SOLO lo que el usuario preguntó, ignorando información no relacionada
- Si los resultados no responden directamente la pregunta, dilo claramente
- Resume en máximo 3 oraciones claras y directas en español
- No inventes datos, solo usa lo que está en los resultados
- Para preguntas de precios o tasas, da el número exacto si aparece en los resultados

Responde solo el resumen, sin introducciones."""


def consultar(query: str) -> str:
    """Busca ``query`` en DuckDuckGo y resume los resultados con Ollama.

    Args:
        query: Texto de la consulta.

    Returns:
        Resumen en español, o mensaje de error si falla.
    """
    try:
        with DDGS() as ddgs:
            resultados = list(ddgs.text(query, max_results=3))
        if not resultados:
            return "No se encontraron resultados para esa consulta."
        contexto = "\n\n".join([
            f"Título: {r['title']}\nFragmento: {r['body']}"
            for r in resultados
        ])
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": SEARCH_PROMPT},
                {"role": "user", "content": f"Consulta: {query}\n\nResultados:\n{contexto}"},
            ],
        )
        return response["message"]["content"].strip()
    except Exception as e:
        return f"Error al consultar: {str(e)}"
