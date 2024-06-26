import logging
from flask import Flask, request, jsonify
from paddlenlp import Taskflow
import config.logConfig

app = Flask(__name__)
logger = logging.getLogger(__name__)
schema = {
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
}
schema_rel = {
    "个人信息": [
        "姓名",
        "专辑",
        "性别",
        "祖籍",
        "职业",
        "毕业学校",
        "出生日期",
        "出生地",
        "发布专辑"
    ]
}
# device_id为gpu id，如果写-1则使用cpu
task = Taskflow("information_extraction", schema=schema_rel, device_id=-1)


def parse(result):
    result = result[0]
    formatted_result = []
    for label, ents in result.items():
        for ent in ents:
            formatted_result.append(
                {"label": label, "start_offset": ent["start"], "end_offset": ent["end"]}
            )
    return formatted_result


@app.route("/uie/extraction", methods=["POST"])
def get_result():
    text = request.json["text"]
    logger.info("Input text = {}".format(text))
    result = task(text)
    logger.info("Input result = {}".format(result))
    formatted_result = parse(result)
    return jsonify(formatted_result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8020)
