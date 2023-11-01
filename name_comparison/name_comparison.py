import os


def generate_response_file(data, filename='comparison_response'):
    with open(f'{filename}.txt', "w") as response_file:
        for row in data:
            response_file.write(row)


def get_file(filename, file_type):
    data = []
    with open(f"{filename}.{file_type}", "r") as file:
        for row in file:
            data.append(row)
    return data


def main():
    response_type = os.environ.get('RESPONSE_TYPE') or 'file'
    get_difference = os.environ.get('GET_DIFFERENCE') or False
    file_one_name = os.environ.get('FIRST_FILE') or 'first'
    file_two_name = os.environ.get('SECOND_FILE') or 'second'
    file_types = os.environ.get('FILE_TYPES') or 'txt'
    try:
        file_one = get_file(file_one_name, file_types)
        file_two = get_file(file_two_name, file_types)
        response = list(filter(lambda x: x in file_two, file_one))
        if get_difference:
            difference = list(filter(lambda x: x not in file_two, file_one))
        if response_type == 'print':
            print(*response)
            print("Finished!")
        elif response_type == 'file':
            generate_response_file(response)
            if get_difference:
                generate_response_file(difference, 'different_names')
            print("Finished!")
        else:
            exit("Invalid response type.")
    except Exception as e:
        exit(f"An error occurred while comparing names: {e}")


if __name__ == "__main__":
    main()
