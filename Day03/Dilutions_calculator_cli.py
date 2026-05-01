import sys
from dilution_lib import Calculation_of_C1, Calculation_of_V1, Calculation_of_C2, Calculation_of_V2

def main():
    if len(sys.argv) < 5:
        print("Dilutions Calculator")
        print("C1 * V1 = C2 * V2")
        print("Choices:")
        print("1: Calculate C1 - args: V1 C2 V2")
        print("2: Calculate V1 - args: C1 C2 V2")
        print("3: Calculate C2 - args: C1 V1 V2")
        print("4: Calculate V2 - args: C1 V1 C2")
        print("In order to use, type: python Dilutions_calculator_cli.py <choice> <val1> <val2> <val3>")
        return

    choice = sys.argv[1]
    try:
        val1 = float(sys.argv[2])
        val2 = float(sys.argv[3])
        val3 = float(sys.argv[4])
    except ValueError:
        print("Error: All values must be numbers.")
        return

    if choice == "1":
        V1, C2, V2 = val1, val2, val3
        C1 = Calculation_of_C1(C2, V2, V1)
        if C1 is not None:
            print(f"C1 = {C1}")
            print("This means that the initial concentration of your solution is", C1, "Molarity units.")

    elif choice == "2":
        C1, C2, V2 = val1, val2, val3
        V1 = Calculation_of_V1(C1, C2, V2)
        if V1 is not None:
            print(f"V1 = {V1}")
            print("This means that the initial volume of your solution is", V1, "volume units.")
    
    elif choice == "3":
        C1, V1, V2 = val1, val2, val3
        C2 = Calculation_of_C2(C1, V1, V2)
        if C2 is not None:
            print(f"C2 = {C2}")
            print("This means that the final concentration of your solution is", C2, "Molarity units.")
    
    elif choice == "4":
        C1, V1, C2 = val1, val2, val3
        V2 = Calculation_of_V2(C1, V1, C2)
        if V2 is not None:
            print(f"V2 = {V2}")
            print("This means that the final volume of your solution is", V2, "Volume units.")
    
if __name__ == "__main__":
    main()