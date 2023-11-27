"""Console script for fab_news."""

from datetime import datetime

import click

from fab_news.fab_news import check_news


@click.command()
@click.option('--webhook', default="", help='Discord Webhook URL')
def main(webhook):
    """Main entrypoint."""
    click.echo(f'{datetime.now()} - Checking ...')
    check_news(webhook)


if __name__ == "__main__":
    main()  # pragma: no cover
