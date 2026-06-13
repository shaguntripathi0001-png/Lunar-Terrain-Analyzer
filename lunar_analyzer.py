import os

while True:

    print("\n================================")
    print("     LUNAR TERRAIN ANALYZER")
    print("================================")
    print("1. Crater Detection")
    print("2. Terrain Relief Map")
    print("3. Safe Landing Analysis")
    print("4. View Latest Mission Report")
    print("5. Exit")
    print("================================")

    choice = input("Select option: ")

    # ==========================
    # CRATER DETECTION
    # ==========================
    if choice == "1":

        os.system(
            "python crater_detection.py"
        )

    # ==========================
    # RELIEF MAP
    # ==========================
    elif choice == "2":

        os.system(
            "python relief_map.py"
        )

    # ==========================
    # SAFE LANDING
    # ==========================
    elif choice == "3":

        os.system(
            "python safe_zone.py"
        )

    # ==========================
    # VIEW REPORT
    # ==========================
    elif choice == "4":

        report_path = (
            "outputs/mission_report.txt"
        )

        print("\n")

        if os.path.exists(report_path):

            with open(
                report_path,
                "r",
                encoding="utf-8"
            ) as f:

                print(f.read())

        else:

            print(
                "No mission report found."
            )

        input(
            "\nPress Enter to continue..."
        )

    # ==========================
    # EXIT
    # ==========================
    elif choice == "5":

        print("\nExiting...")
        break

    else:

        print(
            "\nInvalid Choice"
        )