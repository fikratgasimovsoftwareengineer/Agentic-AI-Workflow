# =============================================================
# main.py — Entry point ReasonerHub
# =============================================================
# Modalità:
#   1. DEMO automatica : esegue 5 query predefinite (una per agente)
#                        e popola MLflow con dati reali
#   2. INTERATTIVA     : l'utente scrive query liberamente
# =============================================================

from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table
from rich         import box

from tracking.ml_flow_tracker import init_mlflow
from orchestrator.root_orchestrator import RootOrchestrator

console = Console()

# ----------------------------------------------------------
# Query demo — una per ogni agente, progettate per mostrare
# tool call + self-reflection in MLflow
# ----------------------------------------------------------
DEMO_QUERIES = [
    {
        "query":       "Calcola la radice quadrata di 1764 e poi dimmi quanto fa 42 elevato alla terza.",
        "description": "MathAgent — tool calculate + più operazioni",
    },
    {
        "query":       "È vero che la Torre Eiffel è più alta dell'Empire State Building?",
        "description": "FactCheckerAgent — verifica storica con tool check_claim",
    },
    {
        "query":       (
            "Riassumi questo testo in massimo 3 punti chiave: "
            "Il machine learning è un sottoinsieme dell'intelligenza artificiale che permette ai sistemi "
            "di apprendere automaticamente dall'esperienza senza essere esplicitamente programmati. "
            "Si basa su algoritmi che analizzano dati, identificano pattern e prendono decisioni "
            "con minimo intervento umano. Le applicazioni spaziano dal riconoscimento vocale "
            "alla guida autonoma, dalla diagnosi medica ai sistemi di raccomandazione."
        ),
        "description": "SummarizerAgent — sintesi con extract_keypoints",
    },
    {
        "query":       (
            "Analizza questo codice Python e dimmi se ci sono problemi:\n"
            "def divide(a, b):\n"
            "    return a / b\n\n"
            "result = divide(10, 0)\n"
            "print(result)"
        ),
        "description": "CodeAnalyzerAgent — bug detection con analyze_code_structure",
    },
    {
        "query":       "Analizza il sentiment di questa frase: 'Questo prodotto è ASSOLUTAMENTE TERRIBILE! Non funziona, è uno spreco di soldi. Sono furioso!'",
        "description": "SentimentAgent — analisi emozioni con detect_sentiment_signals",
    },
]


# ----------------------------------------------------------
# Helpers di stampa
# ----------------------------------------------------------

def print_header():
    console.print(Panel.fit(
        "[bold cyan]ReasonerHub[/bold cyan]\n"
        "[dim]Multi-Agent System con Self-Reflection + MLflow Tracking[/dim]",
        border_style="cyan",
    ))
    console.print()


def print_result(result: dict, description: str = ""):
    """Stampa il risultato di una query in modo leggibile."""

    # Tabella metadati
    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    table.add_column("key",   style="dim",          width=22)
    table.add_column("value", style="bold white")

    table.add_row("Agente",            result["routed_to"])
    table.add_row("Routing method",    result["routing_method"])
    table.add_row("Confidence",        f"{result['confidence']:.2f}")
    table.add_row("Reflection rounds", str(result["reflection_rounds"]))
    table.add_row("Self corrected",    str(result["self_corrected"]))
    table.add_row("Tool chiamato",     result["tool_called"] or "—")

    # Colore confidence
    conf = result["confidence"]
    if conf >= 0.75:
        conf_color = "green"
    elif conf >= 0.5:
        conf_color = "yellow"
    else:
        conf_color = "red"

    console.print(Panel(
        f"[bold]Query:[/bold] {result['query'][:120]}{'...' if len(result['query']) > 120 else ''}\n"
        f"[dim]{description}[/dim]",
        border_style="blue",
        title="[blue]INPUT[/blue]",
    ))

    console.print(table)

    console.print(Panel(
        result["answer"],
        border_style=conf_color,
        title=f"[{conf_color}]RISPOSTA  (confidence: {conf:.2f})[/{conf_color}]",
    ))
    console.print()


# ----------------------------------------------------------
# Modalità DEMO
# ----------------------------------------------------------

def run_demo(orchestrator: RootOrchestrator):
    console.print("[bold yellow]▶  MODALITÀ DEMO — 5 query automatiche[/bold yellow]")
    console.print("[dim]Ogni query popola MLflow con params, metrics e artifacts.[/dim]\n")

    for i, item in enumerate(DEMO_QUERIES, 1):
        console.rule(f"[cyan]Query {i} / {len(DEMO_QUERIES)}[/cyan]")
        console.print(f"[dim]{item['description']}[/dim]\n")

        try:
            result = orchestrator.run(item["query"])
            print_result(result, item["description"])
        except Exception as e:
            console.print(f"[red]Errore nella query {i}: {e}[/red]")
            console.print_exception()

    console.print(Panel.fit(
        "[bold green]✅  Demo completata![/bold green]\n"
        "Apri [bold cyan]http://localhost:5000[/bold cyan] per vedere tutte le run su MLflow.\n\n"
        "[dim]Troverai per ogni run:[/dim]\n"
        "[dim]  • Experiment: ReasonerHub[/dim]\n"
        "[dim]  • Params: agent_name, model, query[/dim]\n"
        "[dim]  • Metrics: confidence_score, latency_ms, reflection_rounds[/dim]\n"
        "[dim]  • Artifacts: reasoning_chain JSON[/dim]\n"
        "[dim]  • Tags: self_corrected, tool_used, tool_name[/dim]",
        border_style="green",
    ))


# ----------------------------------------------------------
# Modalità INTERATTIVA
# ----------------------------------------------------------

def run_interactive(orchestrator: RootOrchestrator):
    console.print("[bold yellow]▶  MODALITÀ INTERATTIVA[/bold yellow]")
    console.print("[dim]Scrivi una query e premi Invio. Digita 'exit' per uscire.[/dim]\n")
    console.print("[dim]Agenti disponibili: math · fact_checker · summarizer · code_analyzer · sentiment[/dim]\n")

    while True:
        try:
            query = console.input("[bold cyan]Tu → [/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit", "q"):
            break

        try:
            result = orchestrator.run(query)
            print_result(result)
        except Exception as e:
            console.print(f"[red]Errore: {e}[/red]")
            console.print_exception()

    console.print("\n[dim]Sessione terminata. Controlla MLflow per le run registrate.[/dim]")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    print_header()

    # Inizializza MLflow — crea experiment se non esiste
    console.print("[dim]Connessione a MLflow...[/dim]")
    init_mlflow()
    console.print("[green]✓[/green] MLflow connesso → [cyan]http://localhost:5000[/cyan]\n")

    # Istanzia orchestratore (e tutti gli agenti)
    console.print("[dim]Inizializzazione agenti...[/dim]")
    orchestrator = RootOrchestrator()
    console.print("[green]✓[/green] 5 agenti pronti\n")

    # Scelta modalità
    console.print("Scegli modalità:")
    console.print("  [bold]1[/bold] → Demo automatica (5 query, popola MLflow)")
    console.print("  [bold]2[/bold] → Interattiva (scrivi le tue query)")
    console.print()

    try:
        choice = console.input("[bold cyan]Scelta (1/2): [/bold cyan]").strip()
    except (KeyboardInterrupt, EOFError):
        choice = "1"

    console.print()

    if choice == "2":
        run_interactive(orchestrator)
    else:
        run_demo(orchestrator)


if __name__ == "__main__":
    main()