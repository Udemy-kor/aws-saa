import json
import sys

from collections import defaultdict


def convert_raw_data_to_chapters(raw_json_path, output_directory):
    lecture_group_by_chapter = defaultdict(dict)

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

    with open(
        output_directory + "lecture_group_by_chapter.json", "w", encoding="utf8"
    ) as f:
        json.dump(lecture_group_by_chapter, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    raw_json_path = sys.argv[1]
    output_directory = sys.argv[2]

    convert_raw_data_to_chapters(raw_json_path, output_directory)
