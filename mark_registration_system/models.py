from django.db import models

class MarkEntry(models.Model):
    module_code = models.CharField(max_length=10, verbose_name="Module Code")  # Code for the module (e.g., CS101)
    module_name = models.CharField(max_length=100, verbose_name="Module Name")  # Name of the module (e.g., Computer Science)
    coursework1_mark = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Coursework 1 Mark")  # Marks for coursework 1
    coursework2_mark = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Coursework 2 Mark")  # Marks for coursework 2
    coursework3_mark = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Coursework 3 Mark")  # Marks for coursework 3
    student_id = models.CharField(max_length=20, verbose_name="Student ID")  # Unique ID for the student
    student_name = models.CharField(max_length=100, verbose_name="Student Name")  # Name of the student
    date_of_entry = models.DateField(verbose_name="Date of Entry")  # Date when marks were entered
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], verbose_name="Gender")  # Gender of the student

    def __str__(self):
        return f"{self.student_name} - {self.module_name}"
