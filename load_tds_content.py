import os
import json

def load_tds_content(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".md"):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                data.append({"title": file, "content": f.read()})

    with open("tds_content.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    folder_path = "tds_course_material"
    load_tds_content(folder_path)
