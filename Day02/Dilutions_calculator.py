# Solve dilution problems using the equation C1 * V1 = C2 * V2
# All the factors must be in the same units

print("--------------------------------------------------")
print("Dilution Calculator (C1 * V1 = C2 * V2)")
print("All the factors must be in the same units (e.g., mL, M, mM, ul...)")
print("--------------------------------------------------")
print("Which variable would you like to calculate?")
print("1 = C1 (Initial concentration)")
print("2 = V1 (Initial volume)")
print("3 = C2 (Final concentration)")
print("4 = V2 (Final volume)")

choice = input("Enter 1, 2, 3, or 4: ")

if choice == "1":
    V1 = float(input("Enter V1: "))
    C2 = float(input("Enter C2: "))
    V2 = float(input("Enter V2: "))
    C1 = (C2 * V2) / V1
    print(f"\nC1 = {C1}")

elif choice == "2":
    C1 = float(input("Enter C1: "))
    C2 = float(input("Enter C2: "))
    V2 = float(input("Enter V2: "))
    V1 = (C2 * V2) / C1
    print(f"\nV1 = {V1}")

elif choice == "3":
    C1 = float(input("Enter C1: "))
    V1 = float(input("Enter V1: "))
    V2 = float(input("Enter V2: "))
    C2 = (C1 * V1) / V2
    print(f"\nC2 = {C2}")

elif choice == "4":
    C1 = float(input("Enter C1: "))
    V1 = float(input("Enter V1: "))
    C2 = float(input("Enter C2: "))
    V2 = (C1 * V1) / C2
    print(f"\nV2 = {V2}")