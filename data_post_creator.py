import json
import random
import pandas as pd

OUTPUT_FILENAME = "testData"
ZIP_PROP_NAME = "ZCTA5CE10"
ZIP_DATA_JSON_FILENAME = "wi"


def main():
    """main"""
    data_in = pd.read_csv("income.csv")

    zData = set()
    for z in data_in["zip"]:
        if pd.notna(z):
            zData.add(int(z))

    inData = dict()
    for z in zData:
        if (len(str(z)) == 5):
            inData[str(z)] = data_in[data_in["zip"] == z]["count"]

    print(inData["54956"].values[1])

    # zip_data = load_json(f"{ZIP_DATA_JSON_FILENAME}.json")
    # add_input_data(zip_data)
    # summarize(zip_data)
    # write(zip_data)


def load_json(filename) -> dict:
    """returns data loaded from a json file"""
    with open(filename, "r", encoding="UTF-8") as file:
        return json.load(file)


def load_csv(filename):
    """returns data loaded from a csv file"""
    with open(filename, "r", encoding="UTF-8") as file:
        return pd.read_csv(file.read())


def add_input_data(data):
    """add input data to geographic zipcode data"""
    for feature in data["features"]:
        props = feature["properties"]
        props["DATA"] = get_data(props[ZIP_PROP_NAME])


def get_data(zipcode) -> int:
    """get the correct piece of data to display for the zipcode"""
    # TODO: get correct data and normalize it
    input_data = random.randint(1, 100)
    return input_data


def write(data):
    """create the output file"""
    with open(f"{OUTPUT_FILENAME}.js", "w", encoding="UTF-8") as out:
        out.write(f"{OUTPUT_FILENAME} = ")
        out.write(json.dumps(data))


def summarize(data):
    """summarize data"""
    print(f"KEYS:\n{key_str(data)}\n")
    print(f'DATA:\n{prop_str(data, "DATA")}')


def key_str(data: dict) -> str:
    """returns a string of the dictonary keys"""
    return ", ".join(data["features"][0]["properties"].keys())


def prop_str(data: dict, prop: str, count: int = 10) -> str:
    """returns a string of the given property"""
    new_prop_str = ""
    for i, feature in enumerate(data["features"]):
        new_prop_str += f'{feature["properties"][prop]}, '
        if i == count:
            break
    return new_prop_str[: len(new_prop_str) - 2]


if __name__ == "__main__":
    main()
