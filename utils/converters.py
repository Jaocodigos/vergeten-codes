import csv

# Receive a list of dicts and convert to a csv
def convert_to_csv(filename: str, data: list):
    with open(f"{filename}.csv", mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data:
            for key in row.keys():
                csv_writer.writerow([f"{row.get(key)}"])


def convert_file_to_list(filename: str, file_type: str):
    data = []
    with open(f"{filename}.{file_type}", "r") as file:
        for row in file:
            data.append(row)
    return data

def convert_file_to_dict(filename:str, file_type: str, keys: list):
    data = []
    row_data = None
    try:

        with open(f"{filename}.{file_type}", "r") as file:
            try:

                for row in file:
                    row = row[:-1]
                    row_data = row_data
                    values = row.split(",")

                    if len(values) < len(keys):
                        print()
                        continue

                    i = 0
                    payload = dict()
                    while i < len(keys):
                        payload[keys[i]] = values[i]
                        i = i + 1
                    data.append(payload)

            except Exception as e:
                print(f"Failed to manipulate row {row_data}. Error: {str(e)}")

    except FileNotFoundError:
        print(f"File {filename} not found. Aborting.")
        return exit("File not found.")

    except Exception as e:
        print(f"Failed to manipulate file {filename}. Error: {str(e)}")

    return data