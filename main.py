#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
import time
import sys

main_url = "https://www.steamtrades.com"
headers = {"User-Agent": "steam-trades-helper (https://github.com/jduar/steam-trades-helper)"}  # request header
sleep_time = 1  # sleep time between requests


def get_trade_links(game1=None, game2=None):
    """Returns an array of trade page links.

    :type game1: str
    :type game2: str
    """

    if game1 is not None and game2 is not None:
        url = f"https://www.steamtrades.com/trades/search?have={game1}&want={game2}"

    elif game1 is None and game2 is not None:
        url = f"https://www.steamtrades.com/trades/search?want={game2}"

    else:
        url = f"https://www.steamtrades.com/trades/search?have={game1}"

    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")

    rows = soup.find_all("div", class_="row_outer_wrap")

    links = []

    for row in rows:
        inner_row_div = row.find("div", class_="row_inner_wrap")
        inner_div = inner_row_div.find("div", class_="column_flex")
        inner_h3 = inner_div.find("h3")
        # Filtering closed trade pages
        if not inner_h3.find("i", class_="red fa fa-lock"):
            link = main_url + inner_h3.find("a")["href"]
            links.append(link)

    return links


def evaluate_trades(links, usr_game_list):
    """Reads an array of trade page links and determines the best trades.

    :type links: [str]
    """
    for link in links:
        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        trd_game_list = parse_trades(soup)

        trader = soup.find("a", class_="author_name").get_text()
        matches = compare_string_arrays(usr_game_list, trd_game_list)

        print(f"{matches} matches - {trader} - {link}")

        time.sleep(sleep_time)


def parse_trades(trade_soup):
    """Parses a trade's BeautifulSoup object.

    :type trade_soup: BeautifulSoup object
    """
    # Getting the list of games in the trader's "Want" section
    want_text = trade_soup.find("div", class_="want markdown")
    game_array = want_text.get_text().split("\n")
    return game_array


def compare_string_arrays(arr1, arr2):
    """Counts the number of ocurrences of items from arr1 in arr2.

    :type arr1: [str]
    :type arr2: [str]
    """
    matches = 0
    for game in arr1:
        if game in arr2:
            matches += 1
    return matches


def find_trades(games_list, wanted_game):
    """Finds trades between the wanted game and the provided list and
    returns an array of available trade links.

    :type games_list: [str]
    :type wanted_game: str
    """
    all_trade_links = []
    for game in games_list:
        print(game)
        trade_links = get_trade_links(game, wanted_game)
        for link in trade_links:
            if link not in all_trade_links:
                all_trade_links.append(link)
        time.sleep(sleep_time)
    return all_trade_links


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--have", type=str,
                        help="""name of a game you have. E.g.:
                        --have \"example\"""")
    parser.add_argument("--want", type=str,
                        help="""name of a game you want. E.g.:
                        --want \"example\"""")
    parser.add_argument("--list", type=str,
                        help="path to your games list")
    args = parser.parse_args()

    games_text = []

    if args.list is not None:
        with open(args.list, "r") as file:
            print(" > Reading your games list.")
            games_text = file.readlines()

    else:
        print(" > Paste your games list and press Ctrl+D.")
        # stdin is required to accept multiline lists.
        games_text = sys.stdin.readlines()

    if len(games_text) > 0:
        print(" > Finding trades...")

        games_list = [game.strip("\n") for game in games_text]

        link_array = find_trades(games_list, args.want)

        evaluate_trades(link_array, games_list)

    else:
        print(" > You haven't provided any games list.")
        exit()


if __name__ == "__main__":
    main()


# https://www.steamtrades.com/trades/search?have=123&want=456
# Game I have - 123; game I want - 456
