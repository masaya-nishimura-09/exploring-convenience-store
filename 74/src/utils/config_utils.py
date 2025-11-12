import json
import os


# プロジェクトのルートディレクトリのパスを取得
def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 設定ファイルのパスを取得
def get_config_path():
    return os.path.join(get_root_dir(), "config.json")


# 設定ファイルを読み込み
def load_config():
    with open(get_config_path(), "r", encoding="utf-8") as file:
        config = json.load(file)
    return config


def get_similarity_threshold():
    config = load_config()
    return config["similarity_threshold"]


def get_project_version():
    config = load_config()
    return config["version"]


def get_runs_per_set():
    config = load_config()
    return config["runs_per_set"]


def get_sets():
    config = load_config()
    return config["sets"]


def get_title():
    config = load_config()
    return config["title"]


def get_item_amount():
    config = load_config()
    return config["item_amount"]


def get_vertical():
    config = load_config()
    return config["vertical"]
