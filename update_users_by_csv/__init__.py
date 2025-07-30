import requests
from os import getenv

from utils.converters import convert_to_csv, convert_file_to_dict
from utils.base_steps import verify_envs

issuer = getenv('CSV_FILE')
path = getenv('ENDPOINT')
username = getenv('USER')
password = getenv('PASSWORD')


def update_data(item: dict):
    try:

        auth = requests.auth.HTTPBasicAuth(username, password)
        response = requests.put(path, json=item, auth=auth, verify=False)
        if response.status_code == 200:
            return True, ""

        print(f"Invalid status code updating item {item}. Response {response.text}")

        return False, response.text

    except Exception as e:

        print(f"Failed to request update for item {item}. Error {str(e)}")
        return False, str(e)



if __name__ == "__main__":

    verify_envs(csv_file=issuer, endpoint=path, username=username, password=password)

    updated = list()
    not_updated = list()

    # Example for keys: ["username", "email"]
    items = convert_file_to_dict("example", "txt", ["username"])

    for i in items:

        update_response, error = update_data(i)
        if update_response:

            print(f"Update success for item {i}. Adding to updated list.")
            updated.append(i)
            continue

        print(f"Adding item {i} to not updated list.")
        i["error"] = error
        not_updated.append(i)

    print("Finished update process.")
    print(f"Success: {len(updated)}")
    print(f"Failed: {len(not_updated)}")
    print("Creating csv files.")

    convert_to_csv("success_update", updated)
    convert_to_csv("failed_update", not_updated)

