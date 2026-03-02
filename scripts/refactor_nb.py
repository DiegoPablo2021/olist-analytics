import json
import re

nb_path = 'C:/Users/Diego/.gemini/antigravity/scratch/solution_olist/solution.ipynb'
try:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. Manter a introdução
    original_cells = nb.get('cells', [])
    new_cells = [original_cells[0]]

    # 2. Inserir a célula de configuração refatorada
    new_code_cell = {
       'cell_type': 'code',
       'execution_count': 1,
       'metadata': {},
       'outputs': [],
       'source': [
        "import sys\n",
        "import os\n",
        "sys.path.append(os.path.dirname(os.path.abspath('')))\n",
        "from src.db import get_engine, get_postgres_uri\n",
        "\n",
        "engine = get_engine()\n",
        "postgres_uri = get_postgres_uri()\n",
        "%load_ext sql\n",
        "%config SqlMagic.style = '_DEPRECATED_DEFAULT'\n",
        "%sql {postgres_uri}\n"
       ]
    }
    
    new_cells.append(new_code_cell)
    
    # 3. Filtrar as células de infraestrutura e limpeza (ETL) que agora estão nos scripts python
    for cell in original_cells[1:]:
        source = "".join(cell.get('source', []))
        
        if cell['cell_type'] == 'code':
            if 'CREATE TABLE' in source or 'COPY ' in source or 'DELETE FROM' in source:
                continue
            if 'SELECT *' in source and 'WHERE' in source and 'IS NULL' in source:
                continue
            if 'create_engine' in source or 'load_dotenv' in source or 'connect_database(' in source:
                 continue
            if '%load_ext sql' in source or '%config SqlMagic' in source or '%sql {postgres_uri}' in source:
                 continue
                 
        if cell['cell_type'] == 'markdown':
             # Títulos que não fazem mais sentido
             if 'Importando as libs' in source or 'Carregando a configuração' in source or 'Limpeza' in source or 'ETL ' in source:
                 continue
                 
        new_cells.append(cell)

    nb['cells'] = new_cells

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    
    print('Notebook atualizado com sucesso.')
except Exception as e:
    print(f'Erro gerando notebook: {e}')
