"""Main Fab News Module."""

import hashlib
import json
import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordEmbed, DiscordWebhook
from icecream import ic
from urlextract import URLExtract

extractor = URLExtract()


def get_data(url):
    """Return a soup object representing the page at `url`."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def compute_hash(data):
    """Return the hash for the supplied payload."""
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def get_old_hash(url):
    """Return the dict containing the cached hash and article payload for the given URL."""
    hash_file = ".cache/" + hashlib.md5(url.encode('utf-8')).hexdigest() + ".yml"
    if os.path.exists(hash_file):
        with open(hash_file, 'r') as file:
            old_hash = file.read()
        return json.loads(old_hash)
    else:
        return {"hash": "", "articles": {}}


def store_new_hash(url, new_hash, articles={}):
    """Store to cache (local disk) the supplied hash and article payload."""
    Path(".cache/").mkdir(parents=True, exist_ok=True)
    hash_file = ".cache/" + hashlib.md5(url.encode('utf-8')).hexdigest() + ".yml"
    context = {"hash": new_hash, "articles": articles}
    with open(hash_file, 'w') as file:
        file.write(json.dumps(context))


def get_article_dict(soup):
    """Return a dict of articles from the supplied `soup` output."""
    articles = soup.findAll(class_='listblock-item')

    articles_dict = {}

    for i in articles:
        title = i.h5.string
        url = i.a['href']
        image = ""
        if i.img:
            image = i.img['src']
        else:
            urls = extractor.find_urls(i.find_next("div", class_="item-card")['style'])
            image = urls[0]

        articles_dict[url] = {"title": title, "url": url, "image": image}

    return articles_dict


def articles(url="", webhook_url=""):
    """Check for Article update and post results if true."""
    old_hash = get_old_hash(url)
    new_data = get_data(url)
    new_hash = compute_hash(new_data)

    articles = get_article_dict(new_data)

    if old_hash["hash"] != "" and old_hash["hash"] != new_hash:
        old_set = set(old_hash["articles"].keys())
        new_set = set(articles.keys())

        new_article_keys = list(new_set - old_set)

        webhook = DiscordWebhook(url=webhook_url)
        for i in new_article_keys:
            embed = DiscordEmbed(title=articles[i]["title"], description=articles[i]["url"])
            embed.set_url(articles[i]["url"])
            embed.set_image(articles[i]["image"])
            webhook.add_embed(embed)
        webhook.execute()
        ic(old_hash)
        ic(new_hash)
        ic(articles)
        store_new_hash(url, new_hash, articles)


def living_legend(url="", webhook_url=""):
    """Check for Living Legend update and post result if true."""
    old_hash = get_old_hash(url)
    new_data = get_data(url)
    new_hash = compute_hash(new_data)

    if old_hash["hash"] == "" or old_hash["hash"] != new_hash:
        articles = new_data.findAll("caption")

        articles_dict = {}

        for i in articles:
            title = i.string
            url = url
            image = ""

            articles_dict[title] = {"title": title, "url": url, "image": image}

        if set(old_hash["articles"]) != set(articles_dict):
            webhook = DiscordWebhook(url=webhook_url)
            embed = DiscordEmbed(title="Living Legend Update!", description=url)
            embed.set_url(url)
            embed.set_image(
                "https://dhhim4ltzu1pj.cloudfront.net/media/images/logo_lss_stroke_white_780.width-10000.png"
            )
            webhook.add_embed(embed)
            webhook.execute()
            store_new_hash(url, new_hash, articles_dict)


def check_news(webhook=""):
    """Simple tool to check fabtcg.com for new articles and updates."""
    urls = ["https://fabtcg.com/resources/rules-and-policy-center/living-legend/"]
    articles_urls = ["https://fabtcg.com/retailer-news/"]
    for url in articles_urls:
        articles(url, webhook)
    for url in urls:
        living_legend(url, webhook)


if __name__ == '__main__':
    check_news()
