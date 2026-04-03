from tools.scraper import scrape_website
from tools.searcher import search_web

TOOLS_DEFINITION = [
    {
        "name": "scrape_website",
        "description": (
            "Scrape le contenu textuel d'une page web à partir de son URL. "
            "À utiliser quand l'URL d'un site est connue et qu'on veut en extraire le contenu."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "L'URL complète de la page à scraper (ex: https://example.com).",
                }
            },
            "required": ["url"],
        },
    },
    {
        "name": "search_web",
        "description": (
            "Effectue une recherche web via DuckDuckGo et retourne les meilleurs résultats. "
            "À utiliser pour trouver des informations, des URLs ou analyser des concurrents."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "La requête de recherche.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Nombre de résultats à retourner (défaut : 5).",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
]


def execute_tool(name: str, inputs: dict) -> str:
    if name == "scrape_website":
        return scrape_website(**inputs)
    if name == "search_web":
        return search_web(**inputs)
    return f"Outil inconnu : {name}"
