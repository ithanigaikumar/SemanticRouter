import json


def read_quotes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [json.loads(line.strip()) for line in lines]
        return data


filename = "train.jsonl"
list_to_iterate = read_quotes(filename)
res = [item["question"] for item in list_to_iterate]


def read_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


filename_code = "glaive_code_assistant_v2.json"
data = read_json(filename_code)
print(data)
