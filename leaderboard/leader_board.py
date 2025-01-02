from rich.table import Table
from rich.console import Console
from colorama import Fore, Style
from db.models.user_answers import UserAnswer
def display_leaderboard():
    """
    display a leaderboard that holds multiple users 
    """
    console = Console()
    print(Fore.YELLOW + "\n=== Trivia Leaderboard ===" + Style.RESET_ALL)

    scores = UserAnswer.get_user_scores() 
    if not scores:
        print(Fore.RED + "No scores available. Play the game to add scores!" + Style.RESET_ALL)
        return
    #sort users by scores in ascending order
    sorted_scores = sorted(scores, key=lambda x:x['score'], reverse=True)

    #create a table for leaderboard
    table = Table(title="Trivia leaderboard", style="cyan")
    table.add_column("Rank",justify="center",style="bold magenta")
    table.add_column("username", style="bold green")
    table.add_column("Score",justify="center",style="bold yellow")

    for rank, user in enumerate(sorted_scores,start=1):
        table.add_row(str(rank), user['username'], str(user['score']))
    console.print(table)
