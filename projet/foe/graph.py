from math import floor
from time import sleep

import matplotlib.pyplot as plt
import requests

from mod.progress_bar import Bar

RUSH = 1.9
GM_KEY = "X_FutureEra_Landmark1"
INTERVAL = (1, 101)

progb = Bar(INTERVAL[1] - INTERVAL[0], "*", "p")

req_pf = []
for gm_lvl in range(INTERVAL[0], INTERVAL[1]):
    gm_data = requests.get(f"https://api.foe-helper.com/v1/LegendaryBuilding/get?id={GM_KEY}&level={gm_lvl}").json()

    if gm_data["status"] != 200:
        print(f"Error: status {gm_data['status']}")
        exit(1)

    total_fp = gm_data["response"]["total_fp"]
    fp_rwds = [r["forgepoints"] for r in gm_data["response"]["patron_bonus"]]

    req_pf.append(total_fp - sum(floor(e * RUSH) or 1 for e in fp_rwds))
    progb.progress(gm_lvl)
    sleep(0.1)


# draw graph with matplotlib

plt.plot(range(INTERVAL[0], INTERVAL[1]), req_pf)
plt.show()
