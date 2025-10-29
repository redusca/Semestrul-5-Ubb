import random
import sys

def generate_matrix_file(k, n, m):
    """
    Generate a file with the format:
    - First line: k
    - Second line: k*k random numbers (0-1000)
    - Third line: n m
    - Fourth line: n*m random numbers (0-1000)
    """
    filename = f"matrix_{k}_{n}_{m}.txt"
    
    with open(filename, 'w') as f:
        # Write k
        f.write(f"{k}\n")
        
        # Write k*k random numbers
        matrix1 = [str(random.randint(0, 50)) for _ in range(k * k)]
        f.write(" ".join(matrix1) + "\n")
        
        # Write n m
        f.write(f"{n} {m}\n")
        
        # Write n*m random numbers
        matrix2 = [str(random.randint(0, 50)) for _ in range(n * m)]
        f.write(" ".join(matrix2) + "\n")
    
    print(f"File '{filename}' generated successfully!")
    return filename

if __name__ == "__main__":
    try:
        generate_matrix_file(3,10,10);
        generate_matrix_file(5,1000,1000);
        generate_matrix_file(5,10,10000);
        generate_matrix_file(5,10000,10);
        generate_matrix_file(5,10000,10000);

    except ValueError:
        print("Error: k, n, and m must be valid integers")
        sys.exit(1)
