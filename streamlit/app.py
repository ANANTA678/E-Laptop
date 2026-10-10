# run -->  python -m streamlit run "C:\Users\ekta panchbhai\OneDrive\Desktop\Python\streamlit\app.py"            
# --> pip install streamlit pandas numpy plotly statsmodels openpyxl

import streamlit as st
import pandas as pd

data = pd.read_csv(r"C:\Users\ekta panchbhai\OneDrive\Desktop\Python\sales 1.csv")
st.line_chart(data["Revenue"])

st.write("Streamlit is running!")

st.title("My First Streamlit App")


import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# App title
st.title("📊 My Sales Dashboard")
st.write("Sales analysis using Pandas and Streamlit")

# 1. Create your own data using a DataFrame
data = {
    "Month": [
        "Jan", "Feb", "Mar", "Apr", "May",
        "Jun", "Jul", "Aug", "Sep", "Oct",
        "Nov", "Dec"
    ],
    "Sales": [
        10000, 15000, 12000, 20000, 25000,
        22000, 30000, 28000, 35000, 40000,
        45000, 50000
    ],
    "Profit": [
        2000, 3000, 2500, 5000, 6000,
        5500, 8000, 7500, 9000, 11000,
        12000, 15000
    ]
}

df = pd.DataFrame(data)

# 2. Display the DataFrame
st.subheader("📋 Sales Data")
st.dataframe(df, use_container_width=True)

# 3. Display summary metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{df['Sales'].sum():,}")
col2.metric("Total Profit", f"₹{df['Profit'].sum():,}")
col3.metric("Average Sales", f"₹{df['Sales'].mean():,.0f}")

st.divider()

# 4. Line chart
st.subheader("📈 Monthly Sales Line Chart")

line_df = df.set_index("Month")[["Sales", "Profit"]]
st.line_chart(line_df)

# 5. Bar chart
st.subheader("📊 Monthly Sales Bar Chart")

bar_df = df.set_index("Month")[["Sales", "Profit"]]
st.bar_chart(bar_df)

# 6. Pie chart
st.subheader("🥧 Sales Distribution Pie Chart")

pie_df = df.set_index("Month")[["Sales"]]
st.subheader("Sales Share by Month")
st.vega_lite_chart(
    df,
    {
        "mark": {"type": "arc", "tooltip": True},
        "encoding": {
            "theta": {
                "field": "Sales",
                "type": "quantitative"
            },
            "color": {
                "field": "Month",
                "type": "nominal",
                "sort": None
            },
            "tooltip": [
                {"field": "Month", "type": "nominal"},
                {"field": "Sales", "type": "quantitative"}
            ]
        },
        "view": {"stroke": None}
    },
    use_container_width=True
)

# 7. Footer
st.divider()
st.write("Built with Python, Pandas, and Streamlit.")




import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Complete Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# 2. CREATE YOUR OWN DATAFRAME
# ==================================================
@st.cache_data
def create_data():

    np.random.seed(42)

    n = 200

    dates = pd.date_range(
        start="2025-01-01",
        periods=n,
        freq="D"
    )

    categories = [
        "Electronics",
        "Clothing",
        "Furniture",
        "Grocery"
    ]

    regions = [
        "North",
        "South",
        "East",
        "West"
    ]

    products = [
        "Laptop",
        "Mobile",
        "Shirt",
        "Table",
        "Chair",
        "Rice",
        "Headphones",
        "Shoes"
    ]

    df = pd.DataFrame({
        "Order_ID": range(1001, 1001 + n),
        "Date": dates,
        "Product": np.random.choice(products, n),
        "Category": np.random.choice(categories, n),
        "Region": np.random.choice(regions, n),
        "Quantity": np.random.randint(1, 11, n),
        "Unit_Price": np.random.randint(500, 20001, n),
        "Customer_Age": np.random.randint(18, 61, n)
    })

    # Calculated columns
    df["Sales"] = df["Quantity"] * df["Unit_Price"]

    df["Profit"] = (
        df["Sales"] * np.random.uniform(0.05, 0.30, n)
    ).round(2)

    df["Profit_Margin"] = (
        df["Profit"] / df["Sales"] * 100
    ).round(2)

    return df


df = create_data()

# ==================================================
# 3. DASHBOARD TITLE
# ==================================================
st.title("📊 Complete Data Analysis Dashboard")

st.write(
    "Explore DataFrame information, data cleaning, "
    "statistics, filtering, KPIs, and interactive charts."
)

st.divider()

