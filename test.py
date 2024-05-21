from pprint import pprint
from paddlenlp import Taskflow
import json

ie = Taskflow(
    "information_extraction",
    schema={
        "人物": [
            "姓名",
            "年龄",
            "性别",
            "祖籍",
            "职业",
            "毕业学校",
            "出生日期",
            "出生地",
            "发布专辑",
            "荣誉",
        ]
    },
    task_path="fine_tune/checkpoint/model_best_aiStudioKE",
    device_id=0,
)
pprint(
    ie(
        "周杰伦（Jay Chou），1979年1月18日出生于台湾省新北市，祖籍福建省永春县，华语流行乐男歌手、音乐人、演员、导演、编剧，毕业于淡江中学。"
    )
)
