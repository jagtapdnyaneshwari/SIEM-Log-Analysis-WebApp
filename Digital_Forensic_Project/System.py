import csv

CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\System.csv'  

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

if __name__ == "__main__":
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        output_file = 'System_logs.html'

        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write('<html><head><title>System Logs</title></head><body>')

            html_file.write('<a href="#" onclick="downloadCSV()" class="download-button-top" download="System_logs.csv">Download CSV</a>')

            html_file.write('<h1>System Event Logs:</h1>')
            html_file.write('<table border="1"><tr><th>Sr. No.</th><th>Date and Time</th><th>Source</th><th>Event ID</th><th>Task Category</th><th>Description</th></tr>')

            for idx, data in enumerate(all_data, start=1):
                html_file.write('<tr>')
                html_file.write(f'<td>{idx}</td>')
                html_file.write(f'<td>{data["Date and Time"]}</td>')
                html_file.write(f'<td>{data["Source"]}</td>')
                html_file.write(f'<td>{data["Event ID"]}</td>')
                html_file.write(f'<td>{data["Task Category"]}</td>')
                html_file.write(f'<td>{data["Description"]}</td>')
                html_file.write('</tr>')

            html_file.write('</table>')

            # Add JavaScript for CSV download
            html_file.write('<script>')
            html_file.write('function downloadCSV() {')
            html_file.write('  var csv = [];')
            html_file.write('  var rows = document.querySelectorAll("table tr");')
            html_file.write('  for (var i = 0; i < rows.length; i++) {')
            html_file.write('    var row = [], cols = rows[i].querySelectorAll("td, th");')
            html_file.write('    for (var j = 0; j < cols.length; j++) ')
            html_file.write('      row.push(cols[j].innerText);')
            html_file.write('    csv.push(row.join(","));')
            html_file.write('  }')
            html_file.write('  var csvContent = "data:text/csv;charset=utf-8,%EF%BB%BF" + csv.join("\\n");')
            html_file.write('  var encodedUri = encodeURI(csvContent);')
            html_file.write('  var link = document.createElement("a");')
            html_file.write('  link.setAttribute("href", encodedUri);')
            html_file.write('  link.setAttribute("download", "System_logs.csv");')
            html_file.write('  document.body.appendChild(link);')
            html_file.write('  link.click();')
            html_file.write('}')
            html_file.write('</script>')
            html_file.write('</body></html>')

        print(f"Data has been saved to {output_file}. Open this file in a web browser to view the data.")
