import csv


def read_csv():
    with open('marks_data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        return list(csv_reader)


def write_csv(data):
    fieldnames = ['module_code', 'module_name', 'coursework1_mark', 'coursework2_mark', 'coursework3_mark', 'student_id', 'student_name', 'date_of_entry', 'gender']
    with open('marks_data.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:  # write header if the file is empty
            writer.writeheader()
        writer.writerow(data)
        

def search_marks_by_module(module_code):
    data = read_csv()
    return [row for row in data if row['module_code'] == module_code]
