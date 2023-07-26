import json
import pandas as pd

DATA_FILENAME = "income.csv"
OUTPUT_FILENAME = "testData"
MARKER_FILENAME = "markerData.json"
ZIP_PROP_NAME = "ZCTA5CE10"
ZIP_DATA_JSON_FILENAME = "wi"
ROUND_COORDS = 3


def main():
    """main"""
    # get input data
    global database
    database = load_database(DATA_FILENAME)

    # get marker data
    global marker_zip_set
    marker_zip_set = set()  # set of zip codes with markers in them
    for marker in load_json(MARKER_FILENAME)["marker_data"]:  # from markerData.js
        marker_zip_set.add(marker["ZIP"])

    # remove zips that don't contain markers
    all_zip_data = load_json(f"{ZIP_DATA_JSON_FILENAME}.json")
    marker_zip_data = list(filter(is_marker_zip, all_zip_data["features"]))

    marker_zip_data = round_coordinates(marker_zip_data, ROUND_COORDS)

    # combine zip data and input data
    add_input_data(marker_zip_data)

    # output
    summarize(marker_zip_data)
    write(marker_zip_data)

# round coordinates
def round_coordinates(data, precision):
    def apply(item, fun):
        if isinstance(item, list):
            return [apply(x, fun) for x in item]
        else:
            return fun(item)

    for i, feature in enumerate(data):
         data[i]["geometry"]["coordinates"] = apply(
            feature["geometry"]["coordinates"], lambda x: round(x, precision)
        )
    return data

def is_marker_zip(zip_data):
    return True if zip_data["properties"][ZIP_PROP_NAME] in marker_zip_set else False


def load_json(filename) -> dict:
    """returns data loaded from a json file"""
    with open(filename, "r", encoding="UTF-8") as file:
        return json.load(file)


def load_csv(filename):
    """returns data loaded from a csv file"""
    with open(filename, "r", encoding="UTF-8") as file:
        return pd.read_csv(file.read())


def load_database(filename) -> dict:
    data_in = pd.read_csv(filename)
    zData = set()
    for z in data_in["zip"]:
        if pd.notna(z):
            zData.add(int(z))

    database = dict()
    for z in zData:
        if len(str(z)) == 5:
            database[str(z)] = data_in[data_in["zip"] == z]["count"]

    return database


def add_input_data(data):
    """add input data to geographic zipcode data"""
    for feature in data:
        props = feature["properties"]
        props["DATA"] = get_data(props[ZIP_PROP_NAME])


def get_data(zipcode) -> int:
    """get the correct piece of data to display for the zipcode"""
    if str(zipcode) in database:
        input_data = database[str(zipcode)].values[6]
        return input_data
    else:
        print(f"{zipcode} not found in database")
        return 0


def write(data):
    """create the output file"""
    with open(f"{OUTPUT_FILENAME}.js", "w", encoding="UTF-8") as out:
        out.write(f"{OUTPUT_FILENAME} = ")
        out.write(json.dumps(data))


def summarize(data):
    """summarize data"""
    print(f"\nKEYS:\n{key_str(data)}\n")
    print(f'DATA:\n{prop_str(data, "DATA")}\n')
    print(f'COORDS:\n{data[0]["geometry"]["coordinates"][0][:5]}\n')
    print(f"LENGTH:\n{len(data)}\n")


def key_str(data: dict) -> str:
    """returns a string of the dictonary keys"""
    return ", ".join(data[0]["properties"].keys())


def prop_str(data: dict, prop: str, count: int = 10) -> str:
    """returns a string of the given property"""
    new_prop_str = ""
    for i, feature in enumerate(data):
        new_prop_str += f'{feature["properties"][prop]}, '
        if i == count:
            break
    return new_prop_str[: len(new_prop_str) - 2]


if __name__ == "__main__":
    main()
