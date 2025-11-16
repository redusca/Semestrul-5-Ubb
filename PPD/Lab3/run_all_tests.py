import subprocess
import sys
import os

def generate_test_data(digits, filename, specific_value=None):
    """Generate test data using the Python generator script"""
    if specific_value:
        cmd = ["python", "generate_test_data.py", "specific", specific_value, filename]
    else:
        cmd = ["python", "generate_test_data.py", "random", str(digits), filename]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  Generated {filename}: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  Error generating {filename}: {e}")
        print(f"  STDERR: {e.stderr}")
        sys.exit(1)

def run_test(exe_name, num_processes, num_runs, input1, input2, variant, test_size, output_csv):
    """
    Run a single test configuration
    
    Args:
        exe_name: Name of the executable (e.g., 'varianta1_standard.exe')
        num_processes: Number of MPI processes to use
        num_runs: Number of times to run the test
        input1: First input file (Numar1.txt)
        input2: Second input file (Numar2.txt)
        variant: Variant number (0=sequential, 1=standard, 2=scatter, 3=async)
        test_size: Test size identifier (e.g., "16", "1000")
        output_csv: Output CSV file name
    """
    variant_names = {
        0: "Sequential",
        1: "MPI Standard",
        2: "MPI Scatter/Gather",
        3: "MPI Asynchronous"
    }
    
    print(f"\n{'='*70}")
    print(f"Testing: {test_size} digits - {variant_names.get(variant, 'Unknown')}")
    print(f"Processes: {num_processes}, Runs: {num_runs}")
    print(f"Executable: {exe_name}")
    print(f"{'='*70}")
    
    cmd = [
        "powershell", "-ExecutionPolicy", "Bypass", "-File", 
        ".\\scriptC.ps1",
        exe_name,
        str(num_processes),
        str(num_runs),
        input1,
        input2,
        str(variant),
        test_size,
        output_csv
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running test: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        sys.exit(1)

def main():
    # Configuration
    num_runs = 10    # Number of runs for averaging
    output_csv = "outC.csv"
    
    # Clean up old CSV if exists
    if os.path.exists(output_csv):
        os.remove(output_csv)
        print(f"Removed old {output_csv}")
    
    print("="*70)
    print("Lab3 - Big Number Addition with MPI - Comprehensive Test Suite")
    print("="*70)
    print(f"Number of runs per test: {num_runs}")
    print(f"Output file: {output_csv}")
    print("="*70)
    
    # Test configurations: (test_name, N1, N2, specific_num1, specific_num2, variants_config)
    # variants_config: [(variant, exe_name, process_counts)]
    test_configs = [
        # Test 1: N1=N2=16 - specific numbers
        {
            "name": "Test 1: N=16 (specific numbers)",
            "n1": 16,
            "n2": 16,
            "specific_num1": "9999444444449999",
            "specific_num2": "9999555555559999",
            "test_size": "16",
            "variants": [
                (0, "varianta0_secvential.exe", [1]),           # Sequential
                (1, "varianta1_standard.exe", [5]),             # Standard with 5 processes
                (2, "varianta2_scatter_gather.exe", [4]),       # Scatter/Gather with 4 processes
                (3, "varianta3_asincron.exe", [5])              # Async with 5 processes
            ]
        },
        # Test 2: N1=N2=1000 - random
        {
            "name": "Test 2: N=1000 (random)",
            "n1": 1000,
            "n2": 1000,
            "specific_num1": None,
            "specific_num2": None,
            "test_size": "1000",
            "variants": [
                (0, "varianta0_secvential.exe", [1]),
                (1, "varianta1_standard.exe", [5, 9, 17]),
                (2, "varianta2_scatter_gather.exe", [4, 8, 16]),
                (3, "varianta3_asincron.exe", [5, 9, 17])
            ]
        },
        # Test 3: N1=N2=10000 - random
        {
            "name": "Test 3: N=10000 (random)",
            "n1": 10000,
            "n2": 10000,
            "specific_num1": None,
            "specific_num2": None,
            "test_size": "10000",
            "variants": [
                (0, "varianta0_secvential.exe", [1]),
                (1, "varianta1_standard.exe", [5, 9, 17]),
                (2, "varianta2_scatter_gather.exe", [4, 8, 16]),
                (3, "varianta3_asincron.exe", [5, 9, 17])
            ]
        },
        # Test 4: N1=100, N2=100000 - random (different sizes)
        {
            "name": "Test 4: N1=100, N2=100000 (random, different sizes)",
            "n1": 100,
            "n2": 100000,
            "specific_num1": None,
            "specific_num2": None,
            "test_size": "100_100000",
            "variants": [
                (0, "varianta0_secvential.exe", [1]),
                (1, "varianta1_standard.exe", [5, 9, 17]),
                (2, "varianta2_scatter_gather.exe", [4, 8, 16]),
                (3, "varianta3_asincron.exe", [5, 9, 17])
            ]
        }
    ]
    
    # Calculate total number of tests
    total_tests = sum(
        sum(len(process_counts) for _, _, process_counts in config["variants"])
        for config in test_configs
    )
    
    current_test = 0
    
    for test_config in test_configs:
        print(f"\n{'#'*70}")
        print(f"# {test_config['name']}")
        print(f"{'#'*70}")
        
        # Generate test data
        print("\nGenerating test data...")
        if test_config["specific_num1"]:
            generate_test_data(test_config["n1"], "temp_Numar1.txt", test_config["specific_num1"])
            generate_test_data(test_config["n2"], "temp_Numar2.txt", test_config["specific_num2"])
        else:
            generate_test_data(test_config["n1"], "temp_Numar1.txt")
            generate_test_data(test_config["n2"], "temp_Numar2.txt")
        
        # Run all variants for this test
        for variant, exe_name, process_counts in test_config["variants"]:
            for num_processes in process_counts:
                current_test += 1
                print(f"\n\nProgress: Test {current_test}/{total_tests}")
                
                run_test(
                    exe_name,
                    num_processes,
                    num_runs,
                    "temp_Numar1.txt",
                    "temp_Numar2.txt",
                    variant,
                    test_config["test_size"],
                    output_csv
                )
    
    # Clean up temporary files
    if os.path.exists("temp_Numar1.txt"):
        os.remove("temp_Numar1.txt")
    if os.path.exists("temp_Numar2.txt"):
        os.remove("temp_Numar2.txt")
    
    print("\n" + "="*70)
    print("All tests completed successfully!")
    print(f"Results have been saved to {output_csv}")
    print("="*70)

if __name__ == "__main__":
    main()
