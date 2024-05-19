import csv
import requests
import random

def process_data(input_file):
    results = []
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)  # 将CSV数据转换为列表
        random_rows = random.sample(data, min(200, len(data)))  # 随机抽取200行或全部数据(如果少于200行)

        for row in random_rows:
            input_text = row[0]
            expected_intent = row[1]

            # 访问API接口
            api_url = "http://10.204.202.149:8869/predict"
            data = {"input_text": input_text}
            response = requests.post(api_url, json=data)
            api_response = response.json()

            # 组合结果
            result = {
                "input": input_text,
                "expected_intent": expected_intent,
                "expected_slots": {}
            }

            for slot_key, slot_value in api_response.get("slot_labels", {}).items():
                result["expected_slots"][slot_key] = {
                    "value": slot_value["value"],
                    "confidence": slot_value["confidence"]
                }

            results.append(result)

    return results

# 用法示例
input_file = "input.csv"
data = process_data(input_file)

# 将结果写入JSON文件
import json
with open("output.json", "w") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)