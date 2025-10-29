import csv
import os

def convert_ns_to_seconds(ns_string):
    """
    Convert nanoseconds string to seconds
    
    Args:
        ns_string: String like "123456789 ns" or "123456789"
    
    Returns:
        Float value in seconds
    """
    # Remove " ns" suffix if present
    ns_value = ns_string.replace(" ns", "").strip()
    
    try:
        # Convert to float and divide by 1,000,000,000 to get seconds
        return float(ns_value) / 1_000_000_000
    except ValueError:
        return 0.0

def process_csv_file(input_file, output_file):
    """
    Process a CSV file to add a "Timp executie (s)" column
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
    """
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    
    rows = []
    
    # Read the input CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for i, row in enumerate(reader):
            if i == 0:
                # Header row - add new column
                row.append('Timp executie (s)')
            else:
                # Data row - calculate seconds from the last column
                if len(row) > 0:
                    # The last column should contain the time in nanoseconds
                    ns_time = row[-1]
                    seconds = convert_ns_to_seconds(ns_time)
                    row.append(f"{seconds:.6f}")
            
            rows.append(row)
    
    # Write the output CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    
    print(f"Processed: {input_file} -> {output_file}")
    print(f"Added 'Timp executie (s)' column with {len(rows)-1} data rows")

def main():
    # Process outC.csv (C/C++ results)
    if os.path.exists("outC.csv"):
        process_csv_file("outC.csv", "outC_with_seconds.csv")
        print()
    else:
        print("outC.csv not found, skipping...")
    
    # Process outJ.csv (Java results)
    if os.path.exists("outJ.csv"):
        process_csv_file("outJ.csv", "outJ_with_seconds.csv")
        print()
    else:
        print("outJ.csv not found, skipping...")
    
    print("="*60)
    print("Processing complete!")
    print("New files created:")
    if os.path.exists("outC_with_seconds.csv"):
        print("  - outC_with_seconds.csv")
    if os.path.exists("outJ_with_seconds.csv"):
        print("  - outJ_with_seconds.csv")
    print("="*60)

if __name__ == "__main__":
    main()
