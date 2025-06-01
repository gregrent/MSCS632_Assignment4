#################################################
# MSCS 532 Assignment 4
# Author: Gregory Renteria
# Employee Scheduler implementation in Python.
#################################################

import tkinter as tk
from tkinter import messagebox, ttk
import random
from collections import defaultdict

# Constants
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
SHIFTS = ['Morning', 'Afternoon', 'Evening']
MAX_DAYS_PER_EMPLOYEE = 5
MIN_EMPLOYEES_PER_SHIFT = 2

# Data storage
employee_preferences = defaultdict(lambda: {day: {} for day in DAYS})
schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
employee_workdays = defaultdict(int)

def add_preference():
    name = name_entry.get()
    day = day_combobox.get()
    shift = shift_combobox.get()
    priority = priority_combobox.get()
    
    if name and day and shift and priority:
        priority = int(priority)
        existing_priorities = employee_preferences[name][day].values()
        if priority in existing_priorities:
            messagebox.showwarning("Duplicate", f"Priority {priority} already assigned for {name} on {day}.")
        else:
            employee_preferences[name][day][shift] = priority
            messagebox.showinfo("Success", f"{name} prefers {shift} on {day} with priority {priority}")
    else:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")

def generate_schedule():
    global schedule, employee_workdays
    schedule = {day: {shift: [] for shift in SHIFTS} for day in DAYS}
    employee_workdays = defaultdict(int)

    for day in DAYS:
        assigned_today = set()
        for priority_level in [1, 2, 3]:
            for shift in SHIFTS:
                for employee in employee_preferences:
                    if employee in assigned_today or employee_workdays[employee] >= MAX_DAYS_PER_EMPLOYEE:
                        continue
                    prefs = employee_preferences[employee][day]
                    if prefs.get(shift) == priority_level and len(schedule[day][shift]) < MIN_EMPLOYEES_PER_SHIFT:
                        schedule[day][shift].append(employee)
                        employee_workdays[employee] += 1
                        assigned_today.add(employee)

        # Fill remaining slots randomly
        for shift in SHIFTS:
            while len(schedule[day][shift]) < MIN_EMPLOYEES_PER_SHIFT:
                available_employees = [e for e in employee_preferences if employee_workdays[e] < MAX_DAYS_PER_EMPLOYEE and e not in assigned_today]
                if not available_employees:
                    break
                chosen = random.choice(available_employees)
                schedule[day][shift].append(chosen)
                employee_workdays[chosen] += 1
                assigned_today.add(chosen)

    display_schedule()

def display_schedule():
    output_text.delete('1.0', tk.END)
    for day in DAYS:
        output_text.insert(tk.END, f"{day}:\n")
        for shift in SHIFTS:
            employees = ', '.join(schedule[day][shift])
            output_text.insert(tk.END, f"  {shift}: {employees}\n")
        output_text.insert(tk.END, "\n")

# GUI Setup
root = tk.Tk()
root.title("Employee Scheduler with Preferences")

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=10)

tk.Label(input_frame, text="Employee Name").grid(row=0, column=0)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Day").grid(row=1, column=0)
day_combobox = ttk.Combobox(input_frame, values=DAYS, state="readonly")
day_combobox.grid(row=1, column=1)

tk.Label(input_frame, text="Shift").grid(row=2, column=0)
shift_combobox = ttk.Combobox(input_frame, values=SHIFTS, state="readonly")
shift_combobox.grid(row=2, column=1)

tk.Label(input_frame, text="Priority (1-3)").grid(row=3, column=0)
priority_combobox = ttk.Combobox(input_frame, values=[1, 2, 3], state="readonly")
priority_combobox.grid(row=3, column=1)

add_button = tk.Button(input_frame, text="Add Preference", command=add_preference)
add_button.grid(row=4, column=0, columnspan=2, pady=5)

# Schedule Button
schedule_button = tk.Button(root, text="Generate Schedule", command=generate_schedule)
schedule_button.pack(pady=5)

# Output Text
output_text = tk.Text(root, height=20, width=60)
output_text.pack(padx=10, pady=10)

# Run the app
root.mainloop()
