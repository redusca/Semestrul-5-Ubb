from analizor_lexical import LexicalAnalyzer

def test_single_file(filename: str):
    print(f"\n{'='*80}")
    print(f"Testing: {filename}")
    print(f"{'='*80}\n")
    
    analyzer = LexicalAnalyzer()
    success = analyzer.analyze_file(filename)
    
    print("\n" + "-"*80)
    print("RESULTS:")
    print("-"*80)
    
    if not success:
        print("\n" + "-"*80)
        print("ERRORS:")
        print("-"*80)
        for error in analyzer.errors:
            print(f"  * {error}")
    
    return success


def test_all_files():
    """Test all example files."""
    files = [
        'cerc.cpp',
        'cmmdc.cpp', 
        'suma_n.cpp',
        'err_1.cpp',
        'err_2.cpp',
        'test_lexical_errors.cpp'
    ]
    
    results = {}
    
    print("="*80)
    print("LEXICAL ANALYZER - COMPREHENSIVE TEST")
    print("="*80)
    
    for filename in files:
        try:
            success = test_single_file(filename)
            results[filename] = "[OK] SUCCESS" if success else "[!] ERRORS FOUND"
        except FileNotFoundError:
            results[filename] = "[X] FILE NOT FOUND"
            print(f"\nError: File '{filename}' not found")
        except Exception as e:
            results[filename] = f"[X] EXCEPTION: {str(e)}"
            print(f"\nError processing '{filename}': {e}")
            
    print("\n")


def interactive_mode():
    print("="*80)
    print("LEXICAL ANALYZER - INTERACTIVE MODE")
    print("="*80)
    print("\nEnter filename to analyze (or 'quit' to exit)")
    
    while True:
        filename = input("\nFilename: ").strip()
        
        if filename.lower() in ['quit', 'exit', 'q']:
            print("Exiting...")
            break
        
        if not filename:
            continue
        
        try:
            test_single_file(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--interactive':
            interactive_mode()
        else:
            # Analyze specific file
            test_single_file(sys.argv[1])
    else:
        # Default: test all files
        test_all_files()
