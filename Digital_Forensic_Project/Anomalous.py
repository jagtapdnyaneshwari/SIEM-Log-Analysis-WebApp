import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\Security_logs.csv'  

def retrieve_data_from_csv(csv_file):
    data = []
    try:
        with open(csv_file, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data

def train_anomaly_detection_model(data):
    df = pd.DataFrame(data)

    features = df[["Event ID", "Task Category"]]
    features = pd.get_dummies(features)

    # Train Isolation Forest model
    model = IsolationForest(contamination=0.05)
    model.fit(features)
    return model

def identify_anomalies(data, model):
#    Identifies anomalous events using the trained anomaly detection model.
    df = pd.DataFrame(data)
    # Extract Event ID, Task Category for prediction
    features = df[["Event ID", "Task Category"]]
    features = pd.get_dummies(features)
    # Predict anomalies
    anomalies = model.predict(features)
    return anomalies

def create_html_page(data, anomalies, output_file):
    with open(output_file, 'w') as html_file:
        html_file.write('<html><head><title>Security Events Logs</title></head><body>')
        # Write data table
        html_file.write('<h1>Anomalous Windows Events:</h1>')
        html_file.write('<table border="1"><tr><th>Date and Time</th><th>Source</th><th>Event ID</th><th>Task Category</th><th>Anomaly</th></tr>')
        for data, is_anomaly in zip(data, anomalies):
            if is_anomaly == -1:  # Filter and print anomalous events
                html_file.write('<tr>')
                html_file.write(f'<td>{data["Date and Time"]}</td>')
                html_file.write(f'<td>{data["Source"]}</td>')
                html_file.write(f'<td>{data["Event ID"]}</td>')
                html_file.write(f'<td>{data["Task Category"]}</td>')
                html_file.write('<td style="background-color: yellow">Anomalous</td>')  # Highlight anomalies
                html_file.write('</tr>')

        html_file.write('</table>')
        html_file.write('</body></html>')

if __name__ == "__main__":
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        # Train the anomaly detection model
        anomaly_model = train_anomaly_detection_model(all_data)

        # Identify anomalous events
        anomalies = identify_anomalies(all_data, anomaly_model)

        output_file = 'Anomalous_logs.html'
        create_html_page(all_data, anomalies, output_file)

        print(f"Data has been saved to {output_file}. Open this file in a web browser to view the anomalous events.")
