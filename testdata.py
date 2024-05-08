
import json
filename = "questionsmaths.json"


def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


res_math = load_from_json(filename)
# Create a new list with the classification 'maths'
res_code = load_from_json("questionscode.json")
classified_data = [(quote, 'maths') for quote in res_math]
classified_code = [(quote, 'code') for quote in res_code]
# Save the new list to a new file
new_filename = "classified_questionsmaths.json"
with open(new_filename, 'w', encoding='utf-8') as file:
    json.dump(classified_data, file)

new_filename = "classified_questionscode.json"
with open(new_filename, 'w', encoding='utf-8') as file:
    json.dump(classified_code, file)

print(f"Data saved to {new_filename}")
