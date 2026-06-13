import os
import sys

python_exe = sys.executable

while True:

    print("\n================================")
    print("     LUNAR TERRAIN ANALYZER")
    print("================================")
    print("1. Crater Detection")
    print("2. Terrain Relief Map")
    print("3. Safe Landing Analysis")
    print("4. Exit")
    print("================================")

    choice = input("Select option: ")

    if choice == "1":
        os.system(f'"{python_exe}" crater_detection.py')

    elif choice == "2":
        os.system(f'"{python_exe}" relief_map.py')

    elif choice == "3":
        os.system(f'"{python_exe}" safe_zone.py')

    elif choice == "4":
        print("Exiting...")
        break

    else:
        print("Invalid choice")