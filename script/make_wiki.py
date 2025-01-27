import json
import sys
import re

from collections import deque
from math import ceil


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


def create_wiki_markdown(study_schedule: deque, save_md_path, lecture_group_by_chapter):
    SCHEDULE_TITLE = "---\n\n### 📅 {week_num} 주차 ({date})\n\n"

    week_num = 1
    schedule = study_schedule.popleft()
    current_cnt = schedule["cnt"]

    schedule_markdown_content = SCHEDULE_TITLE.format(
        week_num=week_num, date=schedule["date"]
    )

    detail_markdown_content = ""
    for chapter in lecture_group_by_chapter.values():
        chapter_idx = chapter["object_index"]
        title = chapter["title"]

        if chapter_idx > current_cnt:
            schedule = study_schedule.popleft()
            current_cnt += schedule["cnt"]
            week_num += 1
            schedule_markdown_content += SCHEDULE_TITLE.format(
                week_num=week_num, date=schedule["date"]
            )

        WIKI_URL = "https://github.com/Udemy-kor/aws-saa/wiki/04-학습-상세-목차#"
        link_url = f"{WIKI_URL}섹션{chapter_idx}-{convert_special_characters(title)}"

        linked_title = f"[{chapter_idx}. {title}]({link_url})\n\n"

        schedule_markdown_content += linked_title
        detail_markdown_content += f"### 섹션{chapter_idx}: {title}\n\n"

        for lecture in chapter["children"]:
            if lecture["_class"] == "quiz":
                icon = "❓"
                content = f"퀴즈 {lecture['object_index']}: {icon} [{lecture['title']}](https://www.udemy.com/course/best-aws-certified-solutions-architect-associate/learn/lecture/{lecture['id']})\n\n"
            else:
                icon = "📺" if lecture["asset"]["asset_type"] == "Video" else "📚"
                time = ceil(lecture["asset"]["time_estimation"] / 60)
                content = f"{lecture['object_index']}. {icon} [{lecture['title']}](https://www.udemy.com/course/best-aws-certified-solutions-architect-associate/learn/lecture/{lecture['id']}) | {time}분\n\n"

            detail_markdown_content += content

    with open(save_md_path + "wiki-schedule.md", "w", encoding="utf8") as f:
        f.write(schedule_markdown_content)

    with open(save_md_path + "wiki-detail.md", "w", encoding="utf8") as f:
        f.write(detail_markdown_content)


if __name__ == "__main__":
    raw_json_path = sys.argv[1]
    save_md_path = sys.argv[2]
    convert_data_path = raw_json_path.replace("raw", "lecture_group_by_chapter")

    study_schedule = deque(
        [
            {"date": "2/10 ~ ", "cnt": 5},
            {"date": "2/17 ~ ", "cnt": 5},
            {"date": "2/24 ~ ", "cnt": 5},
            {"date": "3/3 ~ ", "cnt": 4},
            {"date": "3/10 ~ ", "cnt": 6},
            {"date": "3/17 ~ ", "cnt": 2},
            {"date": "3/24 ~ ", "cnt": 6},
        ]
    )

    with open(raw_json_path, "r", encoding="utf8") as f:
        lecture_group_by_chapter = json.load(f)

        create_wiki_markdown(study_schedule, save_md_path, lecture_group_by_chapter)
