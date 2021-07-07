#!/usr/bin/env python3

import datetime


start_date = datetime.date(2017, 12, 5)
end_date = datetime.date(2018, 1, 1)
delta = datetime.timedelta(days=1)

while start_date < end_date:
    y = start_date.year
    m = start_date.month
    d = start_date.day

    url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{y:04}/{m:02}/{d:02}"

    for t in [0, 3, 6, 9, 12, 15, 18, 21]:
        print(f"{url}/Z__C_RJTD_{y:04}{m:02}{d:02}{t:02}0000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin")
        print(f"{url}/Z__C_RJTD_{y:04}{m:02}{d:02}{t:02}0000_MSM_GPV_Rjp_Lsurf_FH16-33_grib2.bin")
        print(f"{url}/Z__C_RJTD_{y:04}{m:02}{d:02}{t:02}0000_MSM_GPV_Rjp_Lsurf_FH34-39_grib2.bin")

    start_date += delta
