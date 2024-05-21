import json
import re


def duie2doccano(duie_file, doccano_file, category_num):
    """
    将duie数据格式转为doccano标注工具生产的数据格式，用于paddleNLP微调
    para:
        duie_file: duie数据文件路径
        doccano_file: doccano数据文件路径
        category_num: 每个类别数据量
    """

    with open(doccano_file, "w", encoding="utf-8") as f:
        with open(duie_file) as duie_f:
            predicate_num_dict = {}
            text_id = 11
            for sentence in duie_f:
                sentence = json.loads(sentence)
                text = sentence["text"]
                spo_list = sentence["spo_list"]
                entities = []
                entity_id = int(str(text_id) + str(11))
                relations = []
                relation_id = int(str(text_id) + str(1111))
                for spo in spo_list:
                    predicate = spo["predicate"]
                    object = spo["object"]["@value"].replace("(", "").replace(")", "")
                    object_index = [r.span() for r in re.finditer(object, text)]
                    subject = spo["subject"].replace("(", "").replace(")", "")
                    subject_index = [r.span() for r in re.finditer(subject, text)]
                    if len(subject_index) == 1 and len(object_index) == 1:

                        if predicate not in predicate_num_dict:
                            predicate_num_dict[predicate] = 1
                        else:
                            predicate_num_dict[predicate] += 1

                        if (
                            predicate_num_dict[predicate] <= category_num
                        ):  # 控制每类类别数量
                            from_entity_id = entity_id
                            to_entity_id = entity_id + 1
                            entity_subject = {
                                "id": from_entity_id,
                                "label": spo["subject_type"],
                                "start_offset": subject_index[0][0],
                                "end_offset": subject_index[0][1],
                            }
                            entity_object = {
                                "id": to_entity_id,
                                "label": spo["object_type"]["@value"],
                                "start_offset": object_index[0][0],
                                "end_offset": object_index[0][1],
                            }
                            entities.append(entity_subject)
                            entities.append(entity_object)
                            relation = {
                                "id": relation_id,
                                "type": spo["predicate"],
                                "from_id": from_entity_id,
                                "to_id": to_entity_id,
                            }
                            relations.append(relation)
                            data = {
                                "id": text_id,
                                "text": text,
                                "entities": entities,
                                "relations": relations,
                            }
                            data = json.dumps(data, ensure_ascii=False)
                            f.write(data + "\n")
                            text_id += 1

                    # if text_id == 500:
                    # break


if __name__ == "__main__":
    duie_file = (
        "/home/haobingchuan/relation_extraction/data/aiStudioKE/format/train.json"
    )
    doccano_file = "fine_tune/data/aiStudioKE/aiStudioKE_doccano_ext.json"
    duie2doccano(duie_file, doccano_file, category_num=10)
