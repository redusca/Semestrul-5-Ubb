import subprocess
import sys

def run_test(exe_name, num_threads, num_runs, input_file, mode, matrix_type, allocation_type, output_file):
    """
    Run a single test configuration
    
    Args:
        exe_name: Name of the executable (e.g., 'c_static.exe')
        num_threads: Number of threads to use
        num_runs: Number of times to run the test
        input_file: Input matrix file
        mode: Execution mode (1=sequential, 2=parallel horizontal, 3=parallel vertical)
        matrix_type: Matrix type identifier (1-5)
        allocation_type: Allocation type (1=static, 2=dynamic)
        output_file: Output file name
    """
    mode_names = {
        1: "Sequential",
        2: "Parallel Horizontal",
        3: "Parallel Vertical"
    }
    
    matrix_names = {
        1: "10x10",
        2: "1000x1000",
        3: "10x10000",
        4: "10000x10",
        5: "1000x10000"
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: {matrix_names.get(matrix_type, 'Unknown')} - {mode_names.get(mode, 'Unknown')}")
    print(f"Threads: {num_threads}, Runs: {num_runs}")
    print(f"Output: {output_file}")
    print(f"{'='*60}")
    
    cmd = [
        "powershell", "-ExecutionPolicy", "Bypass", "-File", 
        ".\\scriptC.ps1",
        exe_name,
        str(num_threads),
        str(num_runs),
        input_file,
        str(mode),
        str(matrix_type),
        str(allocation_type),
        output_file
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

def main():
    # Configuration
    exe_name = "c_static.exe"
    num_runs = 10    # Number of runs for averaging
    allocation_type = 1  # 1 = static
    allocation_name = "S"  # S for static, D for dynamic
    
    # Matrix configurations: (matrix_type, input_file, k, n, m, thread_counts)
    # Format: (matrix_type, input_file, k, n, m, threads_for_parallel)
    # For mode 1 (sequential), threads will be set to 1
    # For modes 2 and 3 (parallel), will iterate through thread_counts
    matrices = [
        (1, "matrix_3_10_10.txt", 3, 10, 10, [4]),              # N=M=10, k=3, p=4
        (2, "matrix_5_1000_1000.txt", 5, 1000, 1000, [2, 4, 8, 16]), # N=M=1000, k=5, p=2,4,8,16
        (3, "matrix_5_10_10000.txt", 5, 10, 10000, [2, 4, 8, 16]),  # N=10, M=10000, k=5, p=2,4,8,16
        (4, "matrix_5_10000_10.txt", 5, 10000, 10, [2, 4, 8, 16]),  # N=10000, M=10, k=5, p=2,4,8,16
        (5, "matrix_5_10000_10000.txt", 5, 10000, 10000, [2, 4, 8, 16]) # N=10000, M=10000, k=5, p=2,4,8,16
    ]
    
    # Execution modes: 1=sequential, 2=parallel horizontal, 3=parallel vertical
    modes = [1, 2, 3]
    
    print("Starting comprehensive test suite for STATIC allocation")
    print(f"Executable: {exe_name}")
    print(f"Number of runs per test: {num_runs}")
    
    # Calculate total tests
    total_tests = 0
    for _, _, _, _, _, thread_counts in matrices:
        total_tests += 1  # 1 for sequential
        total_tests += len(thread_counts) * 2  # for parallel modes 2 and 3
    
    current_test = 0
    
    for matrix_type, input_file, k, n, m, thread_counts in matrices:
        for mode in modes:
            if mode == 1:
                # Sequential mode - always use 1 thread
                current_test += 1
                print(f"\n\nProgress: Test {current_test}/{total_tests}")
                output_file = f"outputC{allocation_name}_{k}_{n}_{m}.txt"
                run_test(exe_name, 1, num_runs, input_file, mode, matrix_type, allocation_type, output_file)
            else:
                # Parallel modes - iterate through different thread counts
                for num_threads in thread_counts:
                    current_test += 1
                    print(f"\n\nProgress: Test {current_test}/{total_tests}")
                    output_file = f"outputC{allocation_name}_{k}_{n}_{m}.txt"
                    run_test(exe_name, num_threads, num_runs, input_file, mode, matrix_type, allocation_type, output_file)
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("Results have been saved to outC.csv")
    print("="*60)

if __name__ == "__main__":
    main()
