import json

class FIPWithCodes:
    
    # Token code mappings
    TOKEN_CODES = {
        # Keywords
        '#include': 0,
        '<iostream>': 1,
        'struct': 2,
        'int': 3,
        'double': 4,
        'main': 5,
        'return': 6,
        'if': 7,
        'else': 8,
        'while': 9,
        'std::cin': 10,
        'std::cout': 11,
        'std::endl': 12,
        'this->': 13,
        
        # Operators
        '=': 20,
        '+': 21,
        '-': 22,
        '*': 23,
        '/': 24,
        '%': 25,
        '++': 26,
        '--': 27,
        '==': 28,
        '!=': 29,
        '&&': 30,
        '||': 31,
        '>>': 32,
        '<<': 33,
        
        # Delimiters
        '(': 40,
        ')': 41,
        '{': 42,
        '}': 43,
        ';': 44,
        ',': 45,
        '.': 46,
        '"': 47,
        
        # Special tokens
        'ID': 100,
        'CONST': 101,
        'DENUMIRE': 102
    }
    
    CODE_TO_TOKEN = {v: k for k, v in TOKEN_CODES.items()}
    
    def __init__(self):
        """Initialize an empty FIP."""
        self.entries = []  # List of (atom_code, ts_position, atom_value) tuples
        
    def add(self, token_str, ts_position=-1, atom_value=None):
        """
        Add an entry to FIP.
        ts_position is an integer index in the symbol table, or -1 for non-TS tokens.
        """
        atom_code = self.TOKEN_CODES.get(token_str, -1)
        
        if atom_code == -1:
            print(f"Warning: Unknown token '{token_str}'")
            return
        
        self.entries.append((atom_code, ts_position, atom_value))
    
    def get_entries(self):
        return self.entries.copy()
    
    def save_to_file(self, filename):
        """
        Save FIP in compact format: atom_code ts_position
        """
        with open(filename, 'w', encoding='utf-8') as f:
            for atom_code, ts_position, atom_value in self.entries:
                f.write(f"{atom_code} {ts_position}\n")
    
    def save_readable_to_file(self, filename):
        """
        Save FIP in human-readable format with token names and TS positions.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("FIP - Internal Program Form (Readable Format)\n")
            f.write("=" * 90 + "\n")
            f.write(f"{'Token':<20} {'Code':<10} {'TS Position':<15} {'Atom':<20}\n")
            f.write("-" * 90 + "\n")
            
            for atom_code, ts_position, atom_value in self.entries:
                token_name = self.CODE_TO_TOKEN.get(atom_code, f"UNKNOWN_{atom_code}")
                ts_pos_str = str(ts_position) if ts_position != -1 else "-"
                atom_str = atom_value if atom_value is not None else "-"
                f.write(f"{token_name:<20} {atom_code:<10} {ts_pos_str:<15} {atom_str:<20}\n")
    
    def __str__(self):
        result = "FIP (Internal Program Form - Numeric Codes):\n"
        result += "=" * 90 + "\n"
        result += f"{'Token':<20} {'Code':<10} {'TS Position':<15} {'Atom':<20}\n"
        result += "-" * 90 + "\n"
        
        for atom_code, ts_position, atom_value in self.entries:
            token_name = self.CODE_TO_TOKEN.get(atom_code, f"UNKNOWN_{atom_code}")
            ts_pos_str = str(ts_position) if ts_position != -1 else "-"
            atom_str = atom_value if atom_value is not None else "-"
            result += f"{token_name:<20} {atom_code:<10} {ts_pos_str:<15} {atom_str:<20}\n"
        
        return result
    
    def __len__(self):
        return len(self.entries)
    
    @classmethod
    def load_codes_from_json(cls, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Update class-level mappings
            cls.TOKEN_CODES.clear()
            
            for category in ['keywords', 'operators', 'delimiters', 'special_tokens']:
                if category in data:
                    cls.TOKEN_CODES.update(data[category])
            
            # Rebuild reverse mapping
            cls.CODE_TO_TOKEN = {v: k for k, v in cls.TOKEN_CODES.items()}
            
            print(f"Loaded {len(cls.TOKEN_CODES)} token codes from {json_path}")
            
        except Exception as e:
            print(f"Warning: Could not load codes from {json_path}: {e}")
            print("Using default hardcoded values.")
