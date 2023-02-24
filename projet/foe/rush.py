# https://api.foe-helper.com/v1/LegendaryBuilding/get?id=X_ArcticFuture_Landmark2&level=54

from math import floor
import requests

PL_NAME = "pf4"

RUSH = 1.9

# Get the list of all legendary buildings
gm_keys, gm_names = [], []
gm_list = requests.get("https://api.foe-helper.com/v1/LegendaryBuilding/list").json()
if gm_list["status"] == 200:
    for gm in gm_list["response"]["buildings"]:
        gm_keys.append(gm["id"])
        gm_names.append(gm["name"])
else:
    print(f"Error: status {gm_list['status']}")
    exit(1)

for i in range(len(gm_keys)):
    print("{: >2} - {}".format(i, gm_names[i]))

user_input = int(input("ID -> "))
gm_lvl = int(input("Level -> "))
key = gm_keys[user_input]
gm_name = gm_names[user_input]

gm_data = requests.get(f"https://api.foe-helper.com/v1/LegendaryBuilding/get?id={key}&level={gm_lvl}").json()

if gm_data["status"] == 200:
    total_fp = gm_data["response"]["total_fp"]
    fp_rwds = [r["forgepoints"] for r in gm_data["response"]["patron_bonus"]]
else:
    print(f"Error: status {gm_data['status']}")
    exit(1)

print(f"{gm_name} ({key}) Level {gm_lvl} requires {total_fp} FP\n")

pastable_buffer = f"{PL_NAME} {gm_name} [{gm_lvl - 1} -> {gm_lvl}]&"

fp_rq = [floor(e * RUSH) or 1 for e in fp_rwds]

for i in range(len(fp_rwds)):
    print("P{} [{: >4} => {: >4} ] safe with {} pf".format(
        i+1,
        fp_rwds[i],
        fp_rq[i],
        min(max(0, total_fp - floor(sum(fp_rq[:i+1]) + fp_rq[i])), sum(fp_rq) - 1)
    ))

    pastable_buffer = pastable_buffer.replace("&", f"& P{i+1}({fp_rq[i]})")

print("\n|", pastable_buffer.replace("&", ""))
print(f"| you need to add {total_fp - sum(fp_rq) - 1} FP to level up (+1)")
