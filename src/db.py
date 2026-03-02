import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env local (se existir)
load_dotenv()

def get_postgres_uri() -> str:
    """Retorna a URI de conexão lida do ambiente."""
    uri = os.getenv("POSTGRES_URI")
    if not uri:
        raise ValueError("A variável de ambiente 'POSTGRES_URI' não está definida.")
    return uri

def get_engine():
    """Cria e retorna o SQLAlchemy Engine configurado para se conectar à base."""
    db_url = get_postgres_uri()
    try:
        engine = create_engine(db_url)
        # Testar a conexão
        with engine.connect() as conn:
            pass
        return engine
    except SQLAlchemyError as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return None
