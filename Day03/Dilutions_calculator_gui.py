import tkinter as tk
from tkinter import messagebox
from dilution_lib import Calculation_of_C1, Calculation_of_V1, Calculation_of_C2, Calculation_of_V2

class DilutionCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilution Calculator")

        # Choice
        tk.Label(root, text="Choose what to calculate:").grid(row=0, column=0, columnspan=2)
        self.choice_var = tk.StringVar(value="1")
        choices = [("1: C1 (Initial concentration)", "1"),
                   ("2: V1 (Initial volume)", "2"),
                   ("3: C2 (Final concentration)", "3"),
                   ("4: V2 (Final volume)", "4")]
        for i, (text, val) in enumerate(choices):
            tk.Radiobutton(root, text=text, variable=self.choice_var, value=val).grid(row=i+1, column=0, columnspan=2, sticky="w")

        # Inputs
        tk.Label(root, text="Value 1:").grid(row=5, column=0)
        self.val1_entry = tk.Entry(root)
        self.val1_entry.grid(row=5, column=1)

        tk.Label(root, text="Value 2:").grid(row=6, column=0)
        self.val2_entry = tk.Entry(root)
        self.val2_entry.grid(row=6, column=1)

        tk.Label(root, text="Value 3:").grid(row=7, column=0)
        self.val3_entry = tk.Entry(root)
        self.val3_entry.grid(row=7, column=1)

        # Button
        tk.Button(root, text="Calculate", command=self.calculate).grid(row=8, column=0, columnspan=2)

        # Result
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=9, column=0, columnspan=2)

        # Instructions
        instructions = """
Instructions:
For choice 1: Enter V1, C2, V2
For choice 2: Enter C1, C2, V2
For choice 3: Enter C1, V1, V2
For choice 4: Enter C1, V1, C2
All values must be numbers.
        """
        tk.Label(root, text=instructions, justify="left").grid(row=10, column=0, columnspan=2)

    def calculate(self):
        choice = self.choice_var.get()
        try:
            val1 = float(self.val1_entry.get())
            val2 = float(self.val2_entry.get())
            val3 = float(self.val3_entry.get())
        except ValueError:
            messagebox.showerror("Error", "All values must be numbers.")
            return

        result = None
        if choice == "1":
            V1, C2, V2 = val1, val2, val3
            result = Calculation_of_C1(C2, V2, V1)
            if result is not None:
                self.result_label.config(text=f"C1 = {result}\nInitial concentration: {result} Molarity units.")
        elif choice == "2":
            C1, C2, V2 = val1, val2, val3
            result = Calculation_of_V1(C1, C2, V2)
            if result is not None:
                self.result_label.config(text=f"V1 = {result}\nInitial volume: {result} volume units.")
        elif choice == "3":
            C1, V1, V2 = val1, val2, val3
            result = Calculation_of_C2(C1, V1, V2)
            if result is not None:
                self.result_label.config(text=f"C2 = {result}\nFinal concentration: {result} Molarity units.")
        elif choice == "4":
            C1, V1, C2 = val1, val2, val3
            result = Calculation_of_V2(C1, V1, C2)
            if result is not None:
                self.result_label.config(text=f"V2 = {result}\nFinal volume: {result} Volume units.")
        if result is None:
            self.result_label.config(text="Error: Invalid input (e.g., division by zero).")

if __name__ == "__main__":
    root = tk.Tk()
    app = DilutionCalculatorGUI(root)
    root.mainloop()