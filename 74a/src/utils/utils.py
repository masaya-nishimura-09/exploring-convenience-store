import datetime


# 現在の日時を文字列で返す
def get_date():
    now = datetime.datetime.now()
    date = datetime.date.today()
    time = now.strftime("%H-%M-%S-%f")
    return f"{date}_{time}"
