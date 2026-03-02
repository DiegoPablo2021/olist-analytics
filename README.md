# 📊 Olist E-commerce Analytics & Data Engineering

<p align="center">
  <img src="assets/demo.webp" alt="Demonstração do Jupyter rodando ETL e queries SQL em tempo real" width="800">
</p>

Projeto de portfólio de ponta a ponta (End-to-End) focado na análise do dataset público de e-commerce da Olist Store Brasileira. O projeto engloba todas as etapas de um ciclo analítico moderno: Ingestão de Dados Automatizada (ETL/ELT), Modelagem de Data Warehouse (PostgreSQL) e Visualização de Negócios (Power BI).

## 🏗️ Arquitetura do Projeto

Este repositório materializa a evolução de um script simples de Jupyter Notebook analisando CSVs para uma infraestrutura de dados **escalável, automatizada e profissional**.

1. **`src/`** (Backend e Conectividade):
   - Módulos Python Orientados a Objetos (OOP).
   - Abstração de Banco de Dados via **SQLAlchemy ORM**, blindando o código de vulnerabilidades por meio de *Enviroment Variables* no arquivo `.env`.

2. **`scripts/`** (Pipeline de Dados / ETL):
   - **`force_load.py`**: Script de automação massiva que ingere milhões de linhas em arquivos brutos `.csv` para tabelas relacionais do PostgreSQL. A rotina lida nativamente com higienização de dados e *casting* seguro de inconsistências (NaN/Floats implícitos).
   - **`clean_data.py`**: Processo de higienização de integridade relacional.
   - **`deploy_views.py`**: Engenharia de Analytics que cria instâncias de *Data Marts* em SQL (Views pré-agregadas), otimizando a performance do dashboard.

3. **Análise e Visualização**:
   - **Jupyter Notebook (`solution.ipynb`)**: Totalmente refatorado. O código pesado transacional foi removido, transformando o arquivo em uma interface analítica imersiva focada na linguagem SQL pura (`ipython-sql`) para o Cientista de Dados.
   - **Dashboard Power BI (`dashboard/kpis_case.pbix`)**: Painel de BI estruturado com KPIs financeiros e operacionais executivos.

---

## 🚀 Como Iniciar (Setup)

### 1) Pré-requisitos
- Python 3.10+
- Servidor PostgreSQL ativo

**Configuração do Ambiente Virtual:**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2) Variáveis de Ambiente (.env)
Crie um arquivo chamado `.env` na raiz do projeto contendo as credenciais de sua base de dados alvo:
```ini
POSTGRES_URI=postgresql://usuario:senha@localhost:5432/olist_case_solution
```

### 3) Execução do Pipeline (ETL Automático)
Transforme os arquivos CSV brutos da pasta `data/` em um Data Warehouse populado com apenas os comandos abaixo:
```bash
# 1. Pipeline de Ingestão de Dados
python scripts/force_load.py

# 2. Construção do Back-end de Dashboards
python scripts/deploy_views.py
```

### 4) Análise e Resultados
Após a ingestão, os dados estão prontos e as arquiteturas analíticas se conectam nativamente:
- Abra o aplicativo **Power BI Desktop**, navegue para Obter Dados, e conecte o relatório executivo diretamente nas Views do PostgreSQL.
- Ou reproduza as explorações baseadas em Python subindo o serviço de visualização Jupyter:
  ```bash
  jupyter notebook solution.ipynb
  ```

---
*Arquitetura projetada visando boas práticas de Engenharia de Software focada em Dados, escalabilidade transacional no banco subjacente, e entrega executiva de ponta (Analytics).*
