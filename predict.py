from pprint import pprint
from paddlenlp import Taskflow
import json
import time
from util import extract_relation_from_duie


def predict(
    source_file,
    predict_file,
):
    """
    将抽取的结果转换为DuIE的格式,方便后续评估
    param:
        source_file: 原始数据文件,DuIE数据格式文件
        predict_file: 预测结果文件,DuIE数据格式文件
    """
    with open(predict_file, "w", encoding="utf-8") as predicate_file:
        with open(source_file, "r") as f:
            num = 0
            for sentence in f.readlines():
                ans = extract_relation_from_duie(json.loads(sentence), ie=ie)
                spo_str = json.dumps(ans, ensure_ascii=False)
                print("转换为DuIE的spo三元组结果：", spo_str)
                predicate_file.write(spo_str + "\n")
                num += 1
                print(f"抽取第{num}条数据")


if __name__ == "__main__":
    ie = Taskflow(
        "information_extraction",
        task_path="fine_tune/checkpoint/model_best_aiStudioKE",
        device_id=0,
    )

    source_file = "data/aiStudioKE/format/test.json"
    predict_file = "data/aiStudioKE/predict/fine_tune/test.json"

    predict(source_file=source_file, predict_file=predict_file)
