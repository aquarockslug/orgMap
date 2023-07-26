import pandas as pd

df = pd.read_json("wi_truncated.json")


# round coordinates
def round_coordinates(df, precision):
    def apply(item, fun):
        if isinstance(item, list):
            return [apply(x, fun) for x in item]
        else:
            return fun(item)

    for i, feature in enumerate(df["features"]):
         df["features"][i]["geometry"]["coordinates"] = apply(
            feature["geometry"]["coordinates"], lambda x: round(x, precision)
        )

round_coordinates(df, 4)

print(df["features"][0]["geometry"]["coordinates"])
