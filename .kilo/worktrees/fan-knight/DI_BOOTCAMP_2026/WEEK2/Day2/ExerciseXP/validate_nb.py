import json
from pathlib import Path
p = Path('ExercisesXP.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
print('keys=', list(nb.keys()))
print('cells type=', type(nb['cells']))
print('cells count=', len(nb['cells']))
print('first cell keys=', sorted(nb['cells'][0].keys()))
