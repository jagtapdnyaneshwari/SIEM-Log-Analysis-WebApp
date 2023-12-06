import csv

CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\Application_logs.csv'  # CSV file path

def retrieve_data_from_csv(csv_file):
    """Fetch data from the above CSV file and returns it as a list of dictionaries."""
    data = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: The CSV file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data

if __name__ == "__main__":
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        csv_output_file = 'Application_Logs.csv'
        with open(csv_output_file, 'w', newline='', encoding='utf-8-sig') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.DictWriter(csv_file, fieldnames=all_data[0].keys())
            csv_writer.writeheader()
            
            # Write the CSV data
            csv_writer.writerows(all_data)

        output_file = 'Application_Logs.html'

        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write('<html><head><title>Application Logs</title></head><body>')
            html_file.write(f'<a href="{csv_output_file}" class="download-button" download="{csv_output_file}">Download CSV</a>')
            html_file.write('<h1>Application Logs:</h1>')
            html_file.write('<table border="1"><tr>')
            
            # Write header row dynamically
            for key in all_data[0].keys():
                html_file.write(f'<th>{key}</th>')
            html_file.write('</tr>')

            # Write data rows dynamically
            for data in all_data:
                html_file.write('<tr>')
                for key in all_data[0].keys():
                    html_file.write(f'<td>{data.get(key, "")}</td>')
                html_file.write('</tr>')
            html_file.write('</table>')

            html_file.write(f'<p><a href="{csv_output_file}" download>Download CSV</a></p>')
            html_file.write('</body></html>')
        print(f"Data has been saved to {output_file} and {csv_output_file}. Open the HTML file in a web browser to view and download the data.")
