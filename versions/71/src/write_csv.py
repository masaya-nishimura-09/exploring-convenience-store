import os
import csv
from io_utils import get_root_dir

root_dir = get_root_dir()


def write_csv(results):
    for result in results:
        with open(
            os.path.join(root_dir, f"output/stats/{result[0]["name1"]}.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as f:
            # CSVのヘッダーを作成
            csv_writer = csv.writer(f)
            csv_writer.writerow(["Name1", "Name2", "Similarity"])

            for item in result:
                # 結果をcsvファイルに書き込み
                csv_writer.writerow(
                    [
                        item["name1"],
                        item["name2"],
                        f"{item['similarity']:.4f}",
                    ]
                )
