def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32


def celsius_to_kelvin(c):
    return c + 273.15


def fahrenheit_to_celsius(f):
    return (f - 32) * 5/9


def fahrenheit_to_kelvin(f):
    return (f - 32) * 5/9 + 273.15


def kelvin_to_celsius(k):
    return k - 273.15


def kelvin_to_fahrenheit(k):
    return (k - 273.15) * 9/5 + 32


def temperature_converter():
    print("=== Temperature Converter Application ===")

    while True:
        print("\nSupported Units:")
        print("C - Celsius")
        print("F - Fahrenheit")
        print("K - Kelvin")
        print("Q - Quit the application")

        from_unit = input(
            "\nConvert FROM (C/F/K) or Q to quit: ").strip().upper()

        if from_unit == 'Q':
            print("Thank you for using the Temperature Converter! Goodbye.")
            break

        if from_unit not in ['C', 'F', 'K']:
            print("Invalid choice. Please select C, F, or K.")
            continue

        to_unit = input("Convert TO (C/F/K): ").strip().upper()

        if to_unit not in ['C', 'F', 'K']:
            print("Invalid choice. Please select C, F, or K.")
            continue

        if from_unit == to_unit:
            print("The source and target units are the same. No conversion needed!")
            continue

        while True:
            temp_input = input(
                f"Enter the temperature in °{from_unit}: ").strip()

            check_str = temp_input
            if check_str.startswith('-'):
                check_str = check_str[1:]
            if check_str.count('.') == 1:
                check_str = check_str.replace('.', '', 1)

            if check_str.isdigit() and temp_input != "":
                temp = float(temp_input)
                break
            else:
                print("Invalid input. Please enter a valid number.")

        if from_unit == 'C' and to_unit == 'F':
            result = celsius_to_fahrenheit(temp)
        elif from_unit == 'C' and to_unit == 'K':
            result = celsius_to_kelvin(temp)
        elif from_unit == 'F' and to_unit == 'C':
            result = fahrenheit_to_celsius(temp)
        elif from_unit == 'F' and to_unit == 'K':
            result = fahrenheit_to_kelvin(temp)
        elif from_unit == 'K' and to_unit == 'C':
            result = kelvin_to_celsius(temp)
        elif from_unit == 'K' and to_unit == 'F':
            result = kelvin_to_fahrenheit(temp)

        print(f"\nResult: {temp:.2f}°{from_unit} = {result:.2f}°{to_unit}")
        print("-" * 40)


if __name__ == "__main__":
    temperature_converter()
