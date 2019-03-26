import json

with open('./results.json', 'r') as fin:
    data = json.load(fin)
    for exp, result in data["results"].items():
        ours_win = result["ours_win"]
        ours_lose = result["ours_lose"]
        total = ours_win + ours_lose
        ours_win_percent = ours_win / total * 100
        mask_type = "_".join(exp.split('_')[:2])
        mask_ratio = exp.split('_')[-4]
        baseline = exp.split('_')[-1]
        # print(f"{mask_type}, {mask_ratio}, {baseline}, {ours_win_percent:.1f}")
        print(f"{exp} {ours_win_percent:.1f}% ({ours_win} / {total})")
