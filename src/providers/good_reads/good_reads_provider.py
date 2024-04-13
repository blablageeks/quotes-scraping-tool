from abc import ABC
import random

from src.providers.quote_provider import QuoteProvider


class GoodReadsProvider(QuoteProvider, ABC):
    def __init__(self):
        self._base_url = "https://www.goodreads.com"
        self._quotes_type = {
            "popular": f"{self._base_url}/quotes",
            "recent": f"{self._base_url}/quotes/recently_added",
            "new": f"{self._base_url}/quotes/recently_created",
            "tag": f"{self._base_url}/quotes/tag/{{tag}}",
        }

    def load_html_page(self, page: int = 1, q_type: str = None, tag: str = None):
        if tag:
            url = self._quotes_type["tag"].format(tag=tag)
        elif q_type:
            url = self._quotes_type.get(q_type, "popular")
        else:
            url = self._quotes_type["popular"]

        return self.load_data(f"{url}?page={page}")

    def get_max_pagination_pages(self, q_type: str = None, tag: str = None):
        try:
            soup = self.load_html_page(q_type=q_type, tag=tag)
            if tag:
                pagination = soup.find("div", style="float: right;")
            elif q_type == "popular":
                pagination = soup.find("div", class_="u-textAlignRight")
            elif q_type in ["recent", "new"]:
                pagination = soup.find("div", style="text-align: right; width: 100%")
            else:
                pagination = soup.find("div", class_="u-textAlignRight")

            links = pagination.find_all("a") if pagination else []
            return max(int(link.text) for link in links if link.text.isdigit())
        except Exception as exec_info:
            print(str(exec_info))
            raise exec_info

    def get_quotes(self, page: int = 1, q_type: str = None, tag: str = None):
        q_type = random.choice(["popular", "recent", "new"])

        quotes_data = []

        soup = self.load_html_page(page, q_type, tag)

        quotes_list = [quote for quote in soup.find_all("div", class_="quoteDetails")]

        for quote_element in quotes_list:
            quote = self.reformat_quote(
                quote_element.find("div", class_="quoteText")
                .get_text(strip=True)
                .split("―")[0]
                .strip()
            )
            author = (
                quote_element.find("span", class_="authorOrTitle")
                .get_text(strip=True)
                .split(",")[0]
                .strip()
            )
            quotes_data.append({"quote": quote, "author": author})

        return quotes_data

    def get_random_quote(self, tag: str = None, count: int = 1):
        q_type = random.choice(["popular", "recent", "new"])
        try:
            max_pages = (
                self.get_max_pagination_pages(tag=tag)
                if tag
                else self.get_max_pagination_pages(q_type=q_type)
            )
            random_page = random.randint(1, max_pages)
            quotes = self.get_quotes(page=random_page, q_type=q_type, tag=tag)
            return random.sample(quotes, min(count, len(quotes)))
        except Exception as exec_info:
            return [{"quote": "Sic Parvis Magna", "author": "Sir Francis Drake"}]
