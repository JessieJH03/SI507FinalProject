import json

def save_to_json_file(root_node, file_name):
    with open(file_name, 'w') as file:
        json.dump(root_node.serialize(), file, indent=4)

