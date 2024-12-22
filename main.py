import argparse
from dataclasses import dataclass

import requests


@dataclass
class RandomQuote:
    """Class for storing random quotes"""

    house: str
    character: str
    quote: str

    def say(self) -> str:
        return f"{self.character} of {self.house}: '{self.quote}'"


def get_quote(endpoint: str) -> RandomQuote | None:
    base_url = "https://api.gameofthronesquotes.xyz/v1"

    try:
        response = requests.get(base_url + endpoint)
        response.raise_for_status()

        content = response.json()
        return RandomQuote(
            house=content["character"]["house"]["name"],
            character=content["character"]["name"],
            quote=content["sentence"],
        )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def main(endpoint: str) -> None:
    quote = get_quote(endpoint)
    if quote:
        print(quote.say())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint", default="/random", nargs="?", help="The endpoint of interest")
    args = parser.parse_args()

    main(args.endpoint)
