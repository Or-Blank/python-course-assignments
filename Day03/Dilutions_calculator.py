# Import all the calculation from the library file instead of them being here
from dilution_lib import Calculation_of_C1, Calculation_of_V1, Calculation_of_C2, Calculation_of_V2

# Now this is the main function to run the program of the above sub defs
def main():
    print("---------------------------------------------------")
    print("Dilution Calculator (C1 * V1 = C2 * V2)")
    print("Keep in mind: All the factors must be in the same units! (Concentration: Molarity, Volume: uL, mL, etc.)")
    print("---------------------------------------------------")
    print("Hello, Which variable would you like to calculate today?")
    print("1 = C1 (Initial concentration)")
    print("2 = V1 (Initial volume)")
    print("3 = C2 (Final concentration)")
    print("4 = V2 (Final volume)")
    
    choice = input("Enter 1, 2, 3, or 4: ")
    
    if choice == "1":
        V1 = float(input("Enter V1: "))
        C2 = float(input("Enter C2: "))
        V2 = float(input("Enter V2: "))
        C1 = Calculation_of_C1(C2, V2, V1)
        if C1 is not None:
            print(f"\nC1 = {C1}")
            print("This means that the initial concentration of your solution is", C1, "Molarity units.")
        else:
            return
        
    elif choice == "2":
        C1 = float(input("Enter C1: "))
        C2 = float(input("Enter C2: "))
        V2 = float(input("Enter V2: "))
        V1 = Calculation_of_V1(C1, C2, V2)
        if V1 is not None:
            print(f"\nV1 = {V1}")
            print("This means that the initial volume of your solution is", V1, "volume units.")
        else:
            return
        
    elif choice == "3":
        C1 = float(input("Enter C1: "))
        V1 = float(input("Enter V1: "))
        V2 = float(input("Enter V2: "))
        C2 = Calculation_of_C2(C1, V1, V2)
        if C2 is not None:
            print(f"\nC2 = {C2}")
            print("This means that the final concentration of your solution is", C2, "Molarity units.")
        else:
            return
        
    elif choice == "4":
        C1 = float(input("Enter C1: "))
        V1 = float(input("Enter V1: "))
        C2 = float(input("Enter C2: "))
        V2 = Calculation_of_V2(C1, V1, C2)
        if V2 is not None:
            print(f"\nV2 = {V2}")
            print("This means that the final volume of your solution is", V2, "Volume units.")
        else:
            return

if __name__ == "__main__":
    main()
