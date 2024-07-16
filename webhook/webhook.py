from html.parser import HTMLParser
import requests
import datetime
today = datetime.date.today()


# HTML parser: call MyHTMLParser(classname) to filter values by a specific class name.
class MyHTMLParser(HTMLParser):
    def __init__(self, target_class):
        super().__init__()
        self.target_class = target_class
        self.capturing = False
        self.data_list = []

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if attr[0] == "class" and self.target_class in attr[1].split():
                self.capturing = True

    def handle_endtag(self, tag):
        if self.capturing:
            self.capturing = False

    def handle_data(self, data):
        if self.capturing:
            self.data_list.append(data)


def load_file_and_get_version():
    version = None
    try:
        with open("version.txt") as file:
            for line in file:
                line = line.strip()
                if line and line.startswith("VARIABLE") and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    version = value
    except Exception as e:
        print(f"Error reading txt file: {e}")
    return version


def save_version_in_file(version):
    with open("file.txt", "w") as file:
        file.write(f"{version}")  # Write as you want


def main():
    # Get version from Chrome Web Store and compare it.
    actual_version = load_file_and_get_version()
    page = requests.get('')  # Your request to get some info
    tree = MyHTMLParser("N3EXSc")
    tree.feed(page.content.decode("utf-8"))
    version = tree.data_list
    if len(version) > 0:
        if actual_version == version[0]:
            print(f"{today} {version[0]} - Up to date!")
        else:
            # Save the new version from CWS and notify chats.
            url = "" # GCW URL here.
            app_message = {"text": ""} # Message
            message_headers = {"Content-Type": "application/json; charset=UTF-8"}
            requests.post(url, json=app_message, headers=message_headers)
            save_version_in_file(version[0])
            print(f"{today} {version}")
    else:
        print(f"{today} {version} - Version not found.")


if __name__ == '__main__':
    main()
