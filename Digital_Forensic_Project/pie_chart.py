import csv
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\All_Priority_Windows_Logs.csv'  

def read_csv(file_path):
    return pd.read_csv(file_path)

if __name__ == "__main__":
    df = read_csv(CSV_FILE)
    print("All data from CSV:")
    print(df)
    aggregation_counts = df.groupby(['Level', 'Source', 'Event ID', 'Task Category']).size().reset_index(name='Count')

    # Create a pie chart for aggregated counts
    counts = aggregation_counts['Count']
    labels = aggregation_counts.apply(lambda row: f"{row['Level']} - {row['Source']} - {row['Event ID']} - {row['Task Category']}", axis=1)

    # Create the pie chart using Plotly
    fig = go.Figure(data=[go.Pie(labels=labels, values=counts, hoverinfo='label+percent', textinfo='label+percent')])

    fig.update_layout(
        title="<span style='font-weight: bold; color: black;'>Aggregated Counts Pie Chart</span>",
        width=1700,  # Set the width of the chart
        height=1700,  # Set the height of the chart
    )

    pyo.plot(fig, filename='Aggregated_Counts_Pie_chart.html', auto_open=False)
