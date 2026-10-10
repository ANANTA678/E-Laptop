# RUN -->  python -m streamlit run "C:\Users\ekta panchbhai\OneDrive\Desktop\Python\streamlit\Sales.py"            
# RUN --> pip install streamlit pandas numpy plotly statsmodels openpyxl

# ============================================================
# SALES DATA ANALYSIS & DATA CLEANING DASHBOARD
# Using Python, Pandas, NumPy, Streamlit and Plotly
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Analysis Dashboard")
st.caption("Dataset Understanding | Data Cleaning | EDA | Visualization")

# ============================================================
# 2. LOAD YOUR DATASET
# ============================================================

FILE_PATH = r"C:\Users\ekta panchbhai\OneDrive\Desktop\Python\sales 1.csv"

st.sidebar.header("📂 Load Your Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file (optional)",
    type=["csv", "xlsx", "xls"]
)


def load_dataset(file):
    """Load a CSV or Excel dataset."""

    if file is not None:
        if file.name.lower().endswith(".csv"):
            return pd.read_csv(file)
        return pd.read_excel(file)

    return pd.read_csv(FILE_PATH)


try:
    original_df = load_dataset(uploaded_file)

    # Clean column-name spaces
    original_df.columns = original_df.columns.astype(str).str.strip()

    # Remove duplicate column names if any
    original_df = original_df.loc[
        :, ~original_df.columns.duplicated()
    ]

except FileNotFoundError:
    st.error(
        "Dataset not found. Check the file path or upload your CSV file."
    )
    st.code(FILE_PATH)
    st.stop()

except Exception as e:
    st.error(f"Unable to load the dataset: {e}")
    st.stop()


# ============================================================
# 3. STORE DATA IN SESSION STATE
# ============================================================

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = original_df.copy()

if "source_name" not in st.session_state:
    st.session_state.source_name = (
        uploaded_file.name if uploaded_file else FILE_PATH
    )

# Current working dataset
df = st.session_state.cleaned_df.copy()

# Ensure column names are strings
df.columns = df.columns.astype(str).str.strip()

st.sidebar.success("Dataset loaded successfully!")
st.sidebar.write(f"Rows: {df.shape[0]:,}")
st.sidebar.write(f"Columns: {df.shape[1]:,}")

if st.sidebar.button("🔄 Reset to Original Dataset"):
    st.session_state.cleaned_df = original_df.copy()
    st.rerun()

# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def get_numeric_columns(data):
    return data.select_dtypes(include=np.number).columns.tolist()


def get_categorical_columns(data):
    return data.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()


def get_date_columns(data):
    return [
        col for col in data.columns
        if "date" in col.lower()
    ]


# ============================================================
# 5. DASHBOARD TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview",
    "🔍 Data Understanding",
    "🧹 Data Quality",
    "🛠️ Data Cleaning",
    "📈 Analysis & Charts",
    "⬇️ Filter & Download"
])


# ============================================================
# TAB 1: OVERVIEW
# ============================================================

