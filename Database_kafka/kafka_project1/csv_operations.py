import csv

def write_to_csv(filename, bid):
    # Open the file in append mode. 'a+' allows reading and appending.
    with open(filename, 'a+', newline='') as f:
        # Create a CSV writer object
        writer = csv.writer(f)

        # Move to the beginning of the file to check if it's empty
        f.seek(0)
        # If the file is empty (no lines), write the header row
        if len(f.readlines()) == 0:
            writer.writerow(['name', 'price', 'bid_ts'])

        # Move back to the end of the file for appending new data
        f.seek(0, 2)
        # Write the bid data (a dictionary) into the CSV file
        writer.writerow([bid['name'], bid['price'], bid['bid_ts']])
