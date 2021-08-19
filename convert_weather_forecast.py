#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from multiprocessing import Pool

import argparse
import numpy as np
import pygrib

# Path to the first GRIB file (+0-15h)
FNAME1 = "data/Z__C_RJTD_%Y%m%d%H0000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin"
# Path to the second GRIB file (+16-33h)
FNAME2 = "data/Z__C_RJTD_%Y%m%d%H0000_MSM_GPV_Rjp_Lsurf_FH16-33_grib2.bin"
# Time lag until a forecast becomes availabel (in hours)
LAG = 3


def _read_grib(fname, skip=0):
    results = []

    with pygrib.open(fname) as f:
        # Read all grib messages from file -- turns out this is the fastest way
        grbs = f.read()

        if len(grbs) == 0:
            print(f"len(grbs) = 0 for file {fname}")

        # We assume the grid dimensions are identical for all grib messages
        # .latlons() is a fairly expensive function to call
        lats, lons = grbs[0].latlons()

        # Convert the latitude/longitude of the target point into array indices
        i = int((lats.max() - args.lat) / ((lats.max() - lats.min()) / lats.shape[0]))
        j = int((args.lon - lons.min()) / ((lons.max() - lons.min()) / lats.shape[1]))

        # There are 12 features for each forecast time
        # .select() is slow and should be avoided
        for ix in range(skip, len(grbs), 12):
            results.append([grb.values[i, j] for grb in grbs[ix:ix+12]])

    return results


def read_grib(dt):
    print(dt, flush=True)

    dt -= timedelta(hours=LAG)

    # Calculate latest forecast time
    forecast_dt = dt.replace(hour=dt.hour // 3 * 3)

    results = []

    results += _read_grib(forecast_dt.strftime(FNAME1), skip=10)
    results += _read_grib(forecast_dt.strftime(FNAME2), skip=0)

    # How many hours to skip
    offset = dt.hour % 3 + LAG

    return results[offset:offset+24]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="Output file name")
    parser.add_argument("--lat", type=float, help="Latitude of target location")
    parser.add_argument("--lon", type=float, help="Longitude of target location")
    parser.add_argument("--start", help="Start date (inclusive)",
                        type=lambda s: datetime.strptime(s, "%Y/%m/%d"))
    parser.add_argument("--end", help="End date (exclusive)",
                        type=lambda s: datetime.strptime(s, "%Y/%m/%d"))

    global args
    args = parser.parse_args()

    def dates(start, end):
        dt = start
        while dt < end:
            yield dt.astimezone(timezone.utc)
            dt += timedelta(hours=1)

    with Pool() as pool:
        results = pool.map(read_grib, dates(args.start, args.end))

        np.save(args.output, np.array(results))


if __name__ == "__main__":
    main()
