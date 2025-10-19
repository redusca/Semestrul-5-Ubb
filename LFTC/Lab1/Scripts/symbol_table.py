class SymbolTable:
    def __init__(self, size=101):
        self.size = size
        self.table = [None] * size 
        self.positions = {}  
        
    def _hash(self, key):
        """
        Hash function using polynomial rolling hash.
        Converts a string key into an index (0 to size-1).
        """
        hash_value = 0
        prime = 31
        
        for char in key:
            hash_value = (hash_value * prime + ord(char)) % self.size
            
        return hash_value
    
    def add(self, symbol):
        if symbol in self.positions:
            return self.positions[symbol]
        
        hash_value = self._hash(symbol)
        index = hash_value
        
        # Linear probing: find next available slot
        while self.table[index] is not None:
            if self.table[index] == symbol:
                self.positions[symbol] = index
                return index
            index = (index + 1) % self.size
            
            # Check if we've wrapped around (table is full)
            if index == hash_value:
                raise Exception("Symbol table is full!")
        
        # Found empty slot
        self.table[index] = symbol
        self.positions[symbol] = index
        
        return index
    
    def search(self, symbol):
        """
        Check if a symbol exists in the table.
        """
        return symbol in self.positions
    
    def get_position(self, symbol):
        """
        Get the position of a symbol (index in table).
        Returns None if symbol not found.
        """
        return self.positions.get(symbol, None)
    
    def remove(self, symbol):
        """
        Remove a symbol from the table (not recommended for hash tables with linear probing).
        """
        if symbol not in self.positions:
            return False
        
        index = self.positions[symbol]
        self.table[index] = None
        del self.positions[symbol]
        return True
    
    def get_all_symbols(self):
        """
        Get all symbols in the table.
        """
        return [sym for sym in self.table if sym is not None]
    
    def save_to_file(self, filename):
        """
        Save the hash table structure to a file showing the linear probing layout.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"Table Size: {self.size}\n")
            f.write(f"Total Symbols: {len(self.positions)}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"{'Symbol':<30} | {'Code':>5}\n")
            f.write("-" * 60 + "\n")
            for i, symbol in enumerate(self.table):
                if symbol is not None:
                    f.write(f"{symbol:<30} | {i:>5}\n")
            f.write("=" * 60 + "\n")
    
    def __str__(self):
        """
        String representation showing all occupied positions.
        """
        result = "Symbol Table (Hash Table with Linear Probing):\n"
        result += "=" * 60 + "\n"
        
        for i, symbol in enumerate(self.table):
            if symbol is not None:
                hash_val = self._hash(symbol)
                probe_distance = (i - hash_val) % self.size
                result += f"Position {i:3d}: {symbol:<20} (hash={hash_val}, probes={probe_distance})\n"
        
        return result