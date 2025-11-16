import random
import sys

def generate_number(num_digits, filename):
    """Generate a random number with specified digits and save to file"""
    with open(filename, 'w') as f:
        f.write(f"{num_digits}\n")
        
        # First digit should not be 0 for meaningful numbers
        first_digit = random.randint(1, 9)
        f.write(str(first_digit))
        
        # Generate remaining digits
        for i in range(1, num_digits):
            digit = random.randint(0, 9)
            f.write(" " + str(digit))
        
        f.write("\n")

def generate_specific_number(digits_str, filename):
    """Generate a number from a specific string of digits"""
    # Remove spaces from input
    digits_str = digits_str.replace(" ", "")
    num_digits = len(digits_str)
    
    with open(filename, 'w') as f:
        f.write(f"{num_digits}\n")
        for i, digit in enumerate(digits_str):
            if i > 0:
                f.write(" ")
            f.write(digit)
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Generate random: python generate_test_data.py random <num_digits> <filename>")
        print("  Generate specific: python generate_test_data.py specific <digits> <filename>")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "random":
        if len(sys.argv) != 4:
            print("Usage: python generate_test_data.py random <num_digits> <filename>")
            sys.exit(1)
        
        num_digits = int(sys.argv[2])
        filename = sys.argv[3]
        generate_number(num_digits, filename)
        print(f"Generated random number with {num_digits} digits in {filename}")
    
    elif mode == "specific":
        if len(sys.argv) != 4:
            print("Usage: python generate_test_data.py specific <digits> <filename>")
            sys.exit(1)
        
        digits_str = sys.argv[2]
        filename = sys.argv[3]
        generate_specific_number(digits_str, filename)
        print(f"Generated specific number in {filename}")
    
    else:
        print("Invalid mode. Use 'random' or 'specific'")
        sys.exit(1)