with tab1:

    st.header("Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Rows", f"{df.shape[0]:,}")
    col2.metric("Total Columns", f"{df.shape[1]:,}")
    col3.metric("Missing Values", f"{df.isna().sum().sum():,}")
    col4.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

    st.subheader("Dataset Preview")

    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Column Names")

    st.write(df.columns.tolist())

    st.subheader("Dataset Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non-Null Count": df.notna().sum().values,
        "Missing Count": df.isna().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(info_df, use_container_width=True)

    st.subheader("Numeric Summary")

    numeric_cols = get_numeric_columns(df)

    if numeric_cols:
        st.dataframe(
            df[numeric_cols].describe().T,
            use_container_width=True
        )
    else:
        st.info("No numeric columns found.")


# ============================================================
# TAB 2: DATA UNDERSTANDING
# ============================================================

with tab2:

    st.header("🔍 Explore Your Dataset")

    st.subheader("1. Select Rows")

    row_option = st.selectbox(
        "Choose a preview operation",
        [
            "Head",
            "Tail",
            "Random Sample",
            "Complete Dataset"
        ]
    )

    number_of_rows = st.number_input(
        "Number of rows",
        min_value=1,
        max_value=max(1, len(df)),
        value=min(5, max(1, len(df)))
    )

    if row_option == "Head":
        st.dataframe(
            df.head(int(number_of_rows)),
            use_container_width=True
        )

    elif row_option == "Tail":
        st.dataframe(
            df.tail(int(number_of_rows)),
            use_container_width=True
        )

    elif row_option == "Random Sample":
        st.dataframe(
            df.sample(
                n=min(int(number_of_rows), len(df)),
                random_state=42
            ),
            use_container_width=True
        )

    else:
        st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("2. Shape, Columns and Data Types")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Shape (rows, columns)**")
        st.write(df.shape)

        st.write("**Column names**")
        st.write(df.columns.tolist())

    with col2:
        st.write("**Data types**")
        st.dataframe(
            df.dtypes.astype(str).rename("Data Type"),
            use_container_width=True
        )

    st.divider()

    st.subheader("3. Unique Values and Value Counts")

    selected_column = st.selectbox(
        "Select a column",
        df.columns,
        key="unique_column"
    )

    st.write("**Unique values:**")
    st.write(df[selected_column].unique().tolist())

    st.write(
        f"**Number of unique values:** "
        f"{df[selected_column].nunique(dropna=True)}"
    )

    st.write("**Value counts:**")

    value_counts = (
        df[selected_column]
        .value_counts(dropna=False)
        .rename_axis(selected_column)
        .reset_index(name="Count")
    )

    st.dataframe(value_counts, use_container_width=True)

    st.subheader("4. Memory Usage")

    memory_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)

    st.metric("Approximate Memory Usage", f"{memory_usage:.2f} MB")


# ============================================================
# TAB 3: DATA QUALITY
# ============================================================

