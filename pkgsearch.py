import argparse
import requests
from rich.console import Console
from rich.table import Table

USER_AGENT = "TerminalPkgSearch/1.0"

def search_packages(query: str, repo: str = None) -> dict:
    """Ищет проекты в Repology по имени пакета."""
    url = "https://repology.org/api/v1/projects/"
    params = {"search": query}
    
    
    if repo:
        params["inrepo"] = repo #filter project non repo
    
    try:
        response = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f" Ошибка при запросе к API: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(
        description="Поиск пакетов по дистрибутивам linux"
    )
    parser.add_argument("query", help="Имя пакета для поиска")
    parser.add_argument("--repo", help="Фильтр по репозиторию (arch, debian_12, fedora_40 и т.д.)", default=None)
    args = parser.parse_args()

    console = Console()
    console.print(f"[bold cyan]🔍 Ищем пакеты по запросу: '{args.query}'[/bold cyan]")
    if args.repo:
        console.print(f"[bold cyan] Фильтр по репозиторию: {args.repo}[/bold cyan]")

    data = search_packages(args.query, args.repo)
    
    if not data:
        console.print("[red]⚠️ Ничего не найдено.[/red]")
        return

    table = Table(title="Результаты поиска", show_header=True, header_style="bold magenta")
    table.add_column("Проект", style="cyan", no_wrap=True)
    table.add_column("Дистрибутив (Repo)", style="green")
    table.add_column("Версия", style="yellow")
    table.add_column("Статус", style="magenta")

    for project_name, packages in data.items():
        for pkg in packages:
            repo_name = pkg.get("repo", "N/A")
            
            
            if args.repo and repo_name != args.repo:  
                continue  
            
            version = pkg.get("version", "N/A")
            status = pkg.get("status", "unknown").replace("outdated", "устаревший").replace("newest", "актуальный")
            
            table.add_row(project_name, repo_name, version, status)

    console.print(table)
    console.print(f"\n[dim]Найдено проектов: {len(data)}[/dim]")

if __name__ == "__main__":
    main()
