import json
import pandas as pd

DATA_FILENAME = "income.csv"
OUTPUT_FILENAME = "testData"
MARKER_FILENAME = "markerData.json"
ZIP_PROP_NAME = "ZCTA5CE10"
ROUND_COORDS = 4

def main():
    """main"""
    state_zips_filenames = ["../State-zip-code-GeoJSON/wi_wisconsin_zip_codes_geo.min.json",
                            "../State-zip-code-GeoJSON/il_illinois_zip_codes_geo.min.json"]

    all_states = []
    for zip_data_filename in state_zips_filenames:
        state_features = create_features(zip_data_filename)
        summarize(state_features)
        # write(state_features, zip_data_filename.split('/')[-1])
        all_states.append(state_features)

    write(all_states[0] + all_states[1], "testData")

def create_features(filename):
    """creates a list of geoJSON featuress"""
    # get input data
    global database
    database = load_database(DATA_FILENAME)

    # get marker data
    global marker_zip_set
    marker_zip_set = set()  # set of zip codes with markers in them
    for marker in load_json(MARKER_FILENAME)["marker_data"]:  # from markerData.js
        marker_zip_set.add(marker["ZIP"])

    # remove zips that don't include markers then round remaining coordinates
    marker_zips = round_coordinates(get_marker_zips(filename), ROUND_COORDS)

    # combine zip data and input data
    add_input_data(marker_zips)

    return marker_zips

def get_marker_zips(zip_data_filename) -> list:
    """remove geoJSON features with zips that are not in marker_zip_set"""
    def is_marker_zip(zip_data) -> bool:
        return True if zip_data["properties"][ZIP_PROP_NAME] in marker_zip_set else False
    return list(filter(is_marker_zip, load_json(f"{zip_data_filename}")["features"]))


# round coordinates
def round_coordinates(data, precision) -> list:
    def apply(item, fun):
        if isinstance(item, list):
            return [apply(x, fun) for x in item]
        return fun(item)

    for i, feature in enumerate(data):
        data[i]["geometry"]["coordinates"] = apply(
            feature["geometry"]["coordinates"], lambda x: round(x, precision)
        )
    return data



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


def write(data, output_filename):
    """create the output file"""
    with open(f"{output_filename}.js", "w", encoding="UTF-8") as out:
        out.write(f"testData = ")
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
