import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import matplotlib.ticker as mtick

# Set up Streamlit multi-page interface
st.set_page_config(page_title="Financial Analysis Dashboard", page_icon="📊", layout="wide")

# Create sidebar with selection options
st.sidebar.header("Select a File")
page = st.sidebar.selectbox("Choose a report type", ("AFC Profit and Loss", "Real Estate Profit and Loss"))

# Function to extract relevant data and plot for AFC
def plot_afc_data(file):
    if file is not None:
        # Load the AFC Excel file
        df = pd.read_excel(file, sheet_name="Profit and Loss", header=4, engine="openpyxl")

        # Rename first column if necessary
        df.rename(columns={"Unnamed: 0": "Description"}, inplace=True)

        # Define the rows of interest for AFC
        rows_of_interest = ["Total Income", "Total Cost of Goods Sold", "Gross Profit", "Total Expenses", "Net Operating Income", "Net Income"]

        # Extract relevant data for AFC
        extracted_data = {}
        for row in rows_of_interest:
            filtered_row = df[df["Description"] == row]
            if not filtered_row.empty:
                extracted_data[row] = filtered_row.iloc[0, 1:].values

        # Get column names (months) excluding "Total" if present
        columns = df.columns[1:]
        if "Total" in columns:
            columns = columns[:-1]  # Exclude last column

        # Convert values to numeric
        for key in extracted_data:
            extracted_data[key] = np.array(extracted_data[key][:len(columns)], dtype=float)

        # Plot the AFC data
        plt.figure(figsize=(12, 6))
        for row, values in extracted_data.items():
            plt.plot(columns, values, label=row, marker='o')

        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.title('Financial Metrics Over Time')
        plt.legend(loc='upper left')
        plt.xticks(rotation=45)

        # Format y-axis as currency
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))  # Format with dollar sign and commas

        plt.tight_layout()

        # Display the plot on Streamlit
        st.pyplot(plt)

        # Convert extracted data to a DataFrame for interactive plotting
        extracted_data = {key: np.round(value[:len(columns)], 2) for key, value in extracted_data.items()}

        # Extract Month and Year separately
        data_list = []
        for idx, col in enumerate(columns):
            try:
                month, year = col.split()  # Splitting "Jan 2023" into "Jan" and "2023"
                row_values = {row: extracted_data[row][idx] for row in rows_of_interest}
                data_list.append({"Year": year, "Month": month, **row_values})
            except ValueError:
                print(f"Skipping column '{col}' due to unexpected format.")

        # Convert extracted data into DataFrame
        plot_df = pd.DataFrame(data_list)

        # Ensure "Month" column exists
        if "Month" not in plot_df.columns:
            raise ValueError("Month column not found in DataFrame")

        # Convert "Year" to categorical for proper sorting
        plot_df["Year"] = plot_df["Year"].astype(str)

        # Create an interactive bar chart for "Net Income"
        fig = px.bar(
            plot_df,
            x="Month",
            y="Net Income",
            color="Year",
            text_auto=".2s",
            title="Monthly Net Income with Detailed Breakdown",
            labels={"Net Income": "Amount ($)", "Month": "Month"},
            hover_data=["Total Income", "Total Cost of Goods Sold", "Gross Profit", "Total Expenses"],
        )

        # Format y-axis as currency
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")

        # Show the interactive chart
        st.plotly_chart(fig)

# Function to extract relevant data and plot for Real Estate
def plot_real_estate_data(file):
    if file is not None:
        # Load the Real Estate Excel file
        df = pd.read_excel(file, sheet_name="Profit and Loss", header=4, engine="openpyxl")

        # Rename first column if necessary
        df.rename(columns={"Unnamed: 0": "Description"}, inplace=True)

        # Define the rows of interest for Real Estate
        rows_of_interest = ["Total Income", "Gross Profit", "   Total Payroll & Related", "Total Expenses", "Net Operating Income", "Net Income"]

        # Check if "   Total Payroll & Related" exists, otherwise use "   Total 6200 - Payroll Expenses"
        payroll_column = "   Total Payroll & Related" if "   Total Payroll & Related" in df["Description"].values else "   Total 6200 - Payroll Expenses"
        rows_of_interest[2] = payroll_column

        # Extract relevant data for Real Estate
        extracted_data = {}
        for row in rows_of_interest:
            filtered_row = df[df["Description"] == row]
            if not filtered_row.empty:
                extracted_data[row] = filtered_row.iloc[0, 1:].values

        # Get column names (months) excluding "Total" if present
        columns = df.columns[1:]
        if "Total" in columns:
            columns = columns[:-1]  # Exclude last column

        # Convert values to numeric
        for key in extracted_data:
            extracted_data[key] = np.array(extracted_data[key][:len(columns)], dtype=float)

        # Plot the Real Estate data
        plt.figure(figsize=(12, 6))
        for row, values in extracted_data.items():
            plt.plot(columns, values, label=row, marker='o')

        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.title('Financial Metrics Over Time')
        plt.legend(loc='upper left')
        plt.xticks(rotation=45)

        # Format y-axis as currency
        ax = plt.gca()
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))  # Format with dollar sign and commas

        plt.tight_layout()

        # Display the plot on Streamlit
        st.pyplot(plt)

        # Convert extracted data to a DataFrame for interactive plotting
        extracted_data = {key: np.round(value[:len(columns)], 2) for key, value in extracted_data.items()}

        # Extract Month and Year separately
        data_list = []
        for idx, col in enumerate(columns):
            try:
                month, year = col.split()  # Splitting "Jan 2023" into "Jan" and "2023"
                row_values = {row: extracted_data[row][idx] for row in rows_of_interest}
                data_list.append({"Year": year, "Month": month, **row_values})
            except ValueError:
                print(f"Skipping column '{col}' due to unexpected format.")

        # Convert extracted data into DataFrame
        plot_df = pd.DataFrame(data_list)

        # Ensure "Month" column exists
        if "Month" not in plot_df.columns:
            raise ValueError("Month column not found in DataFrame")

        # Convert "Year" to categorical for proper sorting
        plot_df["Year"] = plot_df["Year"].astype(str)

        # Create an interactive bar chart for "Net Income"
        fig = px.bar(
            plot_df,
            x="Month",
            y="Net Income",
            color="Year",
            text_auto=".2s",
            title="Monthly Net Income with Detailed Breakdown",
            labels={"Net Income": "Amount ($)", "Month": "Month"},
            hover_data=["Total Income", "Gross Profit", payroll_column, "Total Expenses"],
        )

        # Format y-axis as currency
        fig.update_yaxes(tickprefix="$", tickformat=",.0f")

        # Show the interactive chart
        st.plotly_chart(fig)

# Streamlit page handling
if page == "AFC Profit and Loss":
    st.header("AFC Profit and Loss Analysis")
    file = st.file_uploader("Upload your AFC Profit and Loss Excel file", type=["xlsx"])
    plot_afc_data(file)

elif page == "Real Estate Profit and Loss":
    st.header("Real Estate Profit and Loss Analysis")
    file = st.file_uploader("Upload your Real Estate Profit and Loss Excel file", type=["xlsx"])
    plot_real_estate_data(file)
