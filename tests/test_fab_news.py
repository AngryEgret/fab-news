#!/usr/bin/env python
"""Tests for `fab_news` package."""

import pytest

from fab_news import fab_news


@pytest.fixture
def article_response():
    """Article Response Fixture."""
    import requests

    return requests.get('https://fabtcg.com/articles/')


@pytest.fixture
def ll_response():
    """Article Response Fixture."""
    import requests

    return requests.get('https://fabtcg.com/resources/rules-and-policy-center/living-legend/')


def test_get_data(article_response):
    """Test the get_data() method."""
    result = fab_news.get_data('https://fabtcg.com/resources/rules-and-policy-center/living-legend/')
    assert result.title.string == "Living Legend"
    del result


def test_compute_hash():
    """Test the compute_hash() method."""
    result = fab_news.compute_hash("test_string")
    assert result == '3474851a3410906697ec77337df7aae4'


def test_get_old_hash():
    """Test the get_old_hash() method."""
    result = fab_news.get_old_hash("https://fabtcg.com/articles/")

    assert type(result) is dict
    assert result["hash"] == "aa8b8ec7378de3e6d267710d1013a114"

    result = fab_news.get_old_hash("")
    assert type(result) is dict
    assert result["hash"] == ""


# def test_store_new_hash():
#     """Test the store_new_hash() method."""
#     url = "https://fabtcg.com/false/"
#     new_hash = "1234"
#     articles = {'1': 'a'}

#     mocker.patch('file.write')

#     fab_news.store_new_hash(url, new_hash, articles)
#     file.write.assert_called_once_with(
#         ".cache/37d1ae0d56f764c259e36ad1884ebcb6.yml", {"hash": "1234", "articles": {'1': 'a'}}
#     )


# def test_get_article_dict(soup):
#     """Return a dict of articles from the supplied `soup` output."""
#     articles = soup.findAll(class_='listblock-item')

#     articles_dict = {}

#     for i in articles:
#         title = i.h5.string
#         url = i.a['href']
#         image = ""
#         if i.img:
#             image = i.img['src']
#         else:
#             urls = extractor.find_urls(i.find_next("div", class_="item-card")['style'])
#             image = urls[0]

#         articles_dict[url] = {"title": title, "url": url, "image": image}

#     return articles_dict


# def test_articles(url="", webhook_url=""):
#     """Check for Article update and post results if true."""
#     old_hash = get_old_hash(url)
#     new_data = get_data(url)
#     new_hash = compute_hash(new_data)

#     articles = get_article_dict(new_data)

#     if old_hash["hash"] != "" and old_hash["hash"] != new_hash:
#         old_set = set(old_hash["articles"].keys())
#         new_set = set(articles.keys())

#         new_article_keys = list(new_set - old_set)

#         webhook = DiscordWebhook(url=webhook_url)
#         for i in new_article_keys:
#             embed = DiscordEmbed(title=articles[i]["title"], description=articles[i]["url"])
#             embed.set_url(articles[i]["url"])
#             embed.set_image(articles[i]["image"])
#             webhook.add_embed(embed)
#         webhook.execute()
#         ic(old_hash)
#         ic(new_hash)
#         ic(articles)
#         store_new_hash(url, new_hash, articles)


# def test_living_legend(url="", webhook_url=""):
#     """Check for Living Legend update and post result if true."""
#     old_hash = get_old_hash(url)
#     new_data = get_data(url)
#     new_hash = compute_hash(new_data)

#     if old_hash["hash"] == "" or old_hash["hash"] != new_hash:
#         webhook = DiscordWebhook(url=webhook_url)
#         embed = DiscordEmbed(title="Living Legend Update!", description=url)
#         embed.set_url(url)
#         embed.set_image("https://dhhim4ltzu1pj.cloudfront.net/media/images/logo_lss_stroke_white_780.width-10000.png")
#         webhook.add_embed(embed)
#         webhook.execute()
#         ic(old_hash)
#         ic(new_hash)
#         store_new_hash(url, new_hash)


# def test_check_news(webhook=""):
#     """Simple tool to check fabtcg.com for new articles and updates."""
#     urls = ["https://fabtcg.com/resources/rules-and-policy-center/living-legend/"]
#     articles_urls = ["https://fabtcg.com/articles/", "https://fabtcg.com/retailer-news/"]
#     for url in articles_urls:
#         articles(url, webhook)
#     for url in urls:
#         living_legend(url, webhook)
