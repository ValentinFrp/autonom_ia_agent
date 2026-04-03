import anthropic
from config.settings import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_AGENT_ITERATIONS
from agent.tools import TOOLS_DEFINITION, execute_tool
from models.task import AgentResult, TaskStatus, ToolCall

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Tu es un agent IA autonome. Tu reçois une tâche et tu l'accomplis en utilisant les outils à ta disposition.

Stratégie :
1. Analyse la tâche et détermine les étapes nécessaires.
2. Utilise les outils pour collecter les informations.
3. Enchaîne les appels d'outils si nécessaire (recherche → scraping → analyse).
4. Quand tu as suffisamment d'informations, rédige un rapport final structuré en français.

Le rapport final doit contenir : un résumé exécutif, les points clés découverts, et une conclusion."""


def run_agent(task: str) -> AgentResult:
    messages = [{"role": "user", "content": task}]
    tool_calls_history: list[ToolCall] = []
    iterations = 0

    while iterations < MAX_AGENT_ITERATIONS:
        iterations += 1

        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS_DEFINITION,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            summary = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "Aucun résumé généré.",
            )
            return AgentResult(
                task=task,
                summary=summary,
                tool_calls=tool_calls_history,
                iterations=iterations,
                status=TaskStatus.COMPLETED,
            )

        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type != "tool_use":
                    continue

                output = execute_tool(block.name, block.input)
                tool_calls_history.append(ToolCall(name=block.name, inputs=block.input, output=output))

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

            messages.append({"role": "user", "content": tool_results})

    return AgentResult(
        task=task,
        summary="Limite d'itérations atteinte sans conclusion.",
        tool_calls=tool_calls_history,
        iterations=iterations,
        status=TaskStatus.FAILED,
    )
