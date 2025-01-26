import json
import sys


if __name__ == "__main__":
    path = sys.argv[1]
    week = sys.argv[2]

    with open(f"{path}", encoding="utf-8") as fp:
        chapters = json.load(fp)
        result = [chapter for chapter in chapters if chapter.get("week") == int(week)]

    titles = [
        f"{chapter.get('object_index')}. {chapter.get('title')}" for chapter in result
    ]

    print("\n".join(titles))
