import shutil


def clear_terminal():
    # ターミナルの高さを取得
    terminal_height = shutil.get_terminal_size().lines
    # 高さ分の改行を出力
    print("\n" * terminal_height)


# ターミナルにマップと進捗を表示
def display_map(status):
    if status.show_output:
        # 画面クリア
        print("\033[H\033[J", end="")

        print("-" * 50)
        print()
        print(f"Map:")
        print("\n".join(status.store_map[0]))


# ターミナルに最終結果を出力
def display_results(
    status, output_file_path 
):
    if not status.show_output:
        pass
    print(f"\nOutput file path: {output_file_path}\n")
    clear_terminal()
