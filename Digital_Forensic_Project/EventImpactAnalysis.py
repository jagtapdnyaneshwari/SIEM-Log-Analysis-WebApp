import csv
import pandas as pd
from sklearn.ensemble import IsolationForest

# CSV file configuration
CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\Security_logs.csv'  # CSV file path

# Define the number of records to display per page
RECORDS_PER_PAGE = 20

def retrieve_data_from_csv(csv_file):
    """Retrieves data from the specified CSV file and returns it as a list of dictionaries."""
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
    """
    Trains an anomaly detection model using the Isolation Forest algorithm.
    You can replace this with other anomaly detection algorithms if needed.
    """
    df = pd.DataFrame(data)
    features = df[["Event ID"]]  # Choose relevant features for anomaly detection
    model = IsolationForest(contamination=0.05)  # Adjust the contamination parameter
    model.fit(features)
    return model

def identify_anomalies(data, model):
    """
    Identifies anomalous events using the trained anomaly detection model.
    Assumes that "Event ID" is used as the feature for detection.
    """
    df = pd.DataFrame(data)
    features = df[["Event ID"]]
    anomalies = model.predict(features)
    return anomalies

def create_html_page(anomalous_data, output_file):
    with open(output_file, 'w') as html_file:
        # Write the HTML header
        html_file.write('<html><head><title>Anomalous Activity</title></head><body>')

        # Write the data table with pagination
        html_file.write('<h1>Anomalous Activity:</h1>')
        html_file.write('<table border="1"><tr><th>Date and Time</th><th>Source</th><th>Event ID</th><th>Task Category</th></tr>')

        # Implement pagination
        page = 1
        page_start = 0
        for data in anomalous_data:
            if page_start % RECORDS_PER_PAGE == 0:
                if page != 1:
                    # Close the previous page
                    html_file.write('</table>')
                    html_file.write(f'<div>Page {page}</div>')
                # Start a new page
                html_file.write('<table border="1"><tr><th>Date and Time</th><th>Source</th><th>Event ID</th><th>Task Category</th></tr>')
                page += 1
            html_file.write('<tr>')
            html_file.write(f'<td>{data["Date and Time"]}</td>')
            html_file.write(f'<td>{data["Source"]}</td>')
            html_file.write(f'<td>{data["Event ID"]}</td>')
            html_file.write(f'<td>{data["Task Category"]}</td>')
            html_file.write('</tr>')
            page_start += 1

        # Close the last page
        html_file.write('</table>')

        # Add JavaScript for pagination
        html_file.write('<script>')
        html_file.write('function changePage(direction) {')
        html_file.write('  var page = parseInt(document.getElementById("currentPage").textContent);')
        html_file.write('  if (direction === "prev" && page > 1) {')
        html_file.write('    page--;')
        html_file.write('  } else if (direction === "next") {')
        html_file.write('    page++;')
        html_file.write('  }')
        html_file.write('  var tables = document.querySelectorAll("table");')
        html_file.write('  for (var i = 0; i < tables.length; i++) {')
        html_file.write('    tables[i].style.display = "none";')
        html_file.write('  }')
        html_file.write('  tables[page - 1].style.display = "table";')
        html_file.write('  document.getElementById("currentPage").textContent = page;')
        html_file.write('}')
        html_file.write('</script>')

        # Add pagination controls
        html_file.write('<div>Page <span id="currentPage">1</span></div>')
        html_file.write('<button onclick="changePage(\'prev\')">Previous</button>')
        html_file.write('<button onclick="changePage(\'next\')">Next</button>')

        # Write the HTML footer
        html_file.write('</body></html>')

if __name__ == "__main__":
    # Retrieve data from CSV file
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        # Train the anomaly detection model
        anomaly_model = train_anomaly_detection_model(all_data)

        # Identify anomalous events
        anomalies = identify_anomalies(all_data, anomaly_model)

        # Filter anomalous data
        anomalous_data = [data for data, is_anomaly in zip(all_data, anomalies) if is_anomaly == -1]

        # Create an HTML file to display the anomalous data with pagination
        output_file = 'Anomalous_Activity.html'
        create_html_page(anomalous_data, output_file)

        print(f"Anomalous activity has been saved to {output_file}. Open this file in a web browser to view the data with pagination.")
