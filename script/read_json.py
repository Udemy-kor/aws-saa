import json
import sys
import re


def convert_special_characters(text: str) -> str:
    """
    space       ➡️ -
    +           ➡️ -
    ,           ➡️ -
    &           ➡️ -
    (           ➡️ -
    )           ➡️ -
    !           ➡️ -
    ?           ➡️ -
    :           ➡️ -
    upper case  ➡️ lower case

    Args:
        text (_type_): _description_
    """

    text = text.replace(" ", "-")
    text = re.sub(r"[(),!?\&,+:]", "", text)

    text = text.lower()

    return text


if __name__ == "__main__":
    chapter_json_path = sys.argv[1]
    week = sys.argv[2]

    with open(f"{chapter_json_path}", encoding="utf-8") as fp:
        sections = json.load(fp)
        weekly_sections = [
            section for section in sections if section.get("week") == int(week)
        ]

    section_titles = []
    for section in weekly_sections:
        index = section.get("object_index")
        title = section.get("title")

        WIKI_URL = "https://github.com/Udemy-kor/aws-saa/wiki/04-학습-상세-목차#"
        link_url = f"{WIKI_URL}섹션{index}-{convert_special_characters(title)}"

        linked_title = f"[{index}. {title}]({link_url})"

        section_titles.append(linked_title)

    print("\n".join(section_titles))
