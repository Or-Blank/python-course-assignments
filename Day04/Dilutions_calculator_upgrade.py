#To run first copy this: pip install customtkinter
#Make sure 1. Dilutions_calculator_upgrade.py and 2. dilution_lib.py are in the same folder

import customtkinter as ctk
from tkinter import messagebox
from dilution_lib import (Calculation_of_C1, Calculation_of_V1, Calculation_of_C2, Calculation_of_V2, convert_volume_from_L, convert_volume_to_L)


class DilutionCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilution Calculator")
        self.root.geometry("520x640")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        main_frame = ctk.CTkFrame(root, corner_radius=15)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Dilution Calculator", font=("Arial", 22, "bold"))
        title.pack(pady=10)

        choice_label = ctk.CTkLabel(main_frame, text="Choose what to calculate:", font=("Arial", 14))
        choice_label.pack(pady=5)

        self.choice_var = ctk.StringVar(value="1")

        choices = [
            ("C1 (Initial concentration)", "1"),
            ("V1 (Initial volume)", "2"),
            ("C2 (Final concentration)", "3"),
            ("V2 (Final volume)", "4"),
        ]

        for text, val in choices:
            ctk.CTkRadioButton(main_frame, text=text, variable=self.choice_var, value=val).pack(
                anchor="w", padx=20
            )

        conc_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        conc_frame.pack(pady=2, fill="x")

        conc_label = ctk.CTkLabel(conc_frame, text="Concentration unit:", font=("Arial", 12))
        conc_label.pack(side="left", padx=10)

        self.conc_unit = ctk.CTkOptionMenu(conc_frame, values=["M", "g/L", "ng/µL"])
        self.conc_unit.set("M")
        self.conc_unit.pack(side="left", padx=10)

        vol_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        vol_frame.pack(pady=2, fill="x")

        vol_label = ctk.CTkLabel(vol_frame, text="Volume unit:", font=("Arial", 12))
        vol_label.pack(side="left", padx=10)

        self.vol_unit = ctk.CTkOptionMenu(vol_frame, values=["L", "mL", "µL"])
        self.vol_unit.set("mL")
        self.vol_unit.pack(side="left", padx=10)

        # Inputs
        self.val1_entry = self._create_entry(main_frame, "Value 1:")
        self.val2_entry = self._create_entry(main_frame, "Value 2:")
        self.val3_entry = self._create_entry(main_frame, "Value 3:")

        calc_button = ctk.CTkButton(main_frame, text="Calculate", command=self.calculate)
        calc_button.pack(pady=15)

        self.result_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        instructions_text = (
            "Instructions:\n"
            "• For C1: enter Value 1 (V1), Value 2 (C2), Value 3 (V2)\n"
            "• For V1: enter Value 1 (C1), Value 2 (C2), Value 3 (V2)\n"
            "• For C2: enter Value 1 (C1), Value 2 (V1), Value 3 (V2)\n"
            "• For V2: enter Value 1 (C1), Value 2 (V1), Value 3 (C2)\n\n"
            
            "All concentrations must use the same unit.\n" "All volumes must use the same unit.\n"
        )

        instructions = ctk.CTkTextbox(main_frame, width=440, height=170, corner_radius=10)
        instructions.insert("0.0", instructions_text)
        instructions.configure(state="disabled")
        instructions.pack(pady=10)

    def _create_entry(self, parent, label_text):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=6)

        label = ctk.CTkLabel(row, text=label_text, width=140, anchor="w", font=("Arial", 13))
        label.pack(side="left")

        entry = ctk.CTkEntry(row, placeholder_text="Enter number")
        entry.pack(side="left", fill="x", expand=True)
        return entry

    def calculate(self):
        choice = self.choice_var.get()
        conc_unit = self.conc_unit.get()
        vol_unit = self.vol_unit.get()

        try:
            val1 = float(self.val1_entry.get())
            val2 = float(self.val2_entry.get())
            val3 = float(self.val3_entry.get())
        except ValueError:
            messagebox.showerror("Error", "All values must be numbers.")
            return

        try:
            # ---------- C1 ----------
            if choice == "1":
                V1_raw, C2_raw, V2_raw = val1, val2, val3
                V1_L = convert_volume_to_L(V1_raw, vol_unit)
                V2_L = convert_volume_to_L(V2_raw, vol_unit)

                C1 = Calculation_of_C1(C2_raw, V2_L, V1_L)

                self.result_label.configure(
                    text=f"C1 = {C1:.6g} {conc_unit}\nInitial concentration."
                )

            # ---------- V1 + solvent ----------
            elif choice == "2":
                C1_raw, C2_raw, V2_raw = val1, val2, val3
                V2_L = convert_volume_to_L(V2_raw, vol_unit)

                V1_L = Calculation_of_V1(C1_raw, C2_raw, V2_L)
                V1_out = convert_volume_from_L(V1_L, vol_unit)

                solvent_out = V2_raw - V1_out

                self.result_label.configure(
                    text=(
                        f"V1 = {V1_out:.6g} {vol_unit}\n"
                        f"Take this volume from the stock.\n\n"
                        f"Add {solvent_out:.6g} {vol_unit} of solvent\n"
                        f"to reach a final volume of {V2_raw} {vol_unit}."
                    )
                )

            # ---------- C2 ----------
            elif choice == "3":
                C1_raw, V1_raw, V2_raw = val1, val2, val3
                V1_L = convert_volume_to_L(V1_raw, vol_unit)
                V2_L = convert_volume_to_L(V2_raw, vol_unit)

                C2 = Calculation_of_C2(C1_raw, V1_L, V2_L)

                self.result_label.configure(
                    text=f"C2 = {C2:.6g} {conc_unit}\nFinal concentration."
                )

            # ---------- V2 ----------
            elif choice == "4":
                C1_raw, V1_raw, C2_raw = val1, val2, val3
                V1_L = convert_volume_to_L(V1_raw, vol_unit)
                V2_L = Calculation_of_V2(C1_raw, V1_L, C2_raw)
                V2_out = convert_volume_from_L(V2_L, vol_unit)
                self.result_label.configure(
                    text=(
                        f"V2 = {V2_out:.6g} {vol_unit}\n"
                        f"Final volume required."
                    )
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return


if __name__ == "__main__":
    root = ctk.CTk()
    app = DilutionCalculatorGUI(root)
    root.mainloop()