# ==================================================
# 4. SIDEBAR FILTERS
# ==================================================
st.sidebar.header("🔎 Dashboard Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter DataFrame
filtered_df = df[
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
].copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["Date"].dt.date.between(
            start_date, end_date
        )
    ]

# ==================================================
# 5. KPI METRICS
# ==================================================
st.header("1. Business Summary")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
average_sales = filtered_df["Sales"].mean()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Average Sales", f"₹{average_sales:,.0f}")
c5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.caption(
    f"Showing {len(filtered_df):,} records "
    f"out of {len(df):,} total records."
)

st.divider()

# ==================================================
# 6. DATAFRAME PRESENTATION
# ==================================================
st.header("2. DataFrame Presentation")

tab1, tab2, tab3, tab4 = st.tabs([
    "Dataset",
    "Head & Tail",
    "Shape & Columns",
    "Data Types"
])

with tab1:
    st.subheader("Complete DataFrame")
    st.dataframe(filtered_df, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("First 5 Rows — head()")
        st.dataframe(filtered_df.head())

    with col2:
        st.subheader("Last 5 Rows — tail()")
        st.dataframe(filtered_df.tail())

with tab3:
    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", filtered_df.shape[0])
    col2.metric("Columns", filtered_df.shape[1])
    col3.metric(
        "Total Cells",
        filtered_df.shape[0] * filtered_df.shape[1]
    )

    st.subheader("Column Names")
    st.write(filtered_df.columns.tolist())

    st.subheader("DataFrame Shape")
    st.code(f"Shape: {filtered_df.shape}")

with tab4:
    st.subheader("Column Data Types")

    dtype_df = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str).values,
        "Non-Null Count": filtered_df.notna().sum().values,
        "Missing Count": filtered_df.isna().sum().values
    })

    st.dataframe(dtype_df, use_container_width=True)

    st.subheader("DataFrame Info")
    st.text(
        f"Rows: {filtered_df.shape[0]}\n"
        f"Columns: {filtered_df.shape[1]}\n"
        f"Memory Usage: "
        f"{filtered_df.memory_usage(deep=True).sum():,} bytes"
    )

st.divider()

# ==================================================
# 7. STATISTICAL ANALYSIS
# ==================================================
st.header("3. Statistical Analysis")

st.subheader("Descriptive Statistics — describe()")

