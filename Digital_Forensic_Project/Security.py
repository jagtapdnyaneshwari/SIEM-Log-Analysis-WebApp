import csv
import pandas as pd
from datetime import datetime
import base64
from datetime import datetime
import re

CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\Security_logs.csv'  
RECORDS_PER_PAGE = 10

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

def replace_line_breaks(text):
    return text.replace('\n', '|')

def restore_line_breaks(text):
    return text.replace('|', '\n')

if __name__ == "__main__":
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        csv_output_file = 'Security_Logs.csv'
        with open(csv_output_file, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=all_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(all_data)
        output_file = 'Security_Logs.html'

        with open(output_file, 'w') as html_file:
            html_file.write('<html><head><title>Security Events Logs</title></head><body>')
            html_file.write(f'<a href="{csv_output_file}" class="download-button" download="{csv_output_file}">Download CSV</a>')
            html_file.write('<h1>Security Event Logs:</h1>')
            html_file.write('<table border="1"><tr><th>Sr. No.</th><th>Date and Time</th><th>Source</th><th>Event ID</th><th>Task Category</th><th>Description</th></tr>')

            for i, data in enumerate(all_data, start=1):
                html_file.write('<tr>')
                html_file.write(f'<td>{i}</td>')  
                date_time = datetime.strptime(data["Date and Time"], "%m-%d-%Y %H:%M")
                formatted_date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
                keywords = data.get("Keywords", "")
                description = replace_line_breaks(data.get("Description", ""))
                html_file.write(f'<td>{formatted_date_time}</td>')
                html_file.write(f'<td>{data["Source"]}</td>')
                html_file.write(f'<td>{data["Event ID"]}</td>')
                html_file.write(f'<td>{data["Task Category"]}</td>')
                html_file.write(f'<td>{description}</td>')
                html_file.write('</tr>')
            html_file.write('</table>')
            html_file.write('</body></html>')
        print(f"Data has been saved to {output_file} and {csv_output_file}. Open the HTML file in a web browser to view and download the data.")
