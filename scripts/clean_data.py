import os
import sys

# Adiciona a raiz do projeto no PYTHONPATH para importar o src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import get_engine
from sqlalchemy import text

def clean_data(engine):
    """Executa a limpeza das tabelas substituindo a área interativa do Jupyter por scripts reprodutíveis."""
    
    queries = [
        # Remove duplicados na tabela Customers
        """
        WITH ranked_customers AS (
          SELECT customer_id,
                 ROW_NUMBER() OVER (
                   PARTITION BY customer_unique_id, customer_zip_code_prefix, customer_city, customer_state
                   ORDER BY customer_id
                 ) AS rn
          FROM customers
        )
        DELETE FROM customers
        WHERE customer_id IN (
          SELECT customer_id
          FROM ranked_customers
          WHERE rn > 1
        );
        """,
        
        # Remove Produtos sem Categoria Traduzível
        """
        DELETE FROM products
        WHERE product_id IN (
          SELECT product_id
          FROM products
          WHERE product_category_name IS NULL
        );
        """
    ]
    
    print("Iniciando limpeza de dados (ETL)...")
    try:
        with engine.begin() as conn: # engine.begin() abre uma transação que dá commit automático no final
            for i, sql in enumerate(queries, 1):
                result = conn.execute(text(sql))
                print(f"Query {i} executada. Linhas afetadas: {result.rowcount}")
        print("Limpeza de dados concluída!")
    except Exception as e:
        print(f"Ocorreu um erro durante a limpeza: {e}")

if __name__ == "__main__":
    engine = get_engine()
    if engine:
        clean_data(engine)
