import json


def write_data(param:int) -> str:
    json_data : dict = {
        "number": param,
    }
    json_data["myNew_key"]= "myNew_value"
    
    for i in range(100):
        json_data[f"key_{i}"] = f"value_{i}"
    
    with open("D:/Documents/Development/FH_Salzburg/pipeline/.data/output.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    
    return str(json.dumps(json_data, indent=4))


def load_data():
    with open("D:/Documents/Development/FH_Salzburg/pipeline/.data/output.json", "r") as json_file:
        data = json.load(json_file)

    print(json.dumps(data, indent=4))


if __name__ == '__main__':
    write_data(42)

    load_data()