def color_red(text):
    red = "\033[31m"
    reset = "\033[0m"
    return f"{red}{text}{reset}"

def menu():
    choice = input(color_red("""
    SELECT OPTION: 
    
    1. H2-Scan
    2. C-Flood
    """))
    
    if choice == "1":
        import h2_scan
    elif choice == "2":
        import cflood
    else:
        print(color_red("Invalid input. Enter 1 or 2."))
        menu()

menu()