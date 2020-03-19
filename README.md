# steam-trades-helper
A faster way to find the best potential trades on steamtrades.com for a game you want.

The script takes a game that you want to obtain (or a list of sveral games) along with a list of games you have for trade and searches for trading pages with matching titles.

It then shows you the resulting trade links, along with the number of matching games in each.

## Usage
You can specify a game you want and the path to a text file with your games available for trade:

    $ python main.py --want "Example" --list "list.txt"

Or, instead, just specify the game you want, and the script will prompt you to paste your game list directly in the terminal.

The script might take a while to run if your lists are long enough - each game equals to a request to the SteamTrades website and I've set a fair delay between them as I don't want to load their servers too much. It should still be much faster than manually doing all of those searches, though!

## Dependencies
* Python 3.6 +
* BeautifulSoup
