import os
import sys

# Adiciona a raiz do projeto no PYTHONPATH para importar o src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db import get_engine
from sqlalchemy import text

def deploy_kpi_views(engine):
    """Cria Views otimizadas no banco de forma idempotente para o Power BI"""
    
    views_sql = [
        # 1. Resumo Vendas Gerais
        """
        CREATE OR REPLACE VIEW vw_kpi_vendas_gerais AS
        SELECT 
            DATE_TRUNC('month', o.order_purchase_timestamp) AS mes_venda,
            COUNT(DISTINCT o.order_id) AS total_pedidos,
            SUM(op.payment_value) AS faturamento_total,
            AVG(op.payment_value) AS ticket_medio,
            SUM(oi.freight_value) AS receita_frete
        FROM orders o
        LEFT JOIN order_payments op ON o.order_id = op.order_id
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY DATE_TRUNC('month', o.order_purchase_timestamp)
        ORDER BY mes_venda;
        """,
        
        # 2. Vendas por Categoria e Produto
        """
        CREATE OR REPLACE VIEW vw_vendas_por_categoria AS
        SELECT 
            t.product_category_name_english AS categoria_produto,
            COUNT(oi.product_id) AS quantidade_produtos_vendidos,
            SUM(oi.price) AS total_receita_produtos
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
        GROUP BY t.product_category_name_english
        ORDER BY total_receita_produtos DESC;
        """,
        
        # 3. Análise Logística (Em dias)
        """
        CREATE OR REPLACE VIEW vw_performance_logistica AS
        SELECT 
            order_id,
            order_status,
            order_purchase_timestamp,
            order_delivered_customer_date,
            order_estimated_delivery_date,
            EXTRACT(EPOCH FROM (order_delivered_customer_date - order_purchase_timestamp))/86400 AS dias_para_entrega,
            EXTRACT(EPOCH FROM (order_estimated_delivery_date - order_delivered_customer_date))/86400 AS saldo_dias_estimativa,
            CASE 
                WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 'Atrasado'
                ELSE 'No Prazo'
            END AS status_entrega
        FROM orders
        WHERE order_status = 'delivered' AND order_delivered_customer_date IS NOT NULL;
        """,
        
        # 4. Satisfação do Cliente (NPS Proxy)
        """
        CREATE OR REPLACE VIEW vw_satisfacao_clientes AS
        SELECT 
            rv.review_score,
            COUNT(rv.review_id) AS quantidade_avaliacoes,
            ROUND(COUNT(rv.review_id) * 100.0 / SUM(COUNT(rv.review_id)) OVER(), 2) AS percentual_total
        FROM order_reviews rv
        GROUP BY rv.review_score
        ORDER BY rv.review_score DESC;
        """
    ]
    
    print("Iniciando o Deploy das Views Analíticas de Negócio...")
    try:
        with engine.begin() as conn: # engine.begin() abre transação e faz commit no final
            for i, sql in enumerate(views_sql, 1):
                conn.execute(text(sql))
                print(f"View {i} criada com sucesso!")
        print("Todas as Views construídas! O Power BI agora pode consultar essas tabelas virtuais prontas.")
    except Exception as e:
        print(f"Ocorreu um erro durante a criação das Views: {e}")

if __name__ == "__main__":
    engine = get_engine()
    if engine:
        deploy_kpi_views(engine)
