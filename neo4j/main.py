import logging
from pprint import pprint
from paddlenlp import Taskflow
import config.logConfig
import pandas as pd
from tests.neoTest import post_nego
from infra.neo4j.neoClient import *
from py2neo import NodeMatcher
import csv


logger = logging.getLogger(__name__)


RET_SCHEMA = {
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
TASK = Taskflow(
    "information_extraction",
    schema={"人物": ["出生地"]},
    # task_path="fine_tune/checkpoint/model_best_aiStudioKE",
)


# 关系抽取(文本中识别实体并抽取实体之间的语义关系，进而获取三元组信息)
def relationship_extract(text_file: str, task: Taskflow, ret_schema: dict) -> list:

    # 获取文件中文本语句
    sentence_list = []
    with open(text_file, "r", encoding="utf-8") as f:
        for key, values in ret_schema.items():
            schema = {}
            schema[key] = values
            task.set_schema(schema)
            for line in f.readlines():
                line = line.strip()
                for sentence in line.split("。"):
                    if sentence:
                        sentence_list.append(sentence)
    logger.info(f"句子数量：{len(sentence_list)}")

    # 提取句子中spo三元组
    spo_list = []
    for sentence in sentence_list:
        subject_types = task(sentence)
        for subject_type in subject_types:
            if subject_type:
                for (
                    _,
                    spos,
                ) in subject_type.items():  # 获取schema具体spo关系值
                    for spo in spos:
                        if "relations" in spo:
                            subject = spo["text"]
                            for predicate, objects in spo[
                                "relations"
                            ].items():  # 获取object具体情况，包含关系、置信度、文本
                                for object in objects:
                                    object = object["text"]
                                    spo_info = [
                                        sentence,
                                        subject,
                                        predicate,
                                        object,
                                    ]
                                    if spo_info not in spo_list:
                                        spo_list.append(spo_info)
    return spo_list


def spo_to_neo4j(spo_file: str):
    """
    将spo_list数据写入neo4j数据库
    """

    gragh = graph_conn()

    # 打开csv文件，以utf-8编码方式读取
    with open(spo_file, "r", encoding="utf-8") as f:
        # 创建csvreader对象，用于读取csv文件
        csvreader = csv.reader(f)
        # 遍历csv文件中的每一行
        for i, row in enumerate(csvreader):
            logger.info(f"正在处理第{i+1}行数据")
            # 如果每一行的第2、3、4个元素都不为空
            if row[1] and row[2] and row[3]:
                # 调用post_nego函数，传入每一行的第2、3、4个元素
                tx = gragh.begin()
                matcher = NodeMatcher(gragh)
                subject_node = matcher.match("TEST", name=row[1]).first()
                object_node = matcher.match("TEST", name=row[3]).first()
                if subject_node and object_node:
                    ab = Relationship(subject_node, row[2], object_node)
                elif subject_node and not object_node:
                    object_node = Node("TEST", name=row[3])
                    gragh.create(object_node)
                elif not subject_node and object_node:
                    subject_node = Node("TEST", name=row[1])
                    gragh.create(subject_node)
                else:
                    subject_node = Node("TEST", name=row[1])
                    object_node = Node("TEST", name=row[3])
                    gragh.create(subject_node)
                    gragh.create(object_node)

                ab = Relationship(subject_node, row[2], object_node)
                tx.create(ab)  # 创建节点和关系
                gragh.commit(tx)


def main(text_file: str, intermediate_dir: str):
    """
    输入文本文件,输出中间文件,实体关系对入库
    """
    text_id = text_file.split("/")[-1].split(".")[0]
    # 1.获取TXT文件实体关系对数据
    all_relationship_info = relationship_extract(
        text_file, task=TASK, ret_schema=RET_SCHEMA
    )

    # 2.将数据写入中间文件
    relationship_pd = pd.DataFrame(
        all_relationship_info,
        columns=["text", "subject", "predicate", "object"],
    )
    intermediate_file = intermediate_dir + "/" + text_id + ".csv"
    relationship_pd.to_csv(
        intermediate_file,
        mode="w",
        index=False,
    )

    # 3.读取中间文件将数据写入neo4j数据库
    spo_to_neo4j(intermediate_file)


if __name__ == "__main__":
    text_file = "input/test.txt"
    intermediate_dir = "output"
    main(text_file, intermediate_dir)
