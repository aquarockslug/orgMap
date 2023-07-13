import json

OUTPUT_FILENAME = 'testData'
ZIP_PROP_NAME = 'ZCTA5CE10'


def main():
    zip_data = load_json()

    # create print_prop + zip_data curry function?

    for feature in zip_data['features']:
        props = feature['properties']
        props['DATA'] = '123456789'

    print(key_str(zip_data))
    print(prop_str(zip_data, 'DATA', 10))

    with open(f'{OUTPUT_FILENAME}.js', 'w', encoding='UTF-8') as out:
        out.write(f'{OUTPUT_FILENAME} = ')
        out.write(json.dumps(zip_data))


def load_json() -> dict:
    with open('wi.json', 'r', encoding='UTF-8') as file:
        return json.load(file)


def key_str(data: dict) -> str:
    return ', '.join(data['features'][0]['properties'].keys())


def prop_str(data: dict, prop: str, count: int) -> str:
    new_prop_str = ''
    for i, feature in enumerate(data["features"]):
        new_prop_str += f'{feature["properties"][prop]}, '
        if i == count:
            break
    return new_prop_str[: len(new_prop_str) - 2]


if __name__ == '__main__':
    main()
