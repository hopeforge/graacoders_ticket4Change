import csv


class Exporter:

    def write_csv(self, path, file_name, dictionary):
        full_file_path = path + '\\' + file_name + '.csv'
        try:
            with open(full_file_path, mode='a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=dictionary.keys(), delimiter=';')
                writer.writerow(dictionary)
            csv_file.close()
        except IOError:
            csv_file.close()
            print("I/O error")