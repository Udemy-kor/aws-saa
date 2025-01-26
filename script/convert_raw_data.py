import json
import sys

from collections import defaultdict
from math import ceil

lecture_group_by_chapter = defaultdict(dict)

if __name__ == "__main__":
    raw_json_path = sys.argv[1]
    save_md_path = sys.argv[2]
    convert_data_path = raw_json_path.replace("raw", "lecture_group_by_chapter")

    with open(raw_json_path, "r", encoding="utf8") as f:
        data = json.load(f)

        chapter_idx = 0
        lecture_idx = 1

        for item in data:
            if item["_class"] == "chapter":
                chapter_idx += 1
                item["children"] = []
                lecture_group_by_chapter[chapter_idx] = item
            else:
                lecture_group_by_chapter[chapter_idx]["children"].append(item)
                lecture_idx += 1

    with open(convert_data_path, "w", encoding="utf8") as f:
        json.dump(lecture_group_by_chapter, f, indent=4, ensure_ascii=False)

    markdown = ""

    for chapter_idx, chapter in lecture_group_by_chapter.items():
        markdown += f"### 섹션{chapter['object_index']}: {chapter['title']}\n\n"
        for lecture in chapter["children"]:
            if lecture["_class"] == "quiz":
                icon = "❓"
                content = f"퀴즈 {lecture['object_index']}: {icon} [{lecture['title']}](https://www.udemy.com/course/best-aws-certified-solutions-architect-associate/learn/lecture/{lecture['id']})\n\n"
            else:
                icon = "📺" if lecture["asset"]["asset_type"] == "Video" else "📚"
                time = ceil(lecture["asset"]["time_estimation"] / 60)
                content = f"{lecture['object_index']}. {icon} [{lecture['title']}](https://www.udemy.com/course/best-aws-certified-solutions-architect-associate/learn/lecture/{lecture['id']}) | {time}분\n\n"

            markdown += content

    with open(save_md_path, "w", encoding="utf8") as f:
        f.write(markdown)