st.dataframe(
    filtered_df.describe().round(2),
    use_container_width=True
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Numerical Column Summary")

    numeric_cols = filtered_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_cols:
        selected_numeric = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        series = filtered_df[selected_numeric]

        stats_df = pd.DataFrame({
            "Statistic": [
                "Mean",
                "Median",
                "Mode",
                "Minimum",
                "Maximum",
                "Standard Deviation",
                "Variance",
                "Sum",
                "Unique Values"
            ],
            "Value": [
                series.mean(),
                series.median(),
                series.mode().iloc[0] if not series.mode().empty else np.nan,
                series.min(),
                series.max(),
                series.std(),
                series.var(),
                series.sum(),
                series.nunique()
            ]
        })

        st.dataframe(stats_df, use_container_width=True)

with col2:
    st.subheader("Category Counts — value_counts()")

    categorical_cols = filtered_df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if categorical_cols:
        selected_category = st.selectbox(
            "Select Category Column",
            categorical_cols
        )

        counts = filtered_df[
            selected_category
        ].value_counts().rename_axis(
            selected_category
        ).reset_index(name="Count")

        st.dataframe(counts, use_container_width=True)

st.divider()

# ==================================================
# 8. DATA QUALITY AND CLEANING
# ==================================================
st.header("4. Data Quality & Cleaning")

missing_count = filtered_df.isna().sum().sum()
duplicate_count = filtered_df.duplicated().sum()

c1, c2, c3 = st.columns(3)

c1.metric("Missing Values", f"{missing_count:,}")
c2.metric("Duplicate Rows", f"{duplicate_count:,}")
c3.metric(
    "Unique Orders",
    f"{filtered_df['Order_ID'].nunique():,}"
)

st.subheader("Missing Values by Column")
missing_df = filtered_df.isna().sum().reset_index()
missing_df.columns = ["Column", "Missing Values"]
st.dataframe(missing_df, use_container_width=True)

st.subheader("Duplicate Records")
st.write("Number of duplicate rows:", duplicate_count)

if duplicate_count > 0:
    st.dataframe(filtered_df[filtered_df.duplicated()])
else:
    st.success("No duplicate rows found in the filtered data.")

st.subheader("Cleaned Data Preview")

clean_df = filtered_df.drop_duplicates().dropna().copy()

st.write(
    f"Original filtered rows: {len(filtered_df)} | "
    f"Rows after cleaning: {len(clean_df)}"
)

st.dataframe(clean_df, use_container_width=True)

st.divider()

# ==================================================
# 9. SALES LINE CHART
# ==================================================
st.header("5. Sales Trend Analysis")

if not filtered_df.empty:
    daily_sales = (
        filtered_df.groupby("Date", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    fig_line = px.line(
        daily_sales,
        x="Date",
        y=["Sales", "Profit"],
        title="Daily Sales and Profit Trend",
        markers=True
    )

    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("No records match the selected filters.")

st.divider()

# ==================================================
# 10. BAR CHART
# ==================================================
st.header("6. Category-wise Sales")

if not filtered_df.empty:
    category_sales = (
        filtered_df.groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    fig_bar = px.bar(
        category_sales,
        x="Category",
        y=["Sales", "Profit"],
        barmode="group",
        title="Sales and Profit by Category",
        text_auto=".2s"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ==================================================
# 11. PIE CHART
# ==================================================
st.header("7. Sales Distribution")

if not filtered_df.empty:
    region_sales = (
        filtered_df.groupby("Region", as_index=False)
        ["Sales"].sum()
    )

    fig_pie = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales Share by Region",
        hole=0.35
    )

    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ==================================================
# 12. SCATTER PLOT
# ==================================================
st.header("8. Relationship Between Sales and Profit")

if not filtered_df.empty:
    fig_scatter = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Product", "Region", "Date"],
        title="Sales vs Profit",
        trendline="ols"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ==================================================
# 13. HISTOGRAM
# ==================================================
st.header("9. Sales Distribution Histogram")

if not filtered_df.empty:
    fig_hist = px.histogram(
        filtered_df,
        x="Sales",
        nbins=20,
        title="Frequency Distribution of Sales",
        marginal="box"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# ==================================================
# 14. REGION-WISE ANALYSIS
# ==================================================
st.header("10. Region-wise Performance")

if not filtered_df.empty:
    region_summary = (
        filtered_df.groupby("Region", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum"),
            Total_Orders=("Order_ID", "nunique")
        )
    )

    region_summary["Profit_Margin"] = (
        region_summary["Total_Profit"]
        / region_summary["Total_Sales"] * 100
    ).round(2)

    st.dataframe(
        region_summary.sort_values(
            "Total_Sales", ascending=False
        ),
        use_container_width=True
    )

    fig_region = px.bar(
        region_summary,
        x="Region",
        y="Total_Sales",
        color="Region",
        title="Total Sales by Region",
        text_auto=".2s"
    )

    st.plotly_chart(fig_region, use_container_width=True)

st.divider()

# ==================================================
# 15. TOP PRODUCTS
# ==================================================
st.header("11. Top Performing Products")

if not filtered_df.empty:
    top_products = (
        filtered_df.groupby("Product", as_index=False)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum")
        )
        .sort_values("Total_Sales", ascending=False)
        .head(10)
    )

    st.dataframe(top_products, use_container_width=True)

    fig_top = px.bar(
        top_products.sort_values("Total_Sales"),
        x="Total_Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Sales",
        text_auto=".2s"
    )

    st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# ==================================================
# 16. INTERACTIVE DATA FILTERING
# ==================================================
st.header("12. Interactive Data Filtering")

if not filtered_df.empty:
    search_text = st.text_input(
        "Search Product Name",
        placeholder="Enter a product name..."
    )

    min_sales = float(filtered_df["Sales"].min())
    max_sales = float(filtered_df["Sales"].max())

    sales_range = st.slider(
        "Select Sales Range",
        min_value=min_sales,
        max_value=max_sales,
        value=(min_sales, max_sales)
    )

    search_df = filtered_df[
        filtered_df["Sales"].between(
            sales_range[0], sales_range[1]
        )
    ]

    if search_text:
        search_df = search_df[
            search_df["Product"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    st.write("Filtered Records:", len(search_df))
    st.dataframe(search_df, use_container_width=True)
else:
    st.info("No records available for interactive filtering.")

st.divider()

# ==================================================
# 17. DOWNLOAD DATA
# ==================================================
st.header("13. Download Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="sales_dashboard_data.csv",
    mime="text/csv"
)

st.download_button(
    label="⬇️ Download Cleaned Data as CSV",
    data=clean_df.to_csv(index=False).encode("utf-8"),
    file_name="cleaned_sales_data.csv",
    mime="text/csv"
)

st.divider()

# ==================================================
# 18. FOOTER
# ==================================================
st.success("Dashboard analysis completed successfully.")

st.caption(
    "Built using Python, Pandas, NumPy, Plotly, and Streamlit."
)


