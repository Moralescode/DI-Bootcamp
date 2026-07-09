import json
from pathlib import Path
p = Path('ExercisesXP.ipynb')
nb = json.loads(p.read_text(encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code' and 'id' not in c:
        print('missing id in code cell', i, 'execution_count', c.get('execution_count'), 'first line', repr(c.get('source')[0] if c.get('source') else ''))
