import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
DATA_PATH = Path("outputs/ola_cleaned.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Dataset could not be loaded: {e}")
    st.info("Check that outputs/ola_cleaned.csv exists.")
    st.stop()

# ---------------- HEADER ----------------
st.title("🚕 OLA RIDE INSIGHTS")
st.caption("Ride Sharing Data Analysis | SQL | Python | Power BI")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    ["Home", "Ride Analysis", "SQL Insights", "Power BI Dashboard"]
)

# ---------------- HOME ----------------
if page == "Home":

    st.subheader("Project Overview")

    st.write(
        "OLA Ride Insights is a data analytics project "
        "that analyzes ride bookings, revenue, cancellations, "
        "vehicle performance and customer ratings."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Bookings", f"{len(df):,}")

    if "Booking_Status" in df.columns:
        success = (df["Booking_Status"] == "Success").sum()
        c2.metric("Successful Bookings", f"{success:,}")

    if "Booking_Value" in df.columns:
        revenue = df.loc[
            df["Booking_Status"] == "Success", "Booking_Value"
        ].sum() if "Booking_Status" in df.columns else df["Booking_Value"].sum()
        c3.metric("Total Revenue", f"₹{revenue:,.0f}")

    if "Booking_Status" in df.columns:
        cancelled = df["Booking_Status"].isin(
            ["Canceled by Customer", "Canceled by Driver"]
        ).sum()
        c4.metric("Cancelled Rides", f"{cancelled:,}")

    st.subheader("Booking Status Overview")

    if "Booking_Status" in df.columns:
        status = df["Booking_Status"].value_counts().reset_index()
        status.columns = ["Booking Status", "Bookings"]

        fig = px.pie(
            status,
            names="Booking Status",
            values="Bookings",
            hole=0.45,
            title="Booking Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------- RIDE ANALYSIS ----------------
elif page == "Ride Analysis":

    st.subheader("Interactive Ride Analysis")

    filtered = df.copy()

    if "Vehicle_Type" in df.columns:
        vehicles = sorted(df["Vehicle_Type"].dropna().unique())
        selected_vehicle = st.multiselect(
            "Select Vehicle Type",
            vehicles,
            default=vehicles
        )
        filtered = filtered[
            filtered["Vehicle_Type"].isin(selected_vehicle)
        ]

    if "Booking_Status" in df.columns:
        statuses = sorted(df["Booking_Status"].dropna().unique())
        selected_status = st.multiselect(
            "Select Booking Status",
            statuses,
            default=statuses
        )
        filtered = filtered[
            filtered["Booking_Status"].isin(selected_status)
        ]

    if "Payment_Method" in df.columns:
        payments = sorted(df["Payment_Method"].dropna().unique())
        selected_payment = st.multiselect(
            "Select Payment Method",
            payments,
            default=payments
        )
        filtered = filtered[
            filtered["Payment_Method"].isin(selected_payment)
        ]

    search = st.text_input("Search Booking ID or Customer ID")

    if search:
        mask = pd.Series(False, index=filtered.index)

        for col in ["Booking_ID", "Customer_ID"]:
            if col in filtered.columns:
                mask |= filtered[col].astype(str).str.contains(
                    search, case=False, na=False
                )

        filtered = filtered[mask]

    st.metric("Filtered Bookings", f"{len(filtered):,}")

    st.dataframe(filtered, use_container_width=True)

    st.download_button(
        "Download Filtered Data",
        filtered.to_csv(index=False).encode("utf-8"),
        "ola_filtered_bookings.csv",
        "text/csv"
    )

# ---------------- SQL INSIGHTS ----------------
elif page == "SQL Insights":

    st.subheader("SQL Analysis Results")

    questions = [
        "Successful Bookings",
        "Average Ride Distance by Vehicle",
        "Customer Cancelled Rides",
        "Top 5 Customers by Number of Rides",
        "Driver Cancellation Reasons",
        "Prime Sedan Driver Ratings",
        "UPI Payment Rides",
        "Average Customer Rating by Vehicle",
        "Total Successful Booking Value",
        "Incomplete Rides with Reasons"
    ]

    choice = st.selectbox("Select SQL Analysis", questions)

    if choice == questions[0]:
        result = df[df["Booking_Status"] == "Success"]

    elif choice == questions[1]:
        result = df.groupby("Vehicle_Type")["Ride_Distance"].mean().round(2).reset_index()

    elif choice == questions[2]:
        result = df[
            df["Booking_Status"] == "Canceled by Customer"
        ]

    elif choice == questions[3]:
        result = df.groupby("Customer_ID").size().reset_index(name="Total Rides")
        result = result.sort_values("Total Rides", ascending=False).head(5)

    elif choice == questions[4]:
        col = "Canceled_Rides_by_Driver"
        result = df[col].dropna().value_counts().reset_index()
        result.columns = ["Cancellation Reason", "Total"]

    elif choice == questions[5]:
        result = df[df["Vehicle_Type"] == "Prime Sedan"]
        result = pd.DataFrame({
            "Maximum Driver Rating": [result["Driver_Ratings"].max()],
            "Minimum Driver Rating": [result["Driver_Ratings"].min()]
        })

    elif choice == questions[6]:
        result = df[df["Payment_Method"] == "UPI"]

    elif choice == questions[7]:
        result = df.groupby("Vehicle_Type")["Customer_Rating"].mean().round(2).reset_index()

    elif choice == questions[8]:
        revenue = df.loc[
            df["Booking_Status"] == "Success", "Booking_Value"
        ].sum()
        result = pd.DataFrame({"Total Successful Booking Value": [revenue]})

    else:
        if "Incomplete_Rides" in df.columns:
            result = df[df["Incomplete_Rides"].astype(str).str.lower() == "yes"]
        else:
            result = pd.DataFrame()

        cols = [
            c for c in [
                "Booking_ID", "Booking_Status",
                "Incomplete_Rides", "Incomplete_Rides_Reason"
            ] if c in result.columns
        ]
        result = result[cols]

    st.dataframe(result, use_container_width=True)
    st.caption(f"Records displayed: {len(result):,}")

# ---------------- POWER BI DASHBOARD ----------------
elif page == "Power BI Dashboard":

    st.subheader("Power BI Interactive Dashboard")

    st.write(
        "View the OLA Ride Insights dashboard created using Power BI."
    )

    report_url = st.text_input(
        "Enter your Power BI Publish to web Embed URL",
        placeholder="https://app.powerbi.com/view?r=..."
    )

    if report_url.startswith("https://app.powerbi.com/view?r="):
        st.components.v1.iframe(
            report_url,
            height=650,
            scrolling=True
        )
    else:
        st.info(
            "Publish your Power BI report to web and paste its "
            "embed URL here to display the dashboard."
        )

# ---------------- FOOTER ----------------
st.divider()
st.caption("OLA Ride Insights | Data Analytics Project")
st.caption("Developed using Python, Pandas, Streamlit, SQL and Power BI")