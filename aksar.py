import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# -------------------------------
# CLASS 1: Student (Encapsulation)
# -------------------------------
class Student:
    def __init__(self, sid, name, year, modules_marks):
        self.__sid = sid
        self.__name = name
        self.__year = year
        self.__modules = modules_marks

    # Encapsulation (getters)
    def get_id(self): return self.__sid
    def get_name(self): return self.__name
    def get_year(self): return self.__year
    def get_modules(self): return self.__modules

    def calculate_average(self):
        marks = list(self.__modules.values())
        return sum(marks) / len(marks)

    def compute_result(self):
        marks = list(self.__modules.values())
        if any(m < 40 for m in marks):
            return "F"
        avg = self.calculate_average()
        if avg >= 70: return "A"
        if avg >= 60: return "B"
        if avg >= 50: return "C"
        if avg >= 40: return "D"
        return "F"

    def __str__(self):
        return f"{self.__sid} | {self.__name} | {self.__year} | {self.compute_result()}"


# -------------------------------
# CLASS 2: StudentManager (Abstraction)
# -------------------------------
class StudentManager:
    def __init__(self):
        self.students = {}

    def store_record(self, sid, name, year, modules_marks):
        self.students[sid] = Student(sid, name, year, modules_marks)

    def remove_entry(self, sid):
        self.students.pop(sid, None)

    def modify_record(self, sid, name, year, modules_marks):
        self.students[sid] = Student(sid, name, year, modules_marks)

    def get_student(self, sid):
        return self.students.get(sid)

    def get_all(self):
        return self.students


# -------------------------------
# CLASS 3: GradeHelper (Utility Class)
# -------------------------------
class GradeHelper:
    @staticmethod
    def generate_remark(grade):
        return {
            "A": "Excellent",
            "B": "Good",
            "C": "Satisfactory",
            "D": "Needs Improvement",
            "F": "Fail"
        }.get(grade, "")