with tab3:

    st.header("🧹 Data Quality Report")

    st.subheader("1. Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Missing Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    missing_df = missing_df.sort_values(
        "Missing Values",
        ascending=False
    )

    st.dataframe(missing_df, use_container_width=True)

    missing_only = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if not missing_only.empty:
        fig = px.bar(
            missing_only,
            x="Column",
            y="Missing Values",
            title="Missing Values by Column"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No missing values found.")

    st.divider()

    st.subheader("2. Duplicate Rows")

    duplicate_count = df.duplicated().sum()

    st.metric("Duplicate Rows", int(duplicate_count))

    if duplicate_count > 0:
        st.write("Preview of duplicate rows:")
        st.dataframe(
            df[df.duplicated(keep=False)].head(20),
            use_container_width=True
        )

    st.divider()

    st.subheader("3. Blank or Empty Strings")

    blank_counts = {}

    for col in get_categorical_columns(df):
        blank_counts[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .eq("")
            .fillna(False)
            .sum()
        )

    if blank_counts:
        blank_df = pd.DataFrame({
            "Column": list(blank_counts.keys()),
            "Blank Strings": list(blank_counts.values())
        })

        st.dataframe(blank_df, use_container_width=True)
    else:
        st.info("No text columns available to check.")

    st.divider()

    st.subheader("4. Numeric Outlier Detection (IQR)")

    numeric_cols = get_numeric_columns(df)

    if numeric_cols:

        outlier_column = st.selectbox(
            "Select numeric column",
            numeric_cols,
            key="outlier_column"
        )

        values = pd.to_numeric(
            df[outlier_column],
            errors="coerce"
        ).dropna()

        if len(values) >= 4:

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            lower_limit = q1 - 1.5 * iqr
            upper_limit = q3 + 1.5 * iqr

            outliers = values[
                (values < lower_limit) |
                (values > upper_limit)
            ]

            col1, col2, col3 = st.columns(3)

            col1.metric("Q1", f"{q1:,.2f}")
            col2.metric("Q3", f"{q3:,.2f}")
            col3.metric("Outlier Count", len(outliers))

            st.write(f"Lower limit: {lower_limit:,.2f}")
            st.write(f"Upper limit: {upper_limit:,.2f}")

            fig = px.box(
                df,
                y=outlier_column,
                title=f"Box Plot: {outlier_column}"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Not enough numeric values for IQR analysis.")

    else:
        st.info("No numeric columns found.")


# ============================================================
# TAB 4: DATA CLEANING
# ============================================================

with tab4:

    st.header("🛠️ Data Cleaning Workspace")

    st.warning(
        "Cleaning operations below update the working dataset. "
        "Use Reset to Original Dataset in the sidebar to start again."
    )

    st.subheader("Current Working Dataset")
    st.write(f"Rows: {df.shape[0]:,} | Columns: {df.shape[1]:,}")

    # --------------------------------------------------------
    # A. Clean using selected operations
    # --------------------------------------------------------

    st.subheader("1. Apply Data Cleaning Operations")

    with st.form("cleaning_form"):

        clean_blank_strings = st.checkbox(
            "Convert blank text strings to missing values",
            value=True
        )

        remove_empty_columns = st.checkbox(
            "Remove columns that are completely empty",
            value=False
        )

        drop_columns = st.multiselect(
            "Select columns to drop",
            df.columns.tolist(),
            help="Choose only columns you do not need."
        )

        remove_duplicates = st.checkbox(
            "Remove duplicate rows",
            value=False
        )

        st.markdown("**Rename a column (optional)**")

        rename_col = st.selectbox(
            "Column to rename",
            ["-- No Rename --"] + df.columns.tolist()
        )

        new_column_name = st.text_input(
            "New column name",
            placeholder="Enter new name"
        )

        st.markdown("**Fill missing values**")

        fill_method = st.selectbox(
            "Fill method",
            [
                "Do not fill",
                "Numeric mean + categorical mode",
                "Numeric median + categorical mode",
                "Fill with zero for numeric, Unknown for text",
                "Forward fill",
                "Backward fill"
            ]
        )

        convert_dates = st.checkbox(
            "Convert columns containing 'date' in their name to datetime",
            value=False
        )

        apply_cleaning = st.form_submit_button(
            "✅ Apply Cleaning"
        )

    if apply_cleaning:

        cleaned = st.session_state.cleaned_df.copy()

        if clean_blank_strings:

            text_columns = get_categorical_columns(cleaned)

            for col in text_columns:
                cleaned[col] = cleaned[col].replace(
                    r"^\s*$",
                    np.nan,
                    regex=True
                )

        if remove_empty_columns:
            cleaned = cleaned.dropna(axis=1, how="all")

        valid_drop_columns = [
            col for col in drop_columns
            if col in cleaned.columns
        ]

        if valid_drop_columns:
            cleaned = cleaned.drop(
                columns=valid_drop_columns
            )

        if remove_duplicates:
            cleaned = cleaned.drop_duplicates()

        if (
            rename_col != "-- No Rename --"
            and rename_col in cleaned.columns
            and new_column_name.strip()
        ):

            new_name = new_column_name.strip()

            if new_name in cleaned.columns and new_name != rename_col:
                st.error(
                    f"Cannot rename: '{new_name}' already exists."
                )
            else:
                cleaned = cleaned.rename(
                    columns={rename_col: new_name}
                )

        if fill_method == "Numeric mean + categorical mode":

            for col in get_numeric_columns(cleaned):
                if cleaned[col].isna().any():
                    cleaned[col] = cleaned[col].fillna(
                        cleaned[col].mean()
                    )

            for col in get_categorical_columns(cleaned):
                if cleaned[col].isna().any():
                    mode_values = cleaned[col].mode(dropna=True)

                    if not mode_values.empty:
                        cleaned[col] = cleaned[col].fillna(
                            mode_values.iloc[0]
                        )

        elif fill_method == "Numeric median + categorical mode":

            for col in get_numeric_columns(cleaned):
                if cleaned[col].isna().any():
                    cleaned[col] = cleaned[col].fillna(
                        cleaned[col].median()
                    )

            for col in get_categorical_columns(cleaned):
                if cleaned[col].isna().any():
                    mode_values = cleaned[col].mode(dropna=True)

                    if not mode_values.empty:
                        cleaned[col] = cleaned[col].fillna(
                            mode_values.iloc[0]
                        )

        elif fill_method == (
            "Fill with zero for numeric, Unknown for text"
        ):

            for col in get_numeric_columns(cleaned):
                cleaned[col] = cleaned[col].fillna(0)

            for col in get_categorical_columns(cleaned):
                cleaned[col] = cleaned[col].fillna("Unknown")

        elif fill_method == "Forward fill":
            cleaned = cleaned.ffill()

        elif fill_method == "Backward fill":
            cleaned = cleaned.bfill()

        if convert_dates:

            date_cols = get_date_columns(cleaned)

            for col in date_cols:
                cleaned[col] = pd.to_datetime(
                    cleaned[col],
                    errors="coerce"
                )

        st.session_state.cleaned_df = cleaned

        st.success("Cleaning operations applied successfully!")
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # B. Additional numeric conversion
    # --------------------------------------------------------

    st.subheader("2. Convert a Column to Numeric")

    numeric_conversion_col = st.selectbox(
        "Select column to convert",
        ["-- Select --"] + df.columns.tolist(),
        key="numeric_conversion_col"
    )

    if st.button("Convert Selected Column to Numeric"):

        if numeric_conversion_col == "-- Select --":
            st.warning("Please select a column.")

        else:
            cleaned = st.session_state.cleaned_df.copy()

            cleaned[numeric_conversion_col] = pd.to_numeric(
                cleaned[numeric_conversion_col],
                errors="coerce"
            )

            st.session_state.cleaned_df = cleaned

            st.success(
                f"Converted '{numeric_conversion_col}' to numeric."
            )
            st.rerun()

    st.divider()

    # --------------------------------------------------------
    # C. Add calculated columns
    # --------------------------------------------------------

    st.subheader("3. Add Profit and Profit Margin Columns")

    if "Revenue" in df.columns and "Making Cost" in df.columns:

        st.write(
            "Profit = Revenue - Making Cost"
        )

        st.write(
            "Profit Margin (%) = Profit / Revenue × 100"
        )

        if st.button("➕ Create Profit and Profit Margin"):

            cleaned = st.session_state.cleaned_df.copy()

            revenue = pd.to_numeric(
                cleaned["Revenue"],
                errors="coerce"
            )

            cost = pd.to_numeric(
                cleaned["Making Cost"],
                errors="coerce"
            )

            cleaned["Profit"] = revenue - cost

            cleaned["Profit Margin (%)"] = (
                cleaned["Profit"]
                .div(revenue.where(revenue != 0))
                .mul(100)
            ).round(2)

            st.session_state.cleaned_df = cleaned

            st.success("Profit columns created!")
            st.rerun()

    else:
        st.info(
            "The dataset must contain 'Revenue' and 'Making Cost' "
            "to create these calculations."
        )

    st.divider()

    st.subheader("4. Cleaned Dataset Preview")

    st.dataframe(
        st.session_state.cleaned_df.head(20),
        use_container_width=True
    )

    st.write(
        "Remaining missing values:",
        int(st.session_state.cleaned_df.isna().sum().sum())
    )


# ============================================================
# TAB 5: ANALYSIS AND VISUALIZATIONS
# ============================================================

with tab5:

    st.header("📈 Exploratory Data Analysis")

    # Refresh current dataset
    df = st.session_state.cleaned_df.copy()

    # --------------------------------------------------------
    # A. KPI cards
    # --------------------------------------------------------

    st.subheader("1. Key Performance Indicators")

    numeric_cols = get_numeric_columns(df)

    revenue_col = (
        "Revenue" if "Revenue" in df.columns else None
    )

    profit_col = (
        "Profit" if "Profit" in df.columns else None
    )

    quantity_col = (
        "Quantity" if "Quantity" in df.columns else None
    )

    making_cost_col = (
        "Making Cost" if "Making Cost" in df.columns else None
    )

    kpi_cols = st.columns(4)

    kpi_cols[0].metric(
        "Total Records",
        f"{len(df):,}"
    )

    if revenue_col:
        total_revenue = pd.to_numeric(
            df[revenue_col], errors="coerce"
        ).sum()

        kpi_cols[1].metric(
            "Total Revenue",
            f"{total_revenue:,.2f}"
        )
    else:
        kpi_cols[1].metric("Total Revenue", "N/A")

    if quantity_col:
        total_quantity = pd.to_numeric(
            df[quantity_col], errors="coerce"
        ).sum()

        kpi_cols[2].metric(
            "Total Quantity",
            f"{total_quantity:,.0f}"
        )
    else:
        kpi_cols[2].metric("Total Quantity", "N/A")

    if profit_col:
        total_profit = pd.to_numeric(
            df[profit_col], errors="coerce"
        ).sum()

        kpi_cols[3].metric(
            "Total Profit",
            f"{total_profit:,.2f}"
        )
    elif revenue_col and making_cost_col:

        total_profit = (
            pd.to_numeric(df[revenue_col], errors="coerce")
            - pd.to_numeric(df[making_cost_col], errors="coerce")
        ).sum()

        kpi_cols[3].metric(
            "Estimated Profit",
            f"{total_profit:,.2f}"
        )

    else:
        kpi_cols[3].metric("Total Profit", "N/A")

    st.divider()

    # --------------------------------------------------------
    # B. Monthly revenue
    # --------------------------------------------------------

    st.subheader("2. Monthly Revenue Analysis")

    if revenue_col:

        if "Date" in df.columns:

            chart_df = df.copy()

            chart_df["Date"] = pd.to_datetime(
                chart_df["Date"],
                errors="coerce"
            )

            chart_df[revenue_col] = pd.to_numeric(
                chart_df[revenue_col],
                errors="coerce"
            )

            chart_df = chart_df.dropna(
                subset=["Date", revenue_col]
            )

            if not chart_df.empty:

                chart_df["Year-Month"] = (
                    chart_df["Date"].dt.to_period("M").astype(str)
                )

                monthly = (
                    chart_df.groupby("Year-Month", as_index=False)
                    [revenue_col]
                    .sum()
                    .sort_values("Year-Month")
                )

                fig = px.line(
                    monthly,
                    x="Year-Month",
                    y=revenue_col,
                    markers=True,
                    title="Monthly Revenue Trend"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:
                st.info(
                    "No valid dates and revenue values available."
                )

        else:
            st.info("A Date column is required for monthly analysis.")

    else:
        st.info("A Revenue column is required for revenue analysis.")

    st.divider()

    # --------------------------------------------------------
    # C. Category analysis
    # --------------------------------------------------------

    st.subheader("3. Revenue by Product Category")

    if (
        revenue_col
        and "Product Category" in df.columns
    ):

        category_df = df.copy()

        category_df[revenue_col] = pd.to_numeric(
            category_df[revenue_col],
            errors="coerce"
        )

        category_summary = (
            category_df.groupby(
                "Product Category",
                as_index=False,
                dropna=False
            )[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )

        fig = px.bar(
            category_summary,
            x="Product Category",
            y=revenue_col,
            color="Product Category",
            title="Revenue by Product Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            category_summary,
            use_container_width=True
        )

    else:
        st.info(
            "Product Category and Revenue columns are required."
        )

    st.divider()

    # --------------------------------------------------------
    # D. Subcategory analysis
    # --------------------------------------------------------

    st.subheader("4. Revenue by Sub Category")

    if (
        revenue_col
        and "Sub Category" in df.columns
    ):

        sub_df = df.copy()

        sub_df[revenue_col] = pd.to_numeric(
            sub_df[revenue_col],
            errors="coerce"
        )

        sub_summary = (
            sub_df.groupby(
                "Sub Category",
                as_index=False,
                dropna=False
            )[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )

        fig = px.bar(
            sub_summary,
            x="Sub Category",
            y=revenue_col,
            title="Revenue by Sub Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Sub Category and Revenue columns are required.")

    st.divider()

    # --------------------------------------------------------
    # E. Country analysis
    # --------------------------------------------------------

    st.subheader("5. Country-wise Revenue")

    if revenue_col and "Country" in df.columns:

        country_df = df.copy()

        country_df[revenue_col] = pd.to_numeric(
            country_df[revenue_col],
            errors="coerce"
        )

        country_summary = (
            country_df.groupby(
                "Country",
                as_index=False,
                dropna=False
            )[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )

        fig = px.pie(
            country_summary,
            names="Country",
            values=revenue_col,
            title="Revenue Share by Country"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            country_summary,
            use_container_width=True
        )

    else:
        st.info("Country and Revenue columns are required.")

    st.divider()

    # --------------------------------------------------------
    # F. Gender analysis
    # --------------------------------------------------------

    st.subheader("6. Gender-wise Revenue")

    if revenue_col and "Customer Gender" in df.columns:

        gender_df = df.copy()

        gender_df[revenue_col] = pd.to_numeric(
            gender_df[revenue_col],
            errors="coerce"
        )

        gender_summary = (
            gender_df.groupby(
                "Customer Gender",
                as_index=False,
                dropna=False
            )[revenue_col]
            .sum()
        )

        fig = px.bar(
            gender_summary,
            x="Customer Gender",
            y=revenue_col,
            color="Customer Gender",
            title="Revenue by Customer Gender"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Customer Gender and Revenue columns are required.")

    st.divider()

    # --------------------------------------------------------
    # G. Profit analysis
    # --------------------------------------------------------

    st.subheader("7. Revenue vs Profit")

    if revenue_col:

        scatter_df = df.copy()

        scatter_df[revenue_col] = pd.to_numeric(
            scatter_df[revenue_col],
            errors="coerce"
        )

        if profit_col:
            selected_profit_col = profit_col

        elif making_cost_col:
            scatter_df["Profit"] = (
                pd.to_numeric(
                    scatter_df[revenue_col],
                    errors="coerce"
                )
                - pd.to_numeric(
                    scatter_df[making_cost_col],
                    errors="coerce"
                )
            )

            selected_profit_col = "Profit"

        else:
            selected_profit_col = None

        if selected_profit_col:

            fig = px.scatter(
                scatter_df,
                x=revenue_col,
                y=selected_profit_col,
                title="Revenue vs Profit",
                opacity=0.6
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info(
                "Create a Profit column or provide Making Cost "
                "to compare revenue and profit."
            )

    st.divider()

    # --------------------------------------------------------
    # H. Correlation heatmap
    # --------------------------------------------------------

    st.subheader("8. Correlation Analysis")

    numeric_cols = get_numeric_columns(df)

    if len(numeric_cols) >= 2:

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            title="Numeric Column Correlation Matrix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(
            "At least two numeric columns are required "
            "for correlation analysis."
        )

    st.divider()

    # --------------------------------------------------------
    # I. Group-by analysis
    # --------------------------------------------------------

    st.subheader("9. GroupBy Business Analysis")

    group_options = get_categorical_columns(df)

    if group_options and numeric_cols:

        col1, col2 = st.columns(2)

        with col1:
            group_column = st.selectbox(
                "Group by column",
                group_options,
                key="group_column"
            )

        with col2:
            calculation_column = st.selectbox(
                "Numeric column",
                numeric_cols,
                key="calculation_column"
            )

        aggregation = st.selectbox(
            "Aggregation",
            ["Sum", "Mean", "Count", "Minimum", "Maximum"]
        )

        agg_mapping = {
            "Sum": "sum",
            "Mean": "mean",
            "Count": "count",
            "Minimum": "min",
            "Maximum": "max"
        }

        summary = (
            df.groupby(
                group_column,
                dropna=False
            )[calculation_column]
            .agg(agg_mapping[aggregation])
            .reset_index()
        )

        summary = summary.sort_values(
            calculation_column,
            ascending=False
        )

        st.dataframe(
            summary,
            use_container_width=True
        )

        fig = px.bar(
            summary.head(20),
            x=group_column,
            y=calculation_column,
            title=f"{aggregation} of {calculation_column} by {group_column}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(
            "GroupBy analysis needs at least one text column "
            "and one numeric column."
        )


# ============================================================
# TAB 6: FILTER AND DOWNLOAD
# ============================================================

with tab6:

    st.header("⬇️ Filter and Download Dataset")

    df = st.session_state.cleaned_df.copy()

    st.subheader("1. Filter Your Dataset")

    filtered_df = df.copy()

    # --------------------------------------------------------
    # Filter by Year
    # --------------------------------------------------------

    if "Year" in filtered_df.columns:

        year_values = sorted(
            filtered_df["Year"].dropna().unique().tolist(),
            key=lambda x: str(x)
        )

        selected_years = st.multiselect(
            "Select Year",
            year_values,
            default=year_values,
            key="filter_year"
        )

        filtered_df = filtered_df[
            filtered_df["Year"].isin(selected_years)
        ]

    # --------------------------------------------------------
    # Filter by Country
    # --------------------------------------------------------

    if "Country" in filtered_df.columns:

        country_values = sorted(
            filtered_df["Country"].dropna().unique().tolist(),
            key=lambda x: str(x)
        )

        selected_countries = st.multiselect(
            "Select Country",
            country_values,
            default=country_values,
            key="filter_country"
        )

        filtered_df = filtered_df[
            filtered_df["Country"].isin(selected_countries)
        ]

    # --------------------------------------------------------
    # Filter by State
    # --------------------------------------------------------

    if "State" in filtered_df.columns:

        state_values = sorted(
            filtered_df["State"].dropna().unique().tolist(),
            key=lambda x: str(x)
        )

        selected_states = st.multiselect(
            "Select State",
            state_values,
            default=state_values,
            key="filter_state"
        )

        filtered_df = filtered_df[
            filtered_df["State"].isin(selected_states)
        ]

    # --------------------------------------------------------
    # Filter by Customer Gender
    # --------------------------------------------------------

    if "Customer Gender" in filtered_df.columns:

        gender_values = sorted(
            filtered_df["Customer Gender"].dropna().unique().tolist(),
            key=lambda x: str(x)
        )

        selected_genders = st.multiselect(
            "Select Customer Gender",
            gender_values,
            default=gender_values,
            key="filter_gender"
        )

        filtered_df = filtered_df[
            filtered_df["Customer Gender"].isin(selected_genders)
        ]

    # --------------------------------------------------------
    # Filter by Product Category
    # --------------------------------------------------------

    if "Product Category" in filtered_df.columns:

        category_values = sorted(
            filtered_df["Product Category"].dropna().unique().tolist(),
            key=lambda x: str(x)
        )

        selected_categories = st.multiselect(
            "Select Product Category",
            category_values,
            default=category_values,
            key="filter_category"
        )

        filtered_df = filtered_df[
            filtered_df["Product Category"].isin(selected_categories)
        ]

    # --------------------------------------------------------
    # Filter by Sub Category
    # --------------------------------------------------------

    if "Sub Category" in filtered_df.columns:

        subcategory_values = sorted(
            filtered_df["Sub Category"].dropna().unique().tolist(),
            key=lambda x: str(x)
        )

        selected_subcategories = st.multiselect(
            "Select Sub Category",
            subcategory_values,
            default=subcategory_values,
            key="filter_subcategory"
        )

        filtered_df = filtered_df[
            filtered_df["Sub Category"].isin(
                selected_subcategories
            )
        ]

    # --------------------------------------------------------
    # Numeric range filter
    # --------------------------------------------------------

    numeric_cols = get_numeric_columns(filtered_df)

    if numeric_cols:

        numeric_filter_col = st.selectbox(
            "Optional numeric filter",
            ["No Numeric Filter"] + numeric_cols,
            key="numeric_filter_col"
        )

        if numeric_filter_col != "No Numeric Filter":

            numeric_values = pd.to_numeric(
                filtered_df[numeric_filter_col],
                errors="coerce"
            ).dropna()

            if not numeric_values.empty:

                minimum = float(numeric_values.min())
                maximum = float(numeric_values.max())

                if minimum < maximum:

                    selected_range = st.slider(
                        f"Range for {numeric_filter_col}",
                        min_value=minimum,
                        max_value=maximum,
                        value=(minimum, maximum),
                        key="numeric_range"
                    )

                    filtered_df = filtered_df[
                        pd.to_numeric(
                            filtered_df[numeric_filter_col],
                            errors="coerce"
                        ).between(
                            selected_range[0],
                            selected_range[1]
                        )
                    ]

                else:
                    st.info(
                        "The selected column has only one numeric value."
                    )

    st.divider()

    st.subheader("2. Filtered Dataset Preview")

    st.metric("Filtered Rows", f"{len(filtered_df):,}")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("3. Download Reports")

    # Convert datetime columns for CSV compatibility
    cleaned_download = df.copy()
    filtered_download = filtered_df.copy()

    def prepare_csv(data):
        export_df = data.copy()

        for col in export_df.columns:
            if pd.api.types.is_datetime64_any_dtype(export_df[col]):
                export_df[col] = export_df[col].astype(str)

        return export_df.to_csv(index=False).encode("utf-8-sig")

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇️ Download Cleaned Dataset",
            data=prepare_csv(cleaned_download),
            file_name="cleaned_sales_data.csv",
            mime="text/csv"
        )

    with col2:

        st.download_button(
            label="⬇️ Download Filtered Dataset",
            data=prepare_csv(filtered_download),
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )

    missing_report = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Missing Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    st.download_button(
        label="⬇️ Download Missing Values Report",
        data=missing_report.to_csv(index=False).encode("utf-8-sig"),
        file_name="missing_values_report.csv",
        mime="text/csv"
    )

# ============================================================
# END OF APPLICATION
# ============================================================

st.sidebar.divider()
st.sidebar.caption("Built with Python, Pandas, Streamlit & Plotly")
