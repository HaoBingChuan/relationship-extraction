from pprint import pprint
import json


# 打印badcase信息
def compare(first_file, second_file):
    first_lines = list(json.loads(line.strip()) for line in open(first_file))
    second_lines = list(json.loads(line.strip()) for line in open(second_file))
    assert len(first_lines) == len(second_lines)
    for index, value in enumerate(zip(first_lines, second_lines)):
        if value[0] != value[1]:
            print(index)
            print("origin:")
            pprint(value[0])
            print("predict:")
            pprint(value[1])
            print("\n")


if __name__ == "__main__":
    compare(
        "data/aiStudioKE/format/test.json",
        "data/aiStudioKE/predict/fine_tune/test.json",
    )
