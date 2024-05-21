from pprint import pprint


def extract_schema_from_duie(duie_data: dict) -> list:
    """
    从duie格式的数据中的三元组提取schema信息,用于传入paddlenlp进行关系抽取
    """
    subject_types = list(
        set([spo["subject_type"] for spo in duie_data["spo_list"]])
    )  # 提取主体类型并去重
    schemas = []
    for subject_type in subject_types:
        schema = {subject_type: []}
        for spo in duie_data["spo_list"]:
            if (
                spo["subject_type"] == subject_type
                and spo["predicate"] not in schema[subject_type]
            ):
                schema[subject_type].append(spo["predicate"])
        if schema not in schemas:
            schemas.append(schema)
    return schemas


def extract_relation_from_duie(duie_data: dict, ie) -> dict:
    """
    基于paddlenlp提取实体关系,然后转换为duie格式,方便性能计算
    """
    spo_list = []
    text = duie_data["text"]
    origin_spo_list = duie_data["spo_list"]
    schemas = extract_schema_from_duie(duie_data)
    for schema in schemas:
        ie.set_schema(schema)
        subject_types = ie(text)
        print("text文本:", text)
        print("schema结构：", schema)
        print("\npaddlenlp关系提取结果:")
        pprint(subject_types)
        for subject_type in subject_types:
            if subject_type:
                for _, spos in subject_type.items():  # 获取schema具体spo关系值
                    for spo in spos:
                        if "relations" in spo:
                            subject = spo["text"]
                            for predicate, objects in spo[
                                "relations"
                            ].items():  # 获取object具体情况，包含关系、置信度、文本
                                for object in objects:
                                    spo_dict = {}
                                    object_value = {"@value": object["text"]}
                                    spo_dict = {
                                        "predicate": predicate,
                                        "subject": subject,
                                        "object": object_value,
                                    }
                                    for each in origin_spo_list:
                                        if predicate == each["predicate"]:
                                            spo_dict["subject_type"] = each[
                                                "subject_type"
                                            ]
                                            spo_dict["object_type"] = each[
                                                "object_type"
                                            ]
                                            break
                                    if spo_dict not in spo_list:
                                        spo_list.append(spo_dict)
    return {"text": text, "spo_list": spo_list}
