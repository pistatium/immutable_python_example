from typing import NamedTuple, Tuple

import requests
import zarame

QIITA_API_ENDPOINT = 'https://qiita.com/api/v2/items'


class User(NamedTuple):
    id: str


class Item(NamedTuple):
    title: str
    url: str
    user: User
    created_at: str


def fetch_qiita_items(page: int = 1) -> Tuple[Item, ...]:
    res = requests.get(QIITA_API_ENDPOINT, {'page': page})
    res.raise_for_status()
    return tuple(
        zarame.load(item, Item) for item in res.json()
    )


def sort_by_title_length(items: Tuple[Item]) -> Tuple[Item, ...]:
    return tuple(
        sorted(items, key=lambda i: len(i.title), reverse=True)
    )


def format_for_display(item: Item) -> str:
    return f'''{item.title}
    URL: {item.url}
    Author: {item.user.id}
    CreatedAt: {item.created_at}'''


def main():
    items = fetch_qiita_items()
    items = sort_by_title_length(items)
    for item in items[:5]:
        print(format_for_display(item))


if __name__ == '__main__':
    main()
