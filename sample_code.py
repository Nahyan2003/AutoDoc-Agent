def celsius_to_fahrenheit(celsius):
    """Converts Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Converts Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

# Example Usage
current_temp_dubai = 35  # Celsius
print(f"The temperature in Dubai is {current_temp_dubai}°C")
print(f"In Fahrenheit, that is {celsius_to_fahrenheit(current_temp_dubai)}°F")