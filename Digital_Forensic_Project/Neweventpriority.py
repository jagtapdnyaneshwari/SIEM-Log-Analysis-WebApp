import csv
import pandas as pd

# MongoDB configuration
MONGO_HOST = 'mongodb://localhost:27017'  # MongoDB host
MONGO_PORT = 27017       # MongoDB port
MONGO_DB_NAME = 'Microsoft_Windows'  # MongoDB database
MONGO_COLLECTION_NAME = 'System_Logs'  # MongoDB collection

def retrieve_data_from_csv(csv_file):
    """Retrieves data from the specified CSV file and returns it as a list of dictionaries."""
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
    """
    Prioritizes events based on Event ID and adds the 'priority' column to each event.
    """
    for event in data:
        # Check if the key "Event ID" exists and the value is non-empty before accessing it
        if "Event ID" in event and event["Event ID"]:
            try:
                event_id = int(event["Event ID"])
                if 100 <= event_id < 200:
                    event['priority'] = "High"
                elif 200 <= event_id < 300:
                    event['priority'] = "Medium"
                else:
                    event['priority'] = "Low"
            except ValueError:
                event['priority'] = "Invalid"
        else:
            event['priority'] = "Missing"

    return data

def create_combined_csv(data, output_file):
    # Create a DataFrame from the updated data
    combined_df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    combined_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Provide the path to your CSV file
    CSV_FILE = r'D:\\umaas\\git\\Digital_Forensic\\logs\\Application_logs.csv'

    # Retrieve data from CSV file
    all_data = retrieve_data_from_csv(CSV_FILE)

    if all_data:
        # Prioritize events based on Event ID and add the 'priority' column
        updated_data = prioritize_events(all_data)

        # Create and save the updated CSV file with the 'priority' column
        updated_output_file = 'updated_priority_events.csv'
        create_combined_csv(updated_data, updated_output_file)

        print(f"Updated data has been saved to {updated_output_file}.")
