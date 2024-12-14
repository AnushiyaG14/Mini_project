# streamlit_app.py
import streamlit as st
import pg8000
import pandas as pd
# Function to connect to the PostgreSQL databas
def get_db_connection():
    conn = pg8000.connect(
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
ques=["Home",
"1.# Find top 10 highest revenue generating products",
"2.# Find the top 5 cities with the highest profit margins",
"3.# Calculate the total discount given for each category",
"4.# Find the average sale price per product category",
"5.# Find the region with the highest average sale price",
"6.# Find the total profit per category",
"7.# Identify the top 3 segments with the highest quantity of orders",
"8.# Determine the average discount percentage given per region",
"9.# Find the product category with the highest total profit",
"10.# Calculate the total revenue generated per year",
"11.#Join to Fetch Complete Order Details",
"12.#Calculate Total Revenue per Order",
"13.#Calculate Total profit per Order",
"14.#Least Revenue generating products",
"15.#Count Orders by Region",
"16.#Calculate Average Discount by state",
"17.#Calculate the total revenue generated on December month",
"18.#Region with the Highest Profit",
"19.#Identify Orders with No Profit (Profit = 0)",
"20.#Most Frequently Ordered Product Category"
]

queries=[
"SELECT 'Welcome' AS Message;"
#Query1
"select c.sub_category as product,sum(p.sales_price * p.quantity) as Top_10_Revenue from order_ret1 as c join order_ret2 as p on c.order_id = p.id group by c.sub_category order by Top_10_Revenue DESC limit 10;",
#Query2
"select c.city, avg(case when sales_price = 0 then 0 else ((p.profit/p.sales_price)* 100) end) as profit_margin from order_ret1 as c join order_ret2 as p on c.order_id=p.id group by c.city order by profit_margin desc limit 5;",
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
"select c.state, avg(p.discount_percent) as avg_discount from order_ret1 as c join order_ret2 as p on c.order_id=p.id group by c.state;",
 #Query17 Calculate the total revenue generated on December month
"select extract(Month from c.order_date) as Month, sum((p.sales_price)*p.quantity) as TotalRevenue from order_ret2 as p, order_ret1 as c group by  extract(Month from c.order_date) order by Month;",
#Query18 Region with the Highest Profit*************/
"select c.region,sum((p.sales_price-p.cost_price)*p.quantity) as highest_profit from order_ret2 as p, order_ret1 as c group by c.region order by highest_profit desc limit 1;",
#Query19 Identify Orders with No Profit (Profit = 0)
 "select c.order_id,(p.sales_price - p.cost_price)*quantity as profit from order_ret2 as p join order_ret1 as c on c.order_id=p.id where  (p.sales_price - p.cost_price)*quantity=0;",
#Query20 Most Frequently Ordered Product Category********/
"SELECT c.category, count(p.id) AS OrderCount FROM order_ret1 as c JOIN order_ret2 as p ON c.order_id = p.id GROUP BY c.category ORDER BY OrderCount DESC LIMIT 1;"

]

st.title("PostgreSQL Query Result!",)
st.sidebar.title("Select your Query here !")

query_description = st.sidebar.selectbox("Choose a query to run:", ques)
query_index = ques.index(query_description)
selected_query = queries[query_index]

if query_index == 0:  # If "Home" is selected
    st.header("Welcome!")
    st.write(
        "This dashboard provides insights into retail order data, including sales, profits, discounts, and more. "
        "Navigate through the sidebar to explore specific analyses."
    )
else:
    st.subheader(f"Selected Query: {query_description}")
    if st.sidebar.button("Submit Query",type="secondary"):
        try:
            result_df = run_query(selected_query)
            if result_df is not None:
                st.dataframe(result_df)  # Display the result
            else:
                st.error("Query execution failed.")
        except Exception as e:
             st.error(f"Error executing query: {e}")

### Sidebar for Navigation
st.sidebar.title("Business insights of Retail Order Data Analysis  !")
page = st.sidebar.selectbox("Go to", ["Home", "Top Selling Products", "Year over Year sales Analysis", "Product Performance","Regional Sales Analysis","Discount Analysis"])

# Main App Logic###
if page == "Home":
    st.title("Business insights of Retail Order Data Analysis  !")
    
elif page == "Top Selling Products":
    st.title("Top Selling Products")
    st.image("/workspaces/Mini_project/image/Capture1.PNG","Caption = Top 10 Revenue generating products")
elif page == "Year over Year sales Analysis":
    st.title("Year over Year sales Analysis")
    st.image("/workspaces/Mini_project/image/capture2.png", "Caption = Yearly Sales Analysis")
    st.image("/workspaces/Mini_project/image/Capture2.PNG","Caption = Monthly sales Analysis ")
elif page == "Product Performance":
    st.title("Product Performance")
    st.image("/workspaces/Mini_project/image/Capture1.PNG", "caption = Product rank by Revenue basis")
    
elif page == "Regional Sales Analysis":
    st.title("Regional Sales Analysis")
    st.image("/workspaces/Mini_project/image/Capture3.png","caption =Regional Sales Analysis ")
elif page == "Discount Analysis":
    st.title("Discount Analysis")
    st.image("/workspaces/Mini_project/image/Capture5.PNG","caption = Product with greater than 20 % disscount ")

st.text("Thank you")
