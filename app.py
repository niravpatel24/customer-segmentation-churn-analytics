import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="European Banking Customer Churn Dashboard",
    layout="wide"
)

# Load data
df = pd.read_csv("Bank data.csv")
df.columns = df.columns.str.strip()

# Title
st.title("🏦 European Banking Customer Churn Dashboard")
st.write("Customer segmentation and churn pattern analysis")

# Sidebar filters
st.sidebar.header("Filters")

geo_filter = st.sidebar.selectbox(
    "Geography",
    ["All"] + sorted(df["Geography"].unique().tolist())
)

gender_filter = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

status_filter = st.sidebar.selectbox(
    "Customer Status",
    ["All"] + sorted(df["Customer Status"].unique().tolist())
)

# Filter data
filtered_df = df.copy()

if geo_filter != "All":
    filtered_df = filtered_df[filtered_df["Geography"] == geo_filter]

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Customer Status"] == status_filter]

# KPI calculations
total_customers = len(filtered_df)
churned = filtered_df["Exited"].sum()
churn_rate = filtered_df["Exited"].mean() * 100
total_balance = filtered_df["Balance"].sum()

highest_geo_churn = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .max()
) * 100

geographic_risk_index = highest_geo_churn / churn_rate

active_churn = (
    filtered_df[filtered_df["Activity Status"] == "Active"]["Exited"].mean()
) * 100

inactive_churn = (
    filtered_df[filtered_df["Activity Status"] == "Inactive"]["Exited"].mean()
) * 100

engagement_drop_indicator = inactive_churn - active_churn

# KPI cards
col1, col2, col3, col4, col5,col6 = st.columns(6)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Total Balance", f"₹{total_balance:,.0f}")
col5.metric("Geographic Risk Index", f"{geographic_risk_index:.2f}x")
col6.metric("Engagement Drop Indicator", f"{engagement_drop_indicator:.2f} pp")

# Geography
st.subheader("🌍 Churn by Geography")

geo_churn = (
    filtered_df.groupby("Geography")["Exited"]
    .mean()
    .reset_index()
)

geo_churn["Exited"] = geo_churn["Exited"] * 100

st.bar_chart(geo_churn.set_index("Geography"))

# Age Group
st.subheader("🎂 Churn by Age Group")

if "Age Grouped" not in filtered_df.columns:
    filtered_df["Age Grouped"] = pd.cut(
        filtered_df["Age"],
        bins=[0, 29, 45, 60, float("inf")],
        labels=["<30", "30–45", "46–60", "60+"]
    )

age_churn = (
    filtered_df.groupby("Age Grouped", observed=False)["Exited"]
    .mean()
    .reset_index()
)

age_churn["Exited"] = age_churn["Exited"] * 100

st.bar_chart(age_churn.set_index("Age Grouped"))
# Tenure Group
st.subheader("📅 Churn by Tenure Group")

tenure_churn = (
    filtered_df.groupby("Tenure Group")["Exited"]
    .mean()
    .reset_index()
)

tenure_churn["Exited"] = tenure_churn["Exited"] * 100

st.bar_chart(tenure_churn.set_index("Tenure Group"))

# Balance Segment
st.subheader("💰 Churn by Balance Segment")

balance_analysis = (
    filtered_df.groupby("Balance Segment")["Exited"]
    .mean()
    .reset_index()
)

balance_analysis["Exited"] = balance_analysis["Exited"] * 100

st.bar_chart(balance_analysis.set_index("Balance Segment"))

# Gender
st.subheader("👥 Churn by Gender")

gender_churn = (
    filtered_df.groupby("Gender")["Exited"]
    .mean()
    .reset_index()
)

gender_churn["Exited"] = gender_churn["Exited"] * 100

st.bar_chart(gender_churn.set_index("Gender"))

# Activity Status
st.subheader("📊 Churn by Activity Status")

activity_churn = (
    filtered_df.groupby("Activity Status")["Exited"]
    .mean()
    .reset_index()
)

activity_churn["Exited"] = activity_churn["Exited"] * 100

st.bar_chart(activity_churn.set_index("Activity Status"))

# Number of Products
st.subheader("🏦 Churn by Number of Products")

product_churn = (
    filtered_df.groupby("NumOfProducts")["Exited"]
    .mean()
    .reset_index()
)

product_churn["Exited"] = product_churn["Exited"] * 100

st.bar_chart(product_churn.set_index("NumOfProducts"))

# High-Value Customer Explorer
st.subheader("💎 High-Value Customer Churn Explorer")

high_value = filtered_df[filtered_df["Balance Segment"] == "High Balance"]

high_value_total = len(high_value)
high_value_churned = high_value["Exited"].sum()

col1, col2 = st.columns(2)

churned_high_value_balance = high_value[high_value["Exited"] == 1]["Balance"].sum()

churned_high_value_balance = high_value[high_value["Exited"] == 1]["Balance"].sum()

st.metric(
    "Churned High-Value Balance",
    f"₹{churned_high_value_balance:,.0f}"
)

if high_value_total > 0:
    high_value_churn_rate = high_value["Exited"].mean() * 100
    st.write(f"High-Value Customer Churn Rate: **{high_value_churn_rate:.2f}%**")
else:
    st.write("No high-value customers found for the selected filters.")

# Key Findings
st.subheader("🔎 Key Findings")

st.write(
    "• Overall churn rate is 20.37%."
)

st.write(
    "• Germany has the highest geographical churn rate at 32.44%."
)

st.write(
    "• Customers aged 46–60 show the highest age-group churn rate at 51.12%."
)

st.write(
    "• High-balance customers have a churn rate of 25.23%."
)

st.write(
    "• Inactive customers have a higher churn rate than active customers."
)

st.write(
    "• Customers with 3 or 4 products show very high churn rates."
)

# Business Recommendations
st.subheader("💡 Business Recommendations")

st.write(
    "• Focus retention efforts on customers aged 46–60, as this group has a high churn rate."
)

st.write(
    "• Prioritize customers in Germany because Germany has the highest geographical churn rate."
)

st.write(
    "• Provide personalized retention offers and relationship management for high-balance customers."
)

st.write(
    "• Increase engagement with inactive customers through targeted communication and banking offers."
)

st.write(
    "• Review customers with 3 or 4 products and identify the reasons behind their high churn."
)

# Geography and Age Drill-Down
st.subheader("🔎 Geography × Age Group Drill-Down")

geo_age_churn = (
    filtered_df.groupby(["Geography", "Age Grouped"], observed=False)
    .agg(
        Customers=("CustomerId", "count"),
        Churn_Rate=("Exited", "mean")
    )
    .reset_index()
)

geo_age_churn["Churn_Rate"] = geo_age_churn["Churn_Rate"] * 100

st.dataframe(
    geo_age_churn,
    use_container_width=True
)