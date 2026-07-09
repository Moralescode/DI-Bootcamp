import json

nb_path = r'C:\Users\DELL\Desktop\TTA_Donald_KOUASSI\DI_BOOTCAMP_2026\WEEK4\Day4\ExerciceXP\ExerciceXP.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("Remaining TODO cells:")
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])
    if 'TODO' in src:
        print(f"Cell {i} ({cell['cell_type']}):")
        print(src[:500])
        print("---")