# -------------------------------
# CLASS 4: StudentApp (GUI Layer)
# -------------------------------
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Calculator (OOP Version)")
        self.root.geometry("1150x650")
        self.root.configure(bg="#e8f4ff")

        self.manager = StudentManager()

        self.modules_by_year = {
            "Year 1": ["Networking", "Operating System", "Information Security", "Problem Solving & Programming"],
            "Year 2": ["Cryptography", "Algorithms & Data Structure", "Computer Forensics", "Communication & Collaboration"],
            "Year 3": ["Secure Programming", "IoT", "Contemporary Issues", "Project"],
        }

        self.pages = {}

        self.create_navbar()
        self.create_add_page()
        self.create_view_page()

        self.show_page("add")
        self.display_records()

        # Track if currently editing
        self.editing_sid = None

    def create_navbar(self):
        nav = tk.Frame(self.root, bg="#cce6ff")
        nav.pack(fill="x", pady=10)

        for text, page in [("Add Student", "add"), ("View Records", "view")]:
            lbl = tk.Label(nav, text=text, bg="#cce6ff", fg="black", font=("Arial", 12, "bold"),
                           padx=20, pady=8, cursor="hand2")
            lbl.pack(side="left", padx=20)
            lbl.bind("<Button-1>", lambda e, p=page: self.show_page(p))

    def show_page(self, page):
        for f in self.pages.values():
            f.pack_forget()
        self.pages[page].pack(fill="both", expand=True, padx=20, pady=10)

    def create_add_page(self):
        page = tk.Frame(self.root, bg="white")
        self.pages["add"] = page

        frame = tk.LabelFrame(page, text="Enter Student Details", bg="white", fg="black",
                              font=("Arial", 14, "bold"), padx=20, pady=20)
        frame.pack(pady=20, padx=20)

        tk.Label(frame, text="Student ID:", bg="white", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.sid_entry = tk.Entry(frame, width=20, font=("Arial", 12)); self.sid_entry.grid(row=0, column=1)

        tk.Label(frame, text="Name:", bg="white", font=("Arial", 12)).grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(frame, width=25, font=("Arial", 12)); self.name_entry.grid(row=0, column=3)

        tk.Label(frame, text="Year:", bg="white", font=("Arial", 12)).grid(row=0, column=4, padx=10, pady=10, sticky="e")
        self.year_var = tk.StringVar()
        year_combo = ttk.Combobox(frame, textvariable=self.year_var, values=list(self.modules_by_year.keys()), state="readonly", width=18, font=("Arial", 12))
        year_combo.grid(row=0, column=5, padx=10, pady=10)
        year_combo.bind("<<ComboboxSelected>>", self.refresh_module_list)

        self.module_labels, self.mark_entries = [], []

        for i in range(4):
            tk.Label(frame, text=f"Module {i+1}:", bg="white", font=("Arial", 12)).grid(row=i+1, column=0, padx=10, pady=10, sticky="e")
            mod_label = tk.Label(frame, text="", bg="white", fg="black", font=("Arial", 12), width=25, anchor="w", relief="solid")
            mod_label.grid(row=i+1, column=1, padx=10, pady=10)
            self.module_labels.append(mod_label)

            tk.Label(frame, text="Marks:", bg="white", font=("Arial", 12)).grid(row=i+1, column=2, padx=10, pady=10, sticky="e")
            mark_entry = tk.Entry(frame, width=10, font=("Arial", 12))
            mark_entry.grid(row=i+1, column=3, padx=10, pady=10)
            self.mark_entries.append(mark_entry)

        tk.Button(frame, text="Save Student", command=self.store_record, bg="#4caf50", fg="white",
                  width=20, font=("Arial", 12, "bold")).grid(row=5, column=0, columnspan=6, pady=15)

    def create_view_page(self):
        page = tk.Frame(self.root, bg="white")
        self.pages["view"] = page

        search_frame = tk.Frame(page, bg="white"); search_frame.pack(pady=10)
        tk.Label(search_frame, text="Search by ID or Name:", bg="white", font=("Arial", 12)).pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=25, font=("Arial", 12)); self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", bg="#2196f3", fg="white",
                  command=lambda: self.display_records(self.search_entry.get())).pack(side="left", padx=5)
        tk.Button(search_frame, text="Reset", bg="#9e9e9e", fg="white",
                  command=lambda: [self.search_entry.delete(0, tk.END), self.display_records()]).pack(side="left", padx=5)

        self.table_frame = tk.Frame(page, bg="white")
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=5)

    # ---------------- Helper Functions ----------------
    def refresh_module_list(self, *args):
        mods = self.modules_by_year.get(self.year_var.get(), [])
        for lbl, mod in zip(self.module_labels, mods):
            lbl.config(text=mod)

    def collect_student_data(self):
        sid = self.sid_entry.get().strip().upper()
        name = self.name_entry.get().strip()
        year = self.year_var.get()

        if not (sid and name and year):
            return None

        marks = []
        for e in self.mark_entries:
            try:
                val = float(e.get())
                if 0 <= val <= 100:
                    marks.append(val)
                else:
                    return None
            except:
                return None

        modules = [lbl.cget("text") for lbl in self.module_labels]
        return sid, name, year, dict(zip(modules, marks))

    def reset_fields(self):
        self.sid_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        for m in self.mark_entries:
            m.delete(0, tk.END)
        self.editing_sid = None  # reset editing mode

    # ---------------- CRUD ----------------
    def store_record(self):
        data = self.collect_student_data()
        if not data:
            messagebox.showerror("Error", "Invalid input or missing fields!")
            return

        sid, name, year, modules = data

        # FIX: Allow updating record if editing
        if self.editing_sid:
            self.manager.modify_record(sid, name, year, modules)
            messagebox.showinfo("Success", f"Student {name}'s record updated successfully!")
            self.reset_fields()
            self.display_records()
            self.show_page("view")
            return

        if self.manager.get_student(sid):
            messagebox.showerror("Error", f"Student ID '{sid}' already exists!")
            return

        self.manager.store_record(sid, name, year, modules)
        messagebox.showinfo("Success", f"Student {name} saved successfully!")
        self.reset_fields()
        self.display_records()

    def remove_entry(self, sid):
        self.manager.remove_entry(sid)
        self.display_records()

    def modify_record(self, sid):
        student = self.manager.get_student(sid)
        if not student:
            return
        self.sid_entry.delete(0, tk.END); self.sid_entry.insert(0, student.get_id())
        self.name_entry.delete(0, tk.END); self.name_entry.insert(0, student.get_name())
        self.year_var.set(student.get_year())
        self.refresh_module_list()
        for e, (_, m) in zip(self.mark_entries, student.get_modules().items()):
            e.delete(0, tk.END); e.insert(0, m)
        self.editing_sid = sid  # now editing mode ON
        self.show_page("add")

    def open_student_report(self, sid):
        student = self.manager.get_student(sid)
        if not student:
            return

        data = student.get_modules()
        report = tk.Toplevel(self.root)
        report.title("Report Card")
        report.geometry("700x500")
        report.configure(bg="white")

        tk.Label(report, text="University of Cybersecurity, London", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        tk.Label(report, text="123 University St, London, UK", font=("Arial", 12), bg="white").pack()
        tk.Label(report, text="Report Card", font=("Arial", 16, "bold"), bg="white").pack(pady=5)

        for label, value in [
            ("Student ID", student.get_id()),
            ("Name", student.get_name()),
            ("Year", student.get_year()),
            ("Date", datetime.now().strftime('%Y-%m-%d'))
        ]:
            tk.Label(report, text=f"{label}: {value}", font=("Arial", 12), bg="white").pack(anchor="w", padx=40)

        table = tk.Frame(report, bg="white"); table.pack(pady=10)
        for c, h in enumerate(["Module", "Marks", "Grade"]):
            tk.Label(table, text=h, bg="#e0f2ff", font=("Arial", 12, "bold"), width=20 if c == 0 else 10,
                     borderwidth=1, relief="solid").grid(row=0, column=c)

        for r, (mod, mark) in enumerate(data.items(), start=1):
            tk.Label(table, text=mod, width=20, borderwidth=1, relief="solid").grid(row=r, column=0)
            tk.Label(table, text=f"{mark:.2f}", width=10, borderwidth=1, relief="solid").grid(row=r, column=1)
            tk.Label(table, text="F" if mark < 40 else "A", width=10, borderwidth=1, relief="solid").grid(row=r, column=2)

        avg = student.calculate_average()
        grade = student.compute_result()
        remark = GradeHelper.generate_remark(grade)

        for label, value in [("Final Average", f"{avg:.2f}"), ("Final Grade", grade), ("Remark", remark)]:
            tk.Label(report, text=f"{label}: {value}", font=("Arial", 12, "bold"), bg="white").pack()

    def display_records(self, search_term=""):
        for w in self.table_frame.winfo_children():
            w.destroy()

        headers = ["ID", "Name", "Year", "Average", "Grade", "Actions"]
        for c, h in enumerate(headers):
            tk.Label(self.table_frame, text=h, bg="#e0f2ff", font=("Arial", 11, "bold"),
                     borderwidth=1, relief="solid", width=15).grid(row=0, column=c)

        for r, (sid, student) in enumerate(sorted(self.manager.get_all().items()), start=1):
            if search_term.lower() not in sid.lower() and search_term.lower() not in student.get_name().lower():
                continue
            avg = student.calculate_average()
            grade = student.compute_result()

            tk.Label(self.table_frame, text=sid, bg="white", width=15).grid(row=r, column=0)
            tk.Label(self.table_frame, text=student.get_name(), bg="white", width=15).grid(row=r, column=1)
            tk.Label(self.table_frame, text=student.get_year(), bg="white", width=15).grid(row=r, column=2)
            tk.Label(self.table_frame, text=f"{avg:.2f}", bg="white", width=15).grid(row=r, column=3)
            tk.Label(self.table_frame, text=grade, bg="white", width=15).grid(row=r, column=4)

            frame = tk.Frame(self.table_frame, bg="white"); frame.grid(row=r, column=5)
            tk.Button(frame, text="👁 View", bg="#2196f3", fg="white", command=lambda s=sid: self.open_student_report(s)).pack(side="left", padx=2)
            tk.Button(frame, text="✏ Edit", bg="#ff9800", fg="white", command=lambda s=sid: self.modify_record(s)).pack(side="left", padx=2)
            tk.Button(frame, text="🗑 Delete", bg="#f44336", fg="white", command=lambda s=sid: self.remove_entry(s)).pack(side="left", padx=2)


# -------------------------------
# RUN PROGRAM
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
