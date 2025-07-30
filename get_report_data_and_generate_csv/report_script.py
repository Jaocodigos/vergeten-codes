# This script has only one objective: receive all reports and replace bad values.
import os
import requests
import csv


issuer = os.environ.get('ISSUER')
path = os.environ.get('FEATURE_PATH')
username = os.environ.get('USER')
password = os.environ.get('PASSWORD')


def verify_envs():
    if not issuer:
        print("Issuer not found. Please insert in environment variables.")
        exit("Environment not found.")
    elif not path:
        print("Path not found. Please insert in environment variables.")
        exit("Environment not found.")
    elif not username:
        print("User not found. Please insert in environment variables.")
        exit("Environment not found.")
    elif not password:
        print("User password not found. Please insert in environment variables.")
        exit("Environment not found.")


# Create a csv file and insert report data.
def convert_to_csv(report_data):
    with open("response.csv", mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in report_data:
            for key in row.keys():
                csv_writer.writerow([f"{row.get(key)}"])


# Request to reports route
def get_reports():
    params = dict(
        limit=0
    )
    auth = requests.auth.HTTPBasicAuth(username, password)
    response = requests.get(f'https://{issuer}/{path}', auth=auth, params=params, verify=False)
    response = response.json()
    return response


def main():
    verify_envs()
    try:
        report_data = get_reports()
        convert_to_csv(report_data)
        print("CSV generated!")
    except Exception as e:
        print(f"Error while running report script: {e}")
        exit("Aborting operation..")


if __name__ == '__main__':
    main()
