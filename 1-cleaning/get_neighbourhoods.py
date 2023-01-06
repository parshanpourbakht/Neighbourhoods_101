import sys
import pandas as pd


def main(boundaries_file, output_file):
    # read semicolon separated csv file
    boundaries = pd.read_csv(boundaries_file, sep=";")
    # remove unneeded columns
    boundaries = boundaries.drop(["MAPID", "Geom"], axis=1)
    boundaries = boundaries.rename(str.lower, axis=1)

    # get lat and lon from column "geo_point_2d" which is formatted
    # like the string "{lat},{lon}", containing the coordinate
    # of the neighbourhood
    boundaries[["lat","lon"]] = pd.DataFrame(
            boundaries["geo_point_2d"].str.split(",").tolist()
        )
    # remove unneeded column
    boundaries = boundaries.drop(["geo_point_2d"], axis=1)

    boundaries.to_csv(output_file, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
