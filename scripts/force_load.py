import os
import io
import sys
import pandas as pd

sys.path.append(r'C:\Users\Diego\.gemini\antigravity\scratch\solution_olist')
from src.db import get_engine
from src.models import Base

DATA_DIR = r'C:\Users\Diego\.gemini\antigravity\scratch\solution_olist\data'
FILE_TABLE_MAP = {
    'dataset_olist_customers.csv': 'customers',
    'dataset_olist_geolocation_csv.csv': 'geolocation',
    'dataset_olist_order_items.csv': 'order_items',
    'dataset_olist_order_payments.csv': 'order_payments',
    'dataset_olist_order_reviews.csv': 'order_reviews',
    'dataset_olist_orders.csv': 'orders',
    'dataset_olist_products.csv': 'products',
    'dataset_olist_sellers.csv': 'sellers',
    'dataset_product_category_name_translation.csv': 'product_category_name_translation'
}

engine = get_engine()
raw_conn = engine.raw_connection()

try:
    with raw_conn.cursor() as cur:
        for file_name, table_name in FILE_TABLE_MAP.items():
            file_path = os.path.join(DATA_DIR, file_name)
            if not os.path.exists(file_path): 
                continue
            
            print(f'Ingerindo {table_name}...')
            # Limpa antes para evitar conflito
            cur.execute(f'TRUNCATE TABLE {table_name} CASCADE;')
            
            delimiter = ';' if 'geolocation' in file_name else ','
            df = pd.read_csv(file_path, delimiter=delimiter)
            
            # Tratamento Extremo para evitar o erro "40.0" num campo Integer 
            # 1. Troca explicitamente todo o DataFrame pra String
            df = df.astype(str)
            # 2. Pandas transforma Null numa string literal "nan". Corrigimos pra flag de Nulo do Postgres '\N'
            df.replace('nan', '\\N', inplace=True)
            df.replace('\\n', ' ', regex=True, inplace=True)
            
            # 3. Remover a maldita casa decimal '.0' residual do float convertida pra string
            if table_name == 'products':
                for col in ['product_name_lenght', 'product_description_lenght', 'product_photos_qty', 'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']:
                    df[col] = df[col].str.replace(r'\.0$', '', regex=True)
            
            output = io.StringIO()
            df.to_csv(output, sep='|', header=False, index=False, na_rep='\\N')
            output.seek(0)
            
            cur.copy_expert(f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER '|', NULL '\\N')", output)
            
        raw_conn.commit()
        print('SUCESSO TOTAL INGESTAO!')
except Exception as e:
    raw_conn.rollback()
    print(f'FALHOU: {e}')
finally:
    raw_conn.close()
