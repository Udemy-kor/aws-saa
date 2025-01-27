import json
import sys


if __name__ == "__main__":
    raw_json_path = sys.argv[1]
    output_directory = sys.argv[2]

    with open(raw_json_path, "r", encoding="utf8") as f:
        lecture_group_by_chapter = json.load(f)

        for chapter_idx, chapter in lecture_group_by_chapter.items():
            markdown = ""
            subfix_ext = ".md"

            file_name = (
                f"섹션 {chapter['object_index']}. {chapter['title'].replace(":", "-")}"
            )
            with open(
                output_directory + file_name + subfix_ext, "w", encoding="utf8"
            ) as f:
                pass

            for lecture in chapter["children"]:
                if lecture["_class"] == "quiz":
                    file_name = f"퀴즈 {lecture['object_index']}. {lecture['title']}"
                # else:
                #     file_name = f"{lecture['object_index']}. {lecture['title']}"

                with open(
                    output_directory + file_name.replace(":", "-") + subfix_ext,
                    "w",
                    encoding="utf8",
                ) as f:
                    pass
