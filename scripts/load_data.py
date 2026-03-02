import os
import io
import sys
import pandas as pd

# Adiciona a raiz do projeto no PYTHONPATH para importar o src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import get_engine
from src.models import Base

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

# Mapeamento arquivo -> tabela para facilitar o COPY
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

def create_tables(engine):
    """Cria todas as tabelas caso não existam."""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso.")

def load_csv_to_postgres(engine):
    """Lê os CSVs rápidos usando pandas e o comando COPY do psycopg2 sob o SQLAlchemy."""
    print("Iniciando ingestão de dados...")
    
    # Abrindo comunicação raw connection do psycopg2 a partir do SQLAlchemy
    raw_conn = engine.raw_connection()
    
    try:
        with raw_conn.cursor() as cur:
            for file_name, table_name in FILE_TABLE_MAP.items():
                file_path = os.path.join(DATA_DIR, file_name)
                
                if not os.path.exists(file_path):
                    print(f"Aviso: Arquivo {file_name} não encontrado no diretório data/. Pulando...")
                    continue
                
                print(f"Carregando {file_name} na tabela {table_name}...")
                
                # Ler com pandas apenas para lidar com o delimiter, que muda pro arquivo geolocation
                delimiter = ';' if 'geolocation' in file_name else ','
                
                # Exemplo simples carregando tudo em memória caso o arquivo caiba.
                # Se for muito massivo, ler em chunks ou mandar o COPY usando o path raw.
                # O COPY lendo do STDIN (io.StringIO) é muito rápido em Python + PostgreSQL
                df = pd.read_csv(file_path, delimiter=delimiter)
                
                # Limpa newline das strings 
                df = df.replace('\\n', ' ', regex=True)
                
                output = io.StringIO()
                # index=False evita de importar o indice autonumerico do CSV. header=False pq no COPY so usamos dados
                df.to_csv(output, sep='|', header=False, index=False, na_rep='\\N')
                output.seek(0)
                
                cur.copy_expert(f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER '|', NULL '\\N')", output)
                
            raw_conn.commit()
            print("Carga de dados finalizada com sucesso!")
            
    except Exception as e:
        raw_conn.rollback()
        print(f"Falha na carga de dados: {e}")
    finally:
        raw_conn.close()

if __name__ == "__main__":
    engine = get_engine()
    if engine:
        create_tables(engine)
        load_csv_to_postgres(engine)



