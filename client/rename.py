import os

files = sorted(os.listdir('.'))
with open('filelist.csv', 'w') as fout:
    for i, f in enumerate(files):
        if not f.endswith('.mp4'):
            continue
        data = f.split('_')
        type = "_".join(data[:-10])
        ratio = data[-9]
        method_A = data[-5]
        method_B = data[-3]
        new_name = f"{type}_{ratio}_{i:04d}.mp4"
        out = f"/Video/{new_name},{type},{ratio},{method_A},{method_B},{f}"
        print(f"{out}")
        os.rename(f, new_name)
        fout.write(f"{out}\n")
