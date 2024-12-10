
# streamlit_app.py

import streamlit as st
import psycopg2
import pandas as pd

# Function to connect to the PostgreSQL databas
def get_db_connection():
    conn = psycopg2.connect(
       host="dsanudb.cl44kq2oiq5z.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="Mini_project",
        user="postgres",
        password="rootanu123"
    )
    return conn
    
# Function to execute a query and return the result as a pandas DataFrame
def run_query(query):
    conn = get_db_connection()
    if conn is None:
        return None  # Return None if connection failed
    
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

queries=[
#Query1
"select c.sub_category as product,sum(p.sales_price * p.quantity) as Top_10_Revenue from order_ret1 as c join order_ret2 as p on c.order_id = p.id group by c.sub_category order by Top_10_Revenue DESC limit 10;",
#Query2
"select c.city, avg(case when sales_price = 0 then 0 else ((p.profit/p.sales_price)* 100) end) as profit_margin from order_ret1 as c, order_ret2 as p group by c.city order by profit_margin desc limit 5;",
#Query3
 "select c.category, sum(p.discount) as total_discount from order_ret1 as c, order_ret2 as p group by c.category;",
#Query4
 "select c.category, avg(p.sales_price) as avg_sales_price from order_ret1 as c join order_ret2 as p on c.order_id=p.id group by c.category;",
#Query5
"select c.region,(sum(p.sales_price * p.quantity)/sum(p.quantity))as highest_average_salesprice from order_ret2 as p, order_ret1 as c group by c.region order by highest_average_Salesprice desc limit 1;",
#Query 6
"select c.category, sum((p.sales_price-p.cost_price)*p.quantity) as total_profit from order_ret2 as p, order_ret1 as c group by c.category;",
#Query 7
 "select c.segment, sum(p.quantity) as highest_quantity from order_ret2 as p, order_ret1 as c group by c.segment order by highest_quantity desc limit 3;",
#Query 8
"select c.region,avg(p.discount_percent) as avg_discount_percentage from order_ret1 as c join order_ret2 as p on c.order_id=p.id group by c.region;",
#Query 9
" select c.category,sum(p.profit) as total_profit from order_ret2 as p, order_ret1 as c group by c.category order by total_profit desc;",
#Query10
 "select extract(Year from c.order_date) as Year, sum((p.sales_price)*p.quantity) as TotalRevenue from order_ret2 as p, order_ret1 as c group by  extract(Year from c.order_date) order by Year;",
#Query11 Join to Fetch Complete Order Details*******/
"SELECT c.order_id, c.order_date, c.Region,p.cost_price,p.sales_price, p.quantity, p.discount_percent FROM order_ret1 as c JOIN order_ret2 as p ON c.order_id = p.id;",
#Query12 Calculate Total Revenue per Order*******/ 
"select c.order_id, sum(p.sales_price *p.quantity)as total_revenue from order_ret1 as c join order_ret2 as p on c.order_id=p.id group by c.order_id;",
 #Query13 Calculate Total profit per Order
"select c.order_id, sum((p.sales_price - p.cost_price)*p.quantity)as total_profit from order_ret1 as c join order_ret2 as p on c.order_id=p.id group by c.order_id;",
 #Query14 Least Revenue generating products
"select c.sub_category as product,sum(p.sales_price * p.quantity) as least_Revenue from order_ret1 as c, order_ret2 as p group by c.sub_category order by least_Revenue asc limit 10;",
#Query 15 Count Orders by Region
 "select region, sum(order_id) as count_orders from order_ret1 group by region;",
#Query16 Calculate Average Discount by state 
"select c.state, avg(p.discount_percent) as avg_discount from order_ret1 as c, order_ret2 as p group by c.state;",
 #Query17 Calculate the total revenue generated on December month 
"select extract(Month from c.order_date) as Month, sum((p.sales_price)*p.quantity) as TotalRevenue from order_ret2 as p, order_ret1 as c group by  extract(Month from c.order_date) order by Month;",
#Query18 Region with the Highest Profit*************/													
"select c.region,sum((p.sales_price-p.cost_price)*p.quantity) as highest_profit from order_ret2 as p, order_ret1 as c group by c.region order by highest_profit desc limit 1;",
#Query19 Identify Orders with No Profit (Profit = 0)
 "select c.order_id,(p.sales_price - p.cost_price)*quantity as profit from order_ret2 as p join order_ret1 as c on c.order_id=p.id where  (p.sales_price - p.cost_price)*quantity=0;",
#Query20 Most Frequently Ordered Product Category********/
"SELECT c.category, count(p.id) AS OrderCount FROM order_ret1 as c JOIN order_ret2 as p ON c.order_id = p.id GROUP BY c.category ORDER BY OrderCount DESC LIMIT 1;"
]

# Streamlit UI
st.title("PostgreSQL Queries Results")
st.subheader("1-10 Query by GUVI")
st.subheader("11-20 My Queries")
for i, query in enumerate(queries, start=1):
    st.subheader(f"Query {i}")
    st.text(query)  # Show the query
    try:
        result_df = run_query(query)
        if result_df is not None:
             st.dataframe(result_df)  # Show the result as a dataframe
        else:
            st.error(f"Query {i} failed to execute.")
    except Exception as e:
        st.error(f"Error running query {i}: {e}")

st.text("Thank you")
