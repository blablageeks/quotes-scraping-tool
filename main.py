import argparse

from providers.good_reads.good_reads_provider import GoodReadsProvider


def main():
    parser = argparse.ArgumentParser("Quotes scraping Tool CLI")
    parser.add_argument(
        "--tag",
        type=str,
        help="Tag",
        choices=["love", "religion", "inspiration", "god", "success"],
        default=None,
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        choices=range(1, 11),
        help="How many quotes to scrape",
    )

    args = parser.parse_args()

    provider = GoodReadsProvider()

    quotes = (
        provider.get_random_quote(tag=args.tag, count=args.count)
        if args.tag
        else provider.get_random_quote(count=args.count)
    )

    for q in quotes:
        print(f"{q['quote']} - {q['author']}\n")


if __name__ == "__main__":
    main()
