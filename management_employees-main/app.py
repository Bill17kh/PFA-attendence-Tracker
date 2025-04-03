import customtkinter as ctk
from datetime import datetime
import mysql.connector

class AttendanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",        # Use your MySQL username
            password="",        # Use your MySQL password
            database="attendance_tracker"
        )
        self.cursor = self.conn.cursor()

        self.title("Employees Attendance Tracker")
        self.geometry("800x600")

        # Set the theme and color scheme
        ctk.set_appearance_mode("blue")
        ctk.set_default_color_theme("green")

        # Initialize data structures
        self.employees = self.load_employees()
        self.departments = self.load_departments()
        self.attendance = self.load_attendance()

        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_employees = self.tabview.add("Employees")
        self.tab_departments = self.tabview.add("Departments")
        self.tab_attendance = self.tabview.add("Mark Attendance")
        self.tab_report = self.tabview.add("Attendance Report")

        self.setup_employees_tab()
        self.setup_departments_tab()
        self.setup_attendance_tab()
        self.setup_report_tab()

    def setup_employees_tab(self):
        frame = ctk.CTkFrame(self.tab_employees)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Add New Employee", font=("Arial", 16, "bold")).pack(pady=10)

        self.first_name_entry = ctk.CTkEntry(frame, placeholder_text="First Name")
        self.first_name_entry.pack(pady=5)

        self.last_name_entry = ctk.CTkEntry(frame, placeholder_text="Last Name")
        self.last_name_entry.pack(pady=5)

        add_button = ctk.CTkButton(frame, text="Add Employee", command=self.add_employee)
        add_button.pack(pady=10)

        self.employees_list = ctk.CTkTextbox(frame, height=200)
        self.employees_list.pack(pady=10, fill="both", expand=True)

        self.update_employees_list()

    def setup_departments_tab(self):
        frame = ctk.CTkFrame(self.tab_departments)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Add New Department", font=("Arial", 16, "bold")).pack(pady=10)

        self.dept_entry = ctk.CTkEntry(frame, placeholder_text="Department Name")
        self.dept_entry.pack(pady=5)

        add_button = ctk.CTkButton(frame, text="Add Department", command=self.add_department)
        add_button.pack(pady=10)

        self.depts_list = ctk.CTkTextbox(frame, height=200)
        self.depts_list.pack(pady=10, fill="both", expand=True)

        self.update_departments_list()

    def setup_attendance_tab(self):
        frame = ctk.CTkFrame(self.tab_attendance)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Mark Attendance", font=("Arial", 16, "bold")).pack(pady=10)

        self.dept_select = ctk.CTkOptionMenu(frame, values=self.get_departments())
        self.dept_select.pack(pady=5)

        self.employees_select = ctk.CTkOptionMenu(frame, values=self.get_employees())
        self.employees_select.pack(pady=5)

        mark_in_button = ctk.CTkButton(frame, text="Check-In", command=self.check_in)
        mark_in_button.pack(pady=10)

        mark_out_button = ctk.CTkButton(frame, text="Check-Out", command=self.check_out)
        mark_out_button.pack(pady=10)

        self.attendance_list = ctk.CTkTextbox(frame, height=200)
        self.attendance_list.pack(pady=10, fill="both", expand=True)

        self.update_attendance_list()

    def setup_report_tab(self):
        frame = ctk.CTkFrame(self.tab_report)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Attendance Report", font=("Arial", 16, "bold")).pack(pady=10)

        self.report_employees_select = ctk.CTkOptionMenu(frame, values=self.get_employees())
        self.report_employees_select.pack(pady=5)

        report_button = ctk.CTkButton(frame, text="Generate Report", command=self.generate_report)
        report_button.pack(pady=10)

        self.report_text = ctk.CTkTextbox(frame, height=300)
        self.report_text.pack(pady=10, fill="both", expand=True)

    def add_employee(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        if first_name and last_name:
            employee_id = f"E{len(self.employees) + 1:03d}"
            self.cursor.execute(
                "INSERT INTO employes (employes_id, first_name, last_name) VALUES (%s, %s, %s)",
                (employee_id, first_name, last_name)
            )
            self.conn.commit()
            self.employees.append((employee_id, first_name, last_name))
            self.update_employees_list()
            self.first_name_entry.delete(0, 'end')
            self.last_name_entry.delete(0, 'end')
            self.update_employees_select()

    def add_department(self):
        dept_name = self.dept_entry.get()
        if dept_name:
            dept_id = f"D{len(self.departments) + 1:03d}"
            self.cursor.execute(
                "INSERT INTO departements (dept_id, dept_name) VALUES (%s, %s)",
                (dept_id, dept_name)
            )
            self.conn.commit()
            self.departments.append((dept_id, dept_name))
            self.update_departments_list()
            self.dept_entry.delete(0, 'end')
            self.update_department_select()

    def check_in(self):
        dept_name = self.dept_select.get()
        employee_name = self.employees_select.get()
        if dept_name and employee_name:
            timestamp = datetime.now()
            employee_id = self.get_employee_id(employee_name)
            dept_id = self.get_department_id(dept_name)
            self.cursor.execute(
                "SELECT * FROM attendance WHERE employes_id = %s AND dept_id = %s AND timestamp IS NOT NULL AND check_out IS NULL",
                (employee_id, dept_id)
            )
            existing_record = self.cursor.fetchone()
            if not existing_record:
                # Insert a new check-in record
                self.cursor.execute(
                    "INSERT INTO attendance (dept_id, employes_id, timestamp) VALUES (%s, %s, %s)",
                    (dept_id, employee_id, timestamp)
                )
                self.conn.commit()
                self.update_attendance_list()

    def check_out(self):
        dept_name = self.dept_select.get()
        employee_name = self.employees_select.get()
        if dept_name and employee_name:
            timestamp = datetime.now()
            employee_id = self.get_employee_id(employee_name)
            dept_id = self.get_department_id(dept_name)
            self.cursor.execute(
                "SELECT * FROM attendance WHERE employes_id = %s AND dept_id = %s AND timestamp IS NOT NULL AND check_out IS NULL",
                (employee_id, dept_id)
            )
            existing_record = self.cursor.fetchone()
            if existing_record:
                # Update check-out time if check-in exists
                self.cursor.execute(
                    "UPDATE attendance SET check_out = %s WHERE employes_id = %s AND dept_id = %s AND check_out IS NULL",
                    (timestamp, employee_id, dept_id)
                )
                self.conn.commit()
                self.update_attendance_list()

    def generate_report(self):
        employee_name = self.report_employees_select.get()
        if employee_name:
            employee_id = self.get_employee_id(employee_name)
            report = f"Attendance Report for {employee_name}:\n\n"
            self.cursor.execute(
                "SELECT dept_name, timestamp, check_out FROM attendance a JOIN departements d ON a.dept_id = d.dept_id WHERE a.employes_id = %s",
                (employee_id,)
            )
            for record in self.cursor.fetchall():
                dept_name, check_in, check_out = record
                check_in_str = check_in.strftime("%Y-%m-%d %H:%M:%S") if check_in else "N/A"
                check_out_str = check_out.strftime("%Y-%m-%d %H:%M:%S") if check_out else "N/A"
                report += f"Dept: {dept_name}, Check-In: {check_in_str}, Check-Out: {check_out_str}\n"
            self.report_text.delete("1.0", "end")
            self.report_text.insert("1.0", report)

    def update_employees_list(self):
        self.employees_list.delete("1.0", "end")
        for employee in self.employees:
            self.employees_list.insert("end", f"{employee[1]} {employee[2]} ({employee[0]})\n")

    def update_departments_list(self):
        self.depts_list.delete("1.0", "end")
        for dept in self.departments:
            self.depts_list.insert("end", f"{dept[1]} ({dept[0]})\n")

    def update_attendance_list(self):
        self.attendance_list.delete("1.0", "end")
        self.cursor.execute("SELECT e.first_name, e.last_name, d.dept_name, a.timestamp, a.check_out FROM attendance a JOIN employes e ON a.employes_id = e.employes_id JOIN departements d ON a.dept_id = d.dept_id")
        for record in self.cursor.fetchall():
            first_name, last_name, dept_name, check_in, check_out = record
            check_in_str = check_in.strftime("%Y-%m-%d %H:%M:%S") if check_in else "N/A"
            check_out_str = check_out.strftime("%Y-%m-%d %H:%M:%S") if check_out else "N/A"
            self.attendance_list.insert("end", f"{first_name} {last_name} - {dept_name}: Check-In: {check_in_str}, Check-Out: {check_out_str}\n")

    def update_employees_select(self):
        self.employees_select.configure(values=self.get_employees())
        self.report_employees_select.configure(values=self.get_employees())

    def update_department_select(self):
        self.dept_select.configure(values=self.get_departments())

    def get_employees(self):
        self.cursor.execute("SELECT CONCAT(first_name, ' ', last_name) FROM employes")
        return [row[0] for row in self.cursor.fetchall()]

    def get_departments(self):
        self.cursor.execute("SELECT dept_name FROM departements")
        return [row[0] for row in self.cursor.fetchall()]

    def load_employees(self):
        self.cursor.execute("SELECT employes_id, first_name, last_name FROM employes")
        return self.cursor.fetchall()

    def load_departments(self):
        self.cursor.execute("SELECT dept_id, dept_name FROM departements")
        return self.cursor.fetchall()

    def load_attendance(self):
        self.cursor.execute("SELECT dept_id, employes_id, timestamp, check_out FROM attendance")
        return self.cursor.fetchall()

    def get_employee_id(self, full_name):
        self.cursor.execute("SELECT employes_id FROM employes WHERE CONCAT(first_name, ' ', last_name) = %s", (full_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_department_id(self, dept_name):
        self.cursor.execute("SELECT dept_id FROM departements WHERE dept_name = %s", (dept_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

if __name__ == "__main__":
    app = AttendanceApp()
    app.mainloop()
