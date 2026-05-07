#To run first copy this: pip install customtkinter
#Make sure 1. Dilutions_calculator_upgrade.py and 2. dilution_lib.py are in the same folder

import customtkinter as ctk
from tkinter import messagebox
from dilution_lib import Calculation_of_C1, Calculation_of_V1, Calculation_of_C2, Calculation_of_V2

class DilutionCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilution Calculator")
        self.root.geometry("420x520")

        ctk.set_appearance_mode("light")  # "light" / "dark" / "system"
        ctk.set_default_color_theme("green")  # "blue" / "green" / "dark-blue"

        # Frame
        main_frame = ctk.CTkFrame(root, corner_radius=15)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(main_frame, text="Dilution Calculator", font=("Arial", 22, "bold"))
        title.pack(pady=10)

        # Choice
        choice_label = ctk.CTkLabel(main_frame, text="Choose what to calculate:", font=("Arial", 14))
        choice_label.pack(pady=5)

        self.choice_var = ctk.StringVar(value="1")

        choices = [
            ("C1 (Initial concentration)", "1"),
            ("V1 (Initial volume)", "2"),
            ("C2 (Final concentration)", "3"),
            ("V2 (Final volume)", "4")
        ]

        for text, val in choices:
            ctk.CTkRadioButton(main_frame, text=text, variable=self.choice_var, value=val).pack(anchor="w", padx=20)

        # Inputs
        self.val1_entry = self._create_entry(main_frame, "Value 1:")
        self.val2_entry = self._create_entry(main_frame, "Value 2:")
        self.val3_entry = self._create_entry(main_frame, "Value 3:")

        # Button
        calc_button = ctk.CTkButton(main_frame, text="Calculate", command=self.calculate)
        calc_button.pack(pady=15)

        # Result
        self.result_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Instructions
        instructions_text = (
            "Instructions:\n"
            "1: Enter V1, C2, V2\n"
            "2: Enter C1, C2, V2\n"
            "3: Enter C1, V1, V2\n"
            "4: Enter C1, V1, C2\n"
            "All values must be numbers."
        )

        instructions = ctk.CTkTextbox(main_frame, width=350, height=120, corner_radius=10)
        instructions.insert("0.0", instructions_text)
        instructions.configure(state="disabled")
        instructions.pack(pady=10)

    def _create_entry(self, parent, label_text):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 13))
        label.pack(pady=3)
        entry = ctk.CTkEntry(parent, width=200)
        entry.pack()
        return entry

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
                self.result_label.configure(text=f"C1 = {result}\nInitial concentration.")
        elif choice == "2":
            C1, C2, V2 = val1, val2, val3
            result = Calculation_of_V1(C1, C2, V2)
            if result is not None:
                self.result_label.configure(text=f"V1 = {result}\nInitial volume.")
        elif choice == "3":
            C1, V1, V2 = val1, val2, val3
            result = Calculation_of_C2(C1, V1, V2)
            if result is not None:
                self.result_label.configure(text=f"C2 = {result}\nFinal concentration.")
        elif choice == "4":
            C1, V1, C2 = val1, val2, val3
            result = Calculation_of_V2(C1, V1, C2)
            if result is not None:
                self.result_label.configure(text=f"V2 = {result}\nFinal volume.")

        if result is None:
            self.result_label.configure(text="Error: Invalid input (division by zero?)")

if __name__ == "__main__":
    root = ctk.CTk()
    app = DilutionCalculatorGUI(root)
    root.mainloop()
