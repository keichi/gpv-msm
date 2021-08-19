#!/usr/bin/env python3

from datetime import datetime, timedelta

import argparse
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input csv file name")
    parser.add_argument("output", help="Output numpy file name")
    parser.add_argument("--start", help="Start date (inclusive)",
                        type=lambda s: datetime.strptime(s, "%Y/%m/%d"))
    parser.add_argument("--end", help="End date (exclusive)",
                        type=lambda s: datetime.strptime(s, "%Y/%m/%d"))

    args = parser.parse_args()

    def dates(start, end):
        dt = start
        while dt < end:
            yield dt
            dt += timedelta(hours=1)

    df = pd.read_csv(args.input, header=0, names=["date", "power"],
                     dtype={"power": np.int64}, parse_dates=["date"])

    # Remove rows with duplicate dates
    # This is needed because power_generation_09.csv contains duplicate rows
    df = df.drop_duplicates(subset="date", keep="first")

    # Use dates as index
    df = df.set_index("date")

    # Iterate through dates and replace missing values with NaN
    out = [df.loc[dt, "power"] if dt in df.index else np.nan
           for dt in dates(args.start, args.end)]

    np.save(args.output, np.array(out))


if __name__ == "__main__":
    main()
