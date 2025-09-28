from colorama import Fore, Back, Style
from colorama import just_fix_windows_console
just_fix_windows_console()
import random
import shutil
import json
from datetime import datetime
import locale
import os

# ♠♣♥♦
locale.setlocale(locale.LC_TIME, '')

table = {
    "player":{
        "hand":[],
        "points":100
    },
    "dealer":{
        "hand":[]
    },
    "game_over":False,
    "standing":False,
    "bet":0,
    "high_score":0,
    "prev_games":[
    ],
    "current_game":{
        "timestamp":1753269315,
        "result": False,
        "points_gained": 0 
    }
}


def load_data():
    if os.path.exists('blackjack_data.json'):
        with open('blackjack_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            table['player']['points'] = data.get("points", 0)
            table['high_score'] = data.get("high_score", 0)
            table['prev_games'] = data.get("prev_games", [])
    else:
        # Initialize default structure if file doesn't exist
        table['player']['points'] = 100
        table['high_score'] = 0
        table['prev_games'] = []

def save_data():
    with open('blackjack_data.json', 'w', encoding='utf-8') as f:
        data = {
            "points":table['player']['points'],
            "high_score":table['high_score'],
            "prev_games":table['prev_games']
        }
        json.dump(data, f, indent=4)

def Title():
    last_10_games = "\n".join(
    f"- {Fore.GREEN if game['result'] == "Win" else Fore.CYAN if game['result'] == "Push" else Fore.RED}Date: {datetime.fromtimestamp(game['timestamp']).strftime('%x %X')} || Result: {game['result']:<4} || Points gained: {game['points_gained']}{Fore.RESET}"
    for game in table['prev_games']
)

    print(rf"""

    {Fore.RED} /$$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$   /$$     {Fore.BLUE}           /$$$$$  /$$$$$$   /$$$$$$  /$$   /$$
    {Fore.RED}| $$__  $$| $$       /$$__  $$ /$$__  $$| $$  /$$/    {Fore.BLUE}           |__  $$ /$$__  $$ /$$__  $$| $$  /$$/
    {Fore.RED}| $$  \ $$| $$      | $$  \ $$| $$  \__/| $$ /$$/     {Fore.BLUE}              | $$| $$  \ $$| $$  \__/| $$ /$$/ 
    {Fore.RED}| $$$$$$$ | $$      | $$$$$$$$| $$      | $$$$$/      {Fore.BLUE}              | $$| $$$$$$$$| $$      | $$$$$/  
    {Fore.RED}| $$__  $$| $$      | $$__  $$| $$      | $$  $$      {Fore.BLUE}         /$$  | $$| $$__  $$| $$      | $$  $$  
    {Fore.RED}| $$  \ $$| $$      | $$  | $$| $$    $$| $$\  $$     {Fore.BLUE}        | $$  | $$| $$  | $$| $$    $$| $$\  $$ 
    {Fore.RED}| $$$$$$$/| $$$$$$$$| $$  | $$|  $$$$$$/| $$ \  $$    {Fore.BLUE}        |  $$$$$$/| $$  | $$|  $$$$$$/| $$ \  $$
    {Fore.RED}|_______/ |________/|__/  |__/ \______/ |__/  \__/    {Fore.BLUE}         \______/ |__/  |__/ \______/ |__/  \__/

{Fore.RESET}
==================================================================
Your goal is to get a total of 21 go over and your out

Game Rules:
- go over 21 you lose
- Aces count as 1 or 11 (depending on if it will set you over 21)
- Dealer stands on 17

Bets:
- win = bet value x2
- lose = lose bet value
- push = get original bet back
==================================================================
Your stats:
- high score: <NOT IMPLMENTED>
- Points: {table['player']['points']}
==================================================================
Last 10 games:
{last_10_games}
==================================================================
""")
class Suits:
    Club = f"{Fore.BLUE}♣{Fore.RESET}"
    Diamond = f"{Fore.RED}♦{Fore.RESET}"
    Spade = f"{Fore.BLUE}♠{Fore.RESET}"
    Heart = f"{Fore.RED}♥{Fore.RESET}"


suits = [Suits.Spade, Suits.Heart, Suits.Diamond, Suits.Club]
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

deck = [(suit, rank) for suit in suits for rank in ranks]
dealt_cards = set()

def MakeCard(suit, rank, hidden=False):
    if hidden:
        top    = f"{Fore.MAGENTA}╔╦╦╦╦╦╦╦╦╦╦╦╦╦╗{Fore.RESET}"
        line1  = f"{Fore.MAGENTA}╠╬╬╬╬╬╬╬╬╬╬╬╬╬╣{Fore.RESET}"
        line2  = f"{Fore.MAGENTA}╠╬╬╬╬╬╬╬╬╬╬╬╬╬╣{Fore.RESET}"
        line3  = f"{Fore.MAGENTA}╠╬╬╬╩╩╩╩╩╩╩╬╬╬╣{Fore.RESET}"
        line4  = f"{Fore.MAGENTA}╠╬╬╣ ????? ╠╬╬╣{Fore.RESET}"
        line5  = f"{Fore.MAGENTA}╠╬╬╬╦╦╦╦╦╦╦╬╬╬╣{Fore.RESET}"
        line6  = f"{Fore.MAGENTA}╠╬╬╬╬╬╬╬╬╬╬╬╬╬╣{Fore.RESET}"
        line7  = f"{Fore.MAGENTA}╠╬╬╬╬╬╬╬╬╬╬╬╬╬╣{Fore.RESET}"
        bottom = f"{Fore.MAGENTA}╚╩╩╩╩╩╩╩╩╩╩╩╩╩╝{Fore.RESET}"
        return [top, line1, line2, line3, line4, line5, line6, line7, bottom]
    top    = f"╔═════════════╗"
    line1  = f"║ {rank:<2}          ║"
    line2  = f"║ {suit}           ║"
    line3  = f"║             ║"
    line4  = f"║      {suit}      ║"
    line5  = f"║             ║"
    line6  = f"║           {suit} ║"
    line7  = f"║          {rank:>2} ║"
    bottom = f"╚═════════════╝"
    return [top, line1, line2, line3, line4, line5, line6, line7, bottom]

def MakeHand(cards, dealer=False):
    # Detect available console width
    try:
        cols = shutil.get_terminal_size().columns
    except:
        cols = 80  # fallback

    card_width = 15 + 2  # card plus 2-space gap
    cards_per_row = max(1, cols // card_width)

    for i in range(0, len(cards), cards_per_row):
        row = cards[i:i+cards_per_row]

        card_lines = []
        for idx, card in enumerate(row):
            # For dealer: hide the second card (index 1) in the first row only
            if dealer and i == 0 and idx == 1:
                card_lines.append(MakeCard(card[0], card[1], hidden=True))
            else:
                # Support cards with optional hidden flag
                if len(card) == 3:
                    card_lines.append(MakeCard(*card))
                else:
                    card_lines.append(MakeCard(card[0], card[1]))

        for line_index in range(9):  # each card is 9 lines tall
            print('  '.join(card[line_index] for card in card_lines))

def deal_card():
    remaining = [card for card in deck if card not in dealt_cards]
    if not remaining:
        raise ValueError("No cards left in the deck")
    card = random.choice(remaining)
    dealt_cards.add(card)
    return card

def CardTotal(cards, dealer=False):
    total = 0
    ace_count = 0
    second = False
    for suit, rank in cards:
        if second and dealer:
            continue
        second = True
        if rank == 'A':
            ace_count += 1
            total += 1
        elif rank in ['J', 'Q', 'K']:
            total += 10
        else:
            total += int(rank) 

    for _ in range(ace_count):
        if total + 10 <= 21:
            total += 10

    return total

if __name__ == "__main__":
    load_data()
    Title()

    input("Press Enter to play...")
    
    while True:
        while True: # Game Loop
            if len(table['player']['hand']) == 0:
                table['current_game'] = {
                    "timestamp":datetime.now().timestamp(),
                    "result": "N/A",
                    "points_gained": 0 
                }
                print("============================================\n\n\n")
                while True:
                    bet = input(f'How much would you like to bet? (Max: {table['player']['points']}): ')
                    bet = int(bet)
                    if bet < 0:
                        print("Must be a positve number")
                        continue
                    elif bet > table['player']['points']:
                        print("Not Enough Points")
                        continue
                    else:
                        print(f"Placeing a bet for {bet} Points")
                        table['bet'] = bet
                        table['player']['points'] -= bet
                        print("============================================\n\n\n")
                        break

                table['standing'] = False
                table['player']['hand'].append(deal_card())
                table['player']['hand'].append(deal_card())

                table['dealer']['hand'].append(deal_card())
                table['dealer']['hand'].append(deal_card())
                #Player BlackJack
                if CardTotal(table['player']['hand']) == 21 and CardTotal(table['dealer']['hand']) != 21:
                    print("Dealers cards:\n")
                    MakeHand(table['dealer']['hand'])
                    print(f"Dealer has: {CardTotal(table['dealer']['hand'])}")
                    
                    print("="*shutil.get_terminal_size().columns)

                    print("Your cards:\n")
                    MakeHand(table['player']['hand'])
                    print(f"You have: {CardTotal(table['player']['hand'])}")
                    print(rf"""
    {Fore.YELLOW}
     /$$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$   /$$          /$$$$$  /$$$$$$   /$$$$$$  /$$   /$$
    | $$__  $$| $$       /$$__  $$ /$$__  $$| $$  /$$/         |__  $$ /$$__  $$ /$$__  $$| $$  /$$/
    | $$  \ $$| $$      | $$  \ $$| $$  \__/| $$ /$$/             | $$| $$  \ $$| $$  \__/| $$ /$$/ 
    | $$$$$$$ | $$      | $$$$$$$$| $$      | $$$$$/              | $$| $$$$$$$$| $$      | $$$$$/  
    | $$__  $$| $$      | $$__  $$| $$      | $$  $$         /$$  | $$| $$__  $$| $$      | $$  $$  
    | $$  \ $$| $$      | $$  | $$| $$    $$| $$\  $$       | $$  | $$| $$  | $$| $$    $$| $$\  $$ 
    | $$$$$$$/| $$$$$$$$| $$  | $$|  $$$$$$/| $$ \  $$      |  $$$$$$/| $$  | $$|  $$$$$$/| $$ \  $$
    |_______/ |________/|__/  |__/ \______/ |__/  \__/       \______/ |__/  |__/ \______/ |__/  \__/
    {Fore.GREEN}
     /$$     /$$ /$$$$$$  /$$   /$$       /$$      /$$ /$$$$$$ /$$   /$$
    |  $$   /$$//$$__  $$| $$  | $$      | $$  /$ | $$|_  $$_/| $$$ | $$
     \  $$ /$$/| $$  \ $$| $$  | $$      | $$ /$$$| $$  | $$  | $$$$| $$
      \  $$$$/ | $$  | $$| $$  | $$      | $$/$$ $$ $$  | $$  | $$ $$ $$
       \  $$/  | $$  | $$| $$  | $$      | $$$$_  $$$$  | $$  | $$  $$$$
        | $$   | $$  | $$| $$  | $$      | $$$/ \  $$$  | $$  | $$\  $$$
        | $$   |  $$$$$$/|  $$$$$$/      | $$/   \  $$ /$$$$$$| $$ \  $$
        |__/    \______/  \______/       |__/     \__/|______/|__/  \__/
    {Fore.RESET}
    """)
                    table['player']['points'] += bet*2
                    table['current_game']['result'] = 'Win'
                    table['current_game']['points_gained'] = bet*2
                    break
                
                #Dealer BlackJack
                if CardTotal(table['player']['hand']) != 21 and CardTotal(table['dealer']['hand']) == 21:
                    print("Dealers cards:\n")
                    MakeHand(table['dealer']['hand'])
                    print(f"Dealer has: {CardTotal(table['dealer']['hand'])}")
                    
                    print("="*shutil.get_terminal_size().columns)

                    print("Your cards:\n")
                    MakeHand(table['player']['hand'])
                    print(f"You have: {CardTotal(table['player']['hand'])}")
                    print(rf"""
    {Fore.YELLOW}
     /$$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$   /$$          /$$$$$  /$$$$$$   /$$$$$$  /$$   /$$
    | $$__  $$| $$       /$$__  $$ /$$__  $$| $$  /$$/         |__  $$ /$$__  $$ /$$__  $$| $$  /$$/
    | $$  \ $$| $$      | $$  \ $$| $$  \__/| $$ /$$/             | $$| $$  \ $$| $$  \__/| $$ /$$/ 
    | $$$$$$$ | $$      | $$$$$$$$| $$      | $$$$$/              | $$| $$$$$$$$| $$      | $$$$$/  
    | $$__  $$| $$      | $$__  $$| $$      | $$  $$         /$$  | $$| $$__  $$| $$      | $$  $$  
    | $$  \ $$| $$      | $$  | $$| $$    $$| $$\  $$       | $$  | $$| $$  | $$| $$    $$| $$\  $$ 
    | $$$$$$$/| $$$$$$$$| $$  | $$|  $$$$$$/| $$ \  $$      |  $$$$$$/| $$  | $$|  $$$$$$/| $$ \  $$
    |_______/ |________/|__/  |__/ \______/ |__/  \__/       \______/ |__/  |__/ \______/ |__/  \__/
    {Fore.RED}
     /$$     /$$ /$$$$$$  /$$   /$$       /$$        /$$$$$$   /$$$$$$  /$$$$$$$$
    |  $$   /$$//$$__  $$| $$  | $$      | $$       /$$__  $$ /$$__  $$| $$_____/
     \  $$ /$$/| $$  \ $$| $$  | $$      | $$      | $$  \ $$| $$  \__/| $$      
      \  $$$$/ | $$  | $$| $$  | $$      | $$      | $$  | $$|  $$$$$$ | $$$$$   
       \  $$/  | $$  | $$| $$  | $$      | $$      | $$  | $$ \____  $$| $$__/   
        | $$   | $$  | $$| $$  | $$      | $$      | $$  | $$ /$$  \ $$| $$      
        | $$   |  $$$$$$/|  $$$$$$/      | $$$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$$
        |__/    \______/  \______/       |________/ \______/  \______/ |________/
    {Fore.RESET}
    """)
                    table['current_game']['result'] = 'Lose'
                    table['current_game']['points_gained'] = -bet
                    break
                
                #Push BlackJack
                if CardTotal(table['player']['hand']) == 21 and CardTotal(table['dealer']['hand']) == 21:
                    print("Dealers cards:\n")
                    MakeHand(table['dealer']['hand'])
                    print(f"Dealer has: {CardTotal(table['dealer']['hand'])}")
                    
                    print("="*shutil.get_terminal_size().columns)

                    print("Your cards:\n")
                    MakeHand(table['player']['hand'])
                    print(f"You have: {CardTotal(table['player']['hand'])}")
                    print(rf"""
    {Fore.YELLOW}
     /$$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$   /$$          /$$$$$  /$$$$$$   /$$$$$$  /$$   /$$
    | $$__  $$| $$       /$$__  $$ /$$__  $$| $$  /$$/         |__  $$ /$$__  $$ /$$__  $$| $$  /$$/
    | $$  \ $$| $$      | $$  \ $$| $$  \__/| $$ /$$/             | $$| $$  \ $$| $$  \__/| $$ /$$/ 
    | $$$$$$$ | $$      | $$$$$$$$| $$      | $$$$$/              | $$| $$$$$$$$| $$      | $$$$$/  
    | $$__  $$| $$      | $$__  $$| $$      | $$  $$         /$$  | $$| $$__  $$| $$      | $$  $$  
    | $$  \ $$| $$      | $$  | $$| $$    $$| $$\  $$       | $$  | $$| $$  | $$| $$    $$| $$\  $$ 
    | $$$$$$$/| $$$$$$$$| $$  | $$|  $$$$$$/| $$ \  $$      |  $$$$$$/| $$  | $$|  $$$$$$/| $$ \  $$
    |_______/ |________/|__/  |__/ \______/ |__/  \__/       \______/ |__/  |__/ \______/ |__/  \__/
    {Fore.CYAN}
     /$$$$$$$  /$$   /$$  /$$$$$$  /$$   /$$
    | $$__  $$| $$  | $$ /$$__  $$| $$  | $$
    | $$  \ $$| $$  | $$| $$  \__/| $$  | $$
    | $$$$$$$/| $$  | $$|  $$$$$$ | $$$$$$$$
    | $$____/ | $$  | $$ \____  $$| $$__  $$
    | $$      | $$  | $$ /$$  \ $$| $$  | $$
    | $$      |  $$$$$$/|  $$$$$$/| $$  | $$
    |__/       \______/  \______/ |__/  |__/
    {Fore.RESET}
    """)
                    table['player']['points'] += bet
                    table['current_game']['result'] = 'Push'
                    table['current_game']['points_gained'] = 0
                    break
            print("Dealers cards:\n")
            MakeHand(table['dealer']['hand'], dealer=True)
            print(f"Dealer has: {CardTotal(table['dealer']['hand'])}")
            
            print("="*shutil.get_terminal_size().columns)

            print("Your cards:\n")
            MakeHand(table['player']['hand'])
            print(f"You have: {CardTotal(table['player']['hand'])}")

            #action loop
            while True:
                action = input("What will you do?:\n- [H] Hit \n- [S] Stand\n>>> ")
                if action.lower() in ["hit", "h"]:
                    table['player']['hand'].append(deal_card())
                    break
                elif action.lower() in ["stand", "s"]:
                    table['standing'] = True
                    while CardTotal(table['dealer']['hand']) < 17:
                        table['dealer']['hand'].append(deal_card())
                    break
                else:
                    print(f"Only enter one of the following: {['h','hit','s','stand']}\n\n\n")
                    break
            
            #player bust
            if CardTotal(table['player']['hand']) > 21:
                print(rf"""
    {Fore.CYAN}   
     /$$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$$$
    | $$__  $$| $$  | $$ /$$__  $$|__  $$__/
    | $$  \ $$| $$  | $$| $$  \__/   | $$   
    | $$$$$$$ | $$  | $$|  $$$$$$    | $$   
    | $$__  $$| $$  | $$ \____  $$   | $$   
    | $$  \ $$| $$  | $$ /$$  \ $$   | $$   
    | $$$$$$$/|  $$$$$$/|  $$$$$$/   | $$   
    |_______/  \______/  \______/    |__/  
    {Fore.RED}
     /$$     /$$ /$$$$$$  /$$   /$$       /$$        /$$$$$$   /$$$$$$  /$$$$$$$$
    |  $$   /$$//$$__  $$| $$  | $$      | $$       /$$__  $$ /$$__  $$| $$_____/
     \  $$ /$$/| $$  \ $$| $$  | $$      | $$      | $$  \ $$| $$  \__/| $$      
      \  $$$$/ | $$  | $$| $$  | $$      | $$      | $$  | $$|  $$$$$$ | $$$$$   
       \  $$/  | $$  | $$| $$  | $$      | $$      | $$  | $$ \____  $$| $$__/   
        | $$   | $$  | $$| $$  | $$      | $$      | $$  | $$ /$$  \ $$| $$      
        | $$   |  $$$$$$/|  $$$$$$/      | $$$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$$
        |__/    \______/  \______/       |________/ \______/  \______/ |________/
    {Fore.RESET}
    """)
                table['current_game']['result'] = 'Lose'
                table['current_game']['points_gained'] = -bet
                print("Dealers cards:\n")
                MakeHand(table['dealer']['hand'])
                print(f"Dealer had: {CardTotal(table['dealer']['hand'])}")
                
                print("="*shutil.get_terminal_size().columns)

                print("Your cards:\n")
                MakeHand(table['player']['hand'])
                print(f"You have: {CardTotal(table['player']['hand'])}")
                break
            
            #dealer bust
            if CardTotal(table['dealer']['hand']) > 21:
                print(rf"""
    {Fore.CYAN}
     /$$$$$$$  /$$$$$$$$  /$$$$$$  /$$       /$$$$$$$$ /$$$$$$$        /$$$$$$$  /$$   /$$  /$$$$$$  /$$$$$$$$
    | $$__  $$| $$_____/ /$$__  $$| $$      | $$_____/| $$__  $$      | $$__  $$| $$  | $$ /$$__  $$|__  $$__/
    | $$  \ $$| $$      | $$  \ $$| $$      | $$      | $$  \ $$      | $$  \ $$| $$  | $$| $$  \__/   | $$   
    | $$  | $$| $$$$$   | $$$$$$$$| $$      | $$$$$   | $$$$$$$/      | $$$$$$$ | $$  | $$|  $$$$$$    | $$   
    | $$  | $$| $$__/   | $$__  $$| $$      | $$__/   | $$__  $$      | $$__  $$| $$  | $$ \____  $$   | $$   
    | $$  | $$| $$      | $$  | $$| $$      | $$      | $$  \ $$      | $$  \ $$| $$  | $$ /$$  \ $$   | $$   
    | $$$$$$$/| $$$$$$$$| $$  | $$| $$$$$$$$| $$$$$$$$| $$  | $$      | $$$$$$$/|  $$$$$$/|  $$$$$$/   | $$   
    |_______/ |________/|__/  |__/|________/|________/|__/  |__/      |_______/  \______/  \______/    |__/   
    {Fore.GREEN}
     /$$     /$$ /$$$$$$  /$$   /$$       /$$      /$$ /$$$$$$ /$$   /$$
    |  $$   /$$//$$__  $$| $$  | $$      | $$  /$ | $$|_  $$_/| $$$ | $$
     \  $$ /$$/| $$  \ $$| $$  | $$      | $$ /$$$| $$  | $$  | $$$$| $$
      \  $$$$/ | $$  | $$| $$  | $$      | $$/$$ $$ $$  | $$  | $$ $$ $$
       \  $$/  | $$  | $$| $$  | $$      | $$$$_  $$$$  | $$  | $$  $$$$
        | $$   | $$  | $$| $$  | $$      | $$$/ \  $$$  | $$  | $$\  $$$
        | $$   |  $$$$$$/|  $$$$$$/      | $$/   \  $$ /$$$$$$| $$ \  $$
        |__/    \______/  \______/       |__/     \__/|______/|__/  \__/
    {Fore.RESET}
    """)
                table['current_game']['result'] = 'Win'
                table['current_game']['points_gained'] = bet*2
                print("Dealers cards:\n")
                MakeHand(table['dealer']['hand'])
                print(f"Dealer has: {CardTotal(table['dealer']['hand'])}")
                
                print("="*shutil.get_terminal_size().columns)

                print("Your cards:\n")
                MakeHand(table['player']['hand'])
                print(f"You had: {CardTotal(table['player']['hand'])}")
                table['player']['points'] += bet*2
                break
            
            #if standing
            if table['standing']:
                print("Dealers cards:\n")
                MakeHand(table['dealer']['hand'])
                print(f"Dealer has: {CardTotal(table['dealer']['hand'])}")
                
                print("="*shutil.get_terminal_size().columns)

                print("Your cards:\n")
                MakeHand(table['player']['hand'])
                print(f"You have: {CardTotal(table['player']['hand'])}")

                #WIN
                if CardTotal(table['player']['hand']) > CardTotal(table['dealer']['hand']):
                    print(f"""
    {Fore.GREEN}
     /$$     /$$ /$$$$$$  /$$   /$$       /$$      /$$ /$$$$$$ /$$   /$$
    |  $$   /$$//$$__  $$| $$  | $$      | $$  /$ | $$|_  $$_/| $$$ | $$
     \  $$ /$$/| $$  \ $$| $$  | $$      | $$ /$$$| $$  | $$  | $$$$| $$
      \  $$$$/ | $$  | $$| $$  | $$      | $$/$$ $$ $$  | $$  | $$ $$ $$
       \  $$/  | $$  | $$| $$  | $$      | $$$$_  $$$$  | $$  | $$  $$$$
        | $$   | $$  | $$| $$  | $$      | $$$/ \  $$$  | $$  | $$\  $$$
        | $$   |  $$$$$$/|  $$$$$$/      | $$/   \  $$ /$$$$$$| $$ \  $$
        |__/    \______/  \______/       |__/     \__/|______/|__/  \__/
    {Fore.RESET}
        """)
                    table['current_game']['result'] = 'Win'
                    table['current_game']['points_gained'] = bet*2
                    table['player']['points'] += bet*2
                    break
                
                #LOSE
                if CardTotal(table['player']['hand']) < CardTotal(table['dealer']['hand']):
                    print(f"""
    {Fore.RED}
     /$$     /$$ /$$$$$$  /$$   /$$       /$$        /$$$$$$   /$$$$$$  /$$$$$$$$
    |  $$   /$$//$$__  $$| $$  | $$      | $$       /$$__  $$ /$$__  $$| $$_____/
     \  $$ /$$/| $$  \ $$| $$  | $$      | $$      | $$  \ $$| $$  \__/| $$      
      \  $$$$/ | $$  | $$| $$  | $$      | $$      | $$  | $$|  $$$$$$ | $$$$$   
       \  $$/  | $$  | $$| $$  | $$      | $$      | $$  | $$ \____  $$| $$__/   
        | $$   | $$  | $$| $$  | $$      | $$      | $$  | $$ /$$  \ $$| $$      
        | $$   |  $$$$$$/|  $$$$$$/      | $$$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$$
        |__/    \______/  \______/       |________/ \______/  \______/ |________/
    {Fore.RESET}
        """)
                    table['current_game']['result'] = 'Lose'
                    table['current_game']['points_gained'] = -bet
                    break
                
                #PUSH
                if CardTotal(table['player']['hand']) == CardTotal(table['dealer']['hand']):
                    print(f"""
    {Fore.CYAN}
     /$$$$$$$  /$$   /$$  /$$$$$$  /$$   /$$
    | $$__  $$| $$  | $$ /$$__  $$| $$  | $$
    | $$  \ $$| $$  | $$| $$  \__/| $$  | $$
    | $$$$$$$/| $$  | $$|  $$$$$$ | $$$$$$$$
    | $$____/ | $$  | $$ \____  $$| $$__  $$
    | $$      | $$  | $$ /$$  \ $$| $$  | $$
    | $$      |  $$$$$$/|  $$$$$$/| $$  | $$
    |__/       \______/  \______/ |__/  |__/
    {Fore.RESET}
        """)
                    table['current_game']['result'] = 'Push'
                    table['current_game']['points_gained'] = 0
                    table['player']['points'] += bet
                    break
        table['prev_games'].append(table['current_game'].copy())
        while True: # Play again Prompt
            if table['player']['points'] <= 0:
                while True:
                    reload_responce = input("You have 0 points\nReload?\n>>> [y/n]")
                    if reload_responce.lower() in ['y','yes','n','no']:
                        table['player']['points'] = 100
                        break
                    else:
                        print(f"Only enter one of the following: {['y','yes','n','no']}\n\n\n")
            if table['player']['points'] > table['high_score']:
                table['high_score'] = table['player']['points']
            save_data()
            responce = input('Play Again? [y/n]: ')
            if responce.lower() in ['y','yes','n','no']:
                if responce in ['n','no']:
                    table['game_over'] = True
                else:
                    table['dealer']['hand'] = []
                    table['player']['hand'] = []
                    table['game_over'] = False
                    table['standing'] = False
                    table['bet'] = 0
                    print("\n"*8)
                    Title()
                    input("Press Enter to play...")
                break
            else:
                print(f"Only enter one of the following: {['y','yes','n','no']}\n\n\n")
        if table['game_over']:
            break
    print("Exiting...")
    exit()