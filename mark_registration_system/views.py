from django.shortcuts import render, redirect
import csv
from django.contrib import messages
from .forms import MarksForm  



def read_csv():
    try:
        with open('marks_data.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            return list(csv_reader)
    except FileNotFoundError:
        return []  # If the file doesn't exist yet, return an empty list

# Helper function to write data to the CSV file
def write_csv(data):
    fieldnames = ['module_code', 'module_name', 'coursework1_mark', 'coursework2_mark', 'coursework3_mark', 'student_id', 'student_name', 'date_of_entry', 'gender']
    try:
        with open('marks_data.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # If the file is empty, write the header
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        print(f"Error writing to CSV: {e}")

# Helper function to get the number of students and modules from the CSV file
def get_stats():
    data = read_csv()
    student_ids = set()
    module_codes = set()

    for row in data:
        student_ids.add(row['student_id'])
        module_codes.add(row['module_code'])

    return len(student_ids), len(module_codes)

# Home page view
def home(request):
    num_students, num_modules = get_stats()
    context = {
        'num_students': num_students,
        'num_modules': num_modules,
    }
    return render(request, 'home.html', context)

# Input Marks view (handles form submission and writes to CSV)
def input_marks(request):
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            write_csv(data)  # Write to CSV
            messages.success(request, 'Mark entry has been saved successfully.')
            return redirect('home')  # Redirect to home page after submission
    else:
        form = MarksForm()
    
    return render(request, 'input_marks.html', {'form': form})  # Render the input form

# View Marks page (handles CSV data reading and displays it based on module_code)
def view_marks(request):
    students = []
    module_code = ''
    if request.method == 'POST':
        module_code = request.POST.get('module_code')
        with open('marks_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['module_code'] == module_code:
                    # Convert coursework marks to integers before summing
                    coursework1 = int(row['coursework1_mark'])
                    coursework2 = int(row['coursework2_mark'])
                    coursework3 = int(row['coursework3_mark'])
                    total = coursework1 + coursework2 + coursework3
                    students.append({
                        'student_id': row['student_id'],
                        'student_name': row['student_name'],
                        'coursework1': coursework1,
                        'coursework2': coursework2,
                        'coursework3': coursework3,
                        'total': total
                    })

    return render(request, 'view_marks.html', {'students': students, 'module_code': module_code})

# Update Marks page (handles searching for a mark entry by module_code, student_id, and date_of_entry)
def update_marks(request):
    error = None
    mark_entry = None

    if request.method == 'POST':
        module_code = request.POST.get('module_code')
        student_id = request.POST.get('student_id')
        date_of_entry = request.POST.get('date_of_entry')

        # Search for the mark entry in the CSV
        data = read_csv()
        for row in data:
            if row['module_code'] == module_code and row['student_id'] == student_id and row['date_of_entry'] == date_of_entry:
                mark_entry = row
                break

        # If the entry is found, update it
        if mark_entry:
            # Only update if the form fields are filled in
            if 'update' in request.POST:
                mark_entry['coursework1_mark'] = request.POST.get('coursework1_mark')
                mark_entry['coursework2_mark'] = request.POST.get('coursework2_mark')
                mark_entry['coursework3_mark'] = request.POST.get('coursework3_mark')

                # Rewrite the CSV with the updated data
                fieldnames = data[0].keys()
                with open('marks_data.csv', mode='w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)

                messages.success(request, 'Mark entry updated successfully.')
                return redirect('home')  # Redirect after successful update

        else:
            error = 'Mark entry not found.'

    return render(request, 'update_marks.html', {'mark_entry': mark_entry, 'error': error})

def get_gender_distribution():
    data = read_csv()
    gender_counts = {'Male': 0, 'Female': 0, 'Other': 0}  # You can add more categories if needed
    for row in data:
        gender = row['gender']
        if gender in gender_counts:
            gender_counts[gender] += 1
    return gender_counts


# Function to get average marks for each coursework
def get_average_marks():
    data = read_csv()
    total_coursework1 = total_coursework2 = total_coursework3 = 0
    num_students = len(data)

    for row in data:
        total_coursework1 += float(row['coursework1_mark'])
        total_coursework2 += float(row['coursework2_mark'])
        total_coursework3 += float(row['coursework3_mark'])

    average_coursework1 = total_coursework1 / num_students
    average_coursework2 = total_coursework2 / num_students
    average_coursework3 = total_coursework3 / num_students

    return {
        'coursework1': average_coursework1,
        'coursework2': average_coursework2,
        'coursework3': average_coursework3
    }


# Function to get marks by module
def get_marks_by_module():
    data = read_csv()
    module_marks = {}

    for row in data:
        module_code = row['module_code']
        coursework1 = float(row['coursework1_mark'])
        coursework2 = float(row['coursework2_mark'])
        coursework3 = float(row['coursework3_mark'])

        if module_code not in module_marks:
            module_marks[module_code] = {'coursework1': [], 'coursework2': [], 'coursework3': []}

        module_marks[module_code]['coursework1'].append(coursework1)
        module_marks[module_code]['coursework2'].append(coursework2)
        module_marks[module_code]['coursework3'].append(coursework3)

    return module_marks

# Visualization page (handles visualizing data from CSV)
def visualization(request):
    data = read_csv()
    module_codes = []
    coursework1_marks = []
    coursework2_marks = []
    coursework3_marks = []

    # Aggregate data for visualization
    for row in data:
        if row['module_code'] not in module_codes:
            module_codes.append(row['module_code'])
            coursework1_marks.append(int(row['coursework1_mark']))
            coursework2_marks.append(int(row['coursework2_mark']))
            coursework3_marks.append(int(row['coursework3_mark']))
        else:
            index = module_codes.index(row['module_code'])
            coursework1_marks[index] += int(row['coursework1_mark'])
            coursework2_marks[index] += int(row['coursework2_mark'])
            coursework3_marks[index] += int(row['coursework3_mark'])

    context = {
        'module_codes': module_codes,
        'coursework1_marks': coursework1_marks,
        'coursework2_marks': coursework2_marks,
        'coursework3_marks': coursework3_marks,
    }

    gender_distribution = get_gender_distribution()
    average_marks = get_average_marks()
    marks_by_module = get_marks_by_module()

    context = {
        'gender_distribution': gender_distribution,
        'average_marks': average_marks,
        'marks_by_module': marks_by_module
    }
    return render(request, 'visualization.html', context)  