#!/usr/bin/env python3

import json
import base64
import asyncio
import aiohttp
import urllib.parse as up
import argparse
import logging


async def main():
    url, verbose = args()
    theme_url = ThemeURL(url)
    logging.basicConfig(level=logging.INFO if verbose else logging.CRITICAL)
    theme_transformed = await collect_transform(theme_url)
    print(json.dumps(theme_transformed))


class ThemeURL():
    def __init__(self, url: str):
        theme_url = up.urlsplit(url)
        self.path = theme_url.path if theme_url.path[-1] == '/' else theme_url.path+'/'
        theme_url = theme_url._replace(path='')
        self.base = up.urlunsplit(theme_url)
    json = "theme.json"


def args():
    parser = argparse.ArgumentParser(
        description='Caches image files as Base64 encoded strings in structurizr theme files')
    parser.add_argument("URL",
                        help="Full URL for the theme base path.\ne.g. https://static.structurizr.com/themes/microsoft-azure-2023.01.24/")
    parser.add_argument("-v", "--verbose", help="Info on icon access",
                        action="store_true", default=False)
    args = parser.parse_args()
    return args.URL, args.verbose


async def collect_transform(theme_url: ThemeURL) -> set:
    async with aiohttp.ClientSession(theme_url.base) as session:
        async with session.get(theme_url.path + theme_url.json) as resp:
            theme = await resp.json()
        async with asyncio.TaskGroup() as tg:
            for elem in theme['elements']:
                tg.create_task(replace_icon(session, theme_url, elem))
    return theme


async def replace_icon(session, theme_url, elem):
    logging.info(f"Attaining icon {elem['icon']}")
    async with session.get(theme_url.path + elem['icon']) as resp:
        icon = await resp.read()
    logging.info(f"Attained icon {elem['icon']}")
    elem['icon'] = base64.b64encode(icon).decode('ascii')

asyncio.run(main())
