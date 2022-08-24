import requests
import re


def strip_tags(text: str) -> str:
    return re.sub('<[^<]+?>', '', text)


def extract_content(url: str) -> str:
    print(f"Fetching {url}...")
    page_content = requests.get(url).text

    headers, rest = page_content.split("<h3>")
    text, footers = rest.split("<br clear=all>")
    text = strip_tags(text)

    return text


if __name__ == '__main__':
    text = ""

    for i in range(1, 51):
        if i < 10:
            possible_extra_zero = "0"
        else:
            possible_extra_zero = ""

        url = f"http://runeberg.org/kalevala/{possible_extra_zero}{i}.html"

        text += extract_content(url)

        print(f"Saving chapter {i}...")

    with open(f'data/kalevala.txt', 'w') as f:
        f.write(text)




