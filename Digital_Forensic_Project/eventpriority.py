import csv
import pandas as pd

CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\Application_logs.csv'  

def retrieve_data_from_csv(csv_file):
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

def prioritize_events(data):
    priority_levels = []

    for event in data:
        if "Event Message" in event and "error" in event["Event Message"].lower():
            priority_levels.append("High")
        elif "Event Message" in event and "warning" in event["Event Message"].lower():
            priority_levels.append("Medium")
        else:
            priority_levels.append("Low")
    return priority_levels

def create_html_page(data, priority_levels, output_file, filter_priority):
    combined_data = list(zip(data, priority_levels))
    filtered_data = [(event, priority) for event, priority in combined_data if priority == filter_priority]

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write('<html><head><title>Microsoft Windows Logs</title>')
        
        # JavaScript for dynamic filtering
        html_file.write('''
        <script>
            function filterData(priority) {
                var rows = document.getElementsByTagName('tr');
                for (var i = 1; i < rows.length; i++) {
                    var cells = rows[i].getElementsByTagName('td');
                    var cellValue = cells[cells.length - 1].innerHTML; // Get the priority cell value
                    rows[i].style.display = (cellValue === priority) ? '' : 'none';
                }
            }
        </script>
        </head><body>''')

        html_file.write(f'<button onclick="filterData(\'{filter_priority}\')">Filter {filter_priority} Priority</button>')

        html_file.write(f'<h1>Microsoft Windows Logs - {filter_priority} Priority:</h1>')
        html_file.write('<table border="1"><tr>')
        
        for column_name in data[0].keys():
            html_file.write(f'<th>{column_name}</th>')
        
        html_file.write('<th>Priority</th></tr>')

        for event, priority in filtered_data:
            html_file.write('<tr>')
            for column_name in event.keys():
                html_file.write(f'<td>{event[column_name]}</td>')
            html_file.write(f'<td>{priority}</td>')
            html_file.write('</tr>')

        html_file.write('</table>')
        html_file.write('</body></html>')

if __name__ == "__main__":
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        priority_levels = prioritize_events(all_data)
        for priority in set(priority_levels):
            output_file = f'{priority}_Priority_Windows_Logs.html'
            create_html_page(all_data, priority_levels, output_file, filter_priority=priority)
            print(f"Data has been saved to {output_file}. Open this file in a web browser to view the filtered data for {priority} priority.")


