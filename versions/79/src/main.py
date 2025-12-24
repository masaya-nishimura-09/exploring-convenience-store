import random, time
from utils.status import Status, Position  
from utils.io_utils import (
    load_config,
    create_output_file,
    write_results,
)
from utils.display_utils import display_results
from utils.store_map import (
    get_random_position,
    move_people,
)
from utils.display_utils import display_map
from libs.map import map_data


def main():
    # 設定ファイルからパラメータを取得
    config = load_config()

    # 地図を読み込む
    store_map = map_data

    # ステータスの初期化
    position = Position(
        config["vertical"],
        config["horizontal"],
    )
    status = Status(
        position=position,
        show_output=config["show_output"],
        store_map=store_map,
    )

    # 初期人の配置
    for i in range(config["people"]):
        x, y = get_random_position(
            status.store_map, config["vertical"], config["horizontal"]
        )
        row = list(status.store_map[0][x])
        row[y] = "!"
        status.store_map[0][x] = "".join(row)
        status.people.append((x, y))

    for i in range(50):
        move_people(status)
        display_map(status)
        output_file_path = create_output_file(config["version"])
        write_results(
            status, output_file_path
        )
        time.sleep(1)

if __name__ == "__main__":
    main()
