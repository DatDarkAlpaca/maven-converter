import csv


def write_csv_maven(filepath: str, maven_data: dict[str, list]):
    headers = maven_data.keys()

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(headers)

        for row in zip(*maven_data.values()):
            writer.writerow(row)
