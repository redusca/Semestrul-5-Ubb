from enum import Enum
from dataclasses import dataclass
import os
from typing import List
from symbol_table import SymbolTable
from fip import FIPWithCodes


class TokenType(Enum):
    #cuvinte rezervate
    INCLUDE = "#include"
    IOSTREAM = "<iostream>"
    STRUCT = "STRUCT"
    INT = "int"
    DOUBLE = "double"
    MAIN = "main"
    RETURN = "return"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    STD_CIN = "std::cin"
    STD_COUT = "std::cout"
    STD_ENDL = "std::endl"
    THIS = "this->"
    
    #semnse
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIV = "/"
    MODULO = "%"
    INCREMENT = "++"
    DECREMENT = "--"
    EQUAL = "=="
    NOT_EQUAL = "!="
    AND = "&&"
    OR = "||"
    INPUT = ">>"
    OUTPUT = "<<"
    DOT = "."
    GHILIMELE = '"'
    
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    SEMICOLON = ";"
    COMMA = ","

    IDENTIFIER = "ID"
    CONSTANT = "CONST"
    DENUMIRE = "DENUMIRE"


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int


@dataclass
class LexicalError:
    message: str
    line: int
    column: int
    
    def __str__(self):
        return f"Lexical Error at line {self.line}, column {self.column}: {self.message}"


class LexicalAnalyzer:
    def __init__(self):
        self.keywords = {
            '#include': TokenType.INCLUDE,
            '<iostream>': TokenType.IOSTREAM,
            'struct': TokenType.STRUCT,
            'int': TokenType.INT,
            'double': TokenType.DOUBLE,
            'main': TokenType.MAIN,
            'return': TokenType.RETURN,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'std::cin': TokenType.STD_CIN,
            'std::cout': TokenType.STD_COUT,
            'std::endl': TokenType.STD_ENDL,
        }
        
        self.multi_char_ops = {
            '++': TokenType.INCREMENT,
            '--': TokenType.DECREMENT,
            '==': TokenType.EQUAL,
            '!=': TokenType.NOT_EQUAL,
            '&&': TokenType.AND,
            '||': TokenType.OR,
            '>>': TokenType.INPUT,
            '<<': TokenType.OUTPUT,
            'this->': TokenType.THIS,
        }
        
        self.single_chars = {
            '=': TokenType.ASSIGN,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '%': TokenType.MODULO,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '/': TokenType.DIV,
            '"': TokenType.GHILIMELE,
        }
        
        # Symbol table and FIP
        self.symbol_table = SymbolTable()
        self.fip = FIPWithCodes()
        self.errors = []
    
    def is_CHAR(self, char):
        """CHAR = "_" | " A " | "B" | ... | "Z" | "a" | ... | "z" ."""
        return char.isalpha() or char == '_'
    
    def is_CIF_OR_ZERO(self, char):
        """CIF = "1" | ... | "9"  ."""
        return char.isdigit()
    
    def is_CHAR_OR_CIF_OR_ZERO(self, char):
        return self.is_CHAR(char) or self.is_CIF_OR_ZERO(char)
    
    def read_ID(self, text, pos):
        """ID = CHAR { CHAR | CIF | "0" } ."""
        start = pos
        
        if not self.is_CHAR(text[pos]):
            return "", pos
        
        pos += 1
        while pos < len(text) and self.is_CHAR_OR_CIF_OR_ZERO(text[pos]):
            pos += 1
        
        return text[start:pos], pos
    
    def read_CONSTANT(self, text, pos):
        """ "0" | CIF { CIF | "0" } [ "." ( CIF | "0" ) { CIF | "0" } ]"""
        start = pos
        has_decimal = False
        
        if text[pos] == '0':
            pos += 1
            if pos < len(text) and text[pos] == '.':
                has_decimal = True
                pos += 1
                # Must have at least one digit after decimal point
                if pos >= len(text) or not self.is_CIF_OR_ZERO(text[pos]):
                    # Return the invalid constant to show in error message
                    return ("INVALID_DECIMAL", text[start:pos]), pos
                while pos < len(text) and self.is_CIF_OR_ZERO(text[pos]):
                    pos += 1
                # Check for second decimal point
                if pos < len(text) and text[pos] == '.':
                    # Consume the rest of the invalid constant
                    while pos < len(text) and (self.is_CIF_OR_ZERO(text[pos]) or text[pos] == '.'):
                        pos += 1
                    return ("MULTIPLE_DECIMALS", text[start:pos]), pos
            # Check if followed by invalid characters (letters)
            if pos < len(text) and self.is_CHAR(text[pos]):
                # Consume the invalid part
                while pos < len(text) and self.is_CHAR_OR_CIF_OR_ZERO(text[pos]):
                    pos += 1
                return ("INVALID_CHARS", text[start:pos]), pos
            return text[start:pos], pos
        
        if not (self.is_CIF_OR_ZERO(text[pos]) and text[pos] != '0'):
            return "", pos
        
        pos += 1
        
        while pos < len(text) and self.is_CIF_OR_ZERO(text[pos]):
            pos += 1
        
        if pos < len(text) and text[pos] == '.':
            has_decimal = True
            pos += 1
            # Must have at least one digit after decimal point
            if pos >= len(text) or not self.is_CIF_OR_ZERO(text[pos]):
                # Return the invalid constant to show in error message
                return ("INVALID_DECIMAL", text[start:pos]), pos
            while pos < len(text) and self.is_CIF_OR_ZERO(text[pos]):
                pos += 1
            # Check for second decimal point
            if pos < len(text) and text[pos] == '.':
                # Consume the rest of the invalid constant
                while pos < len(text) and (self.is_CIF_OR_ZERO(text[pos]) or text[pos] == '.'):
                    pos += 1
                return ("MULTIPLE_DECIMALS", text[start:pos]), pos
        
        # Check if followed by invalid characters (letters)
        if pos < len(text) and self.is_CHAR(text[pos]):
            # Consume the invalid part
            while pos < len(text) and self.is_CHAR_OR_CIF_OR_ZERO(text[pos]):
                pos += 1
            return ("INVALID_CHARS", text[start:pos]), pos
        
        return text[start:pos], pos
    
    def skip_whitespace(self, text, pos):
        while pos < len(text) and text[pos] in ' \t':
            pos += 1
        return pos
    
    
    def tokenize(self, text: str) -> List[Token]:
        tokens = []
        pos = 0
        line = 1
        line_start = 0
        
        while pos < len(text):
            # Skip whitespace
            if text[pos] in ' \t':
                pos = self.skip_whitespace(text, pos)
                continue
            
            # Handle newlines
            if text[pos] == '\n':
                line += 1
                line_start = pos + 1
                pos += 1
                continue
            
            column = pos - line_start + 1
            
            # Try to match multi-character operators
            matched = False
            for op_text, token_type in sorted(self.multi_char_ops.items(), 
                                             key=lambda x: len(x[0]), 
                                             reverse=True):
                if text[pos:pos+len(op_text)] == op_text:
                    tokens.append(Token(token_type, op_text, line, column))
                    pos += len(op_text)
                    matched = True
                    break
            
            if matched:
                continue
            
            # Try to match keywords
            matched = False
            for keyword, token_type in sorted(self.keywords.items(), 
                                             key=lambda x: len(x[0]), 
                                             reverse=True):
                if text[pos:pos+len(keyword)] == keyword:
                    # For alphabetic keywords, ensure word boundary
                    if keyword[0].isalpha():
                        end_pos = pos + len(keyword)
                        if (end_pos >= len(text) or 
                            not (self.is_CHAR(text[end_pos]) or 
                                 self.is_CIF_OR_ZERO(text[end_pos]))):
                            tokens.append(Token(token_type, keyword, line, column))
                            pos += len(keyword)
                            matched = True
                            break
                    else:
                        tokens.append(Token(token_type, keyword, line, column))
                        pos += len(keyword)
                        matched = True
                        break
            
            if matched:
                continue

            # Try to read numeric constant
            if self.is_CIF_OR_ZERO(text[pos]):
                const_val, new_pos = self.read_CONSTANT(text, pos)
                # Check if it's an error tuple
                if isinstance(const_val, tuple):
                    error_type, invalid_value = const_val
                    if error_type == "INVALID_DECIMAL":
                        self.errors.append(LexicalError(
                            f"Invalid numeric constant '{invalid_value}' - no digits after decimal point", 
                            line, column))
                    elif error_type == "INVALID_CHARS":
                        self.errors.append(LexicalError(
                            f"Invalid numeric constant '{invalid_value}' - contains non-digit characters", 
                            line, column))
                    elif error_type == "MULTIPLE_DECIMALS":
                        self.errors.append(LexicalError(
                            f"Invalid numeric constant '{invalid_value}' - multiple decimal points", 
                            line, column))
                    pos = new_pos
                    continue
                elif const_val:  # Valid constant
                    tokens.append(Token(TokenType.CONSTANT, const_val, line, column))
                    pos = new_pos
                    continue
                else:
                    # Empty string returned - should not happen for digits, but handle it
                    self.errors.append(LexicalError(f"Invalid numeric constant", line, column))
                    pos += 1
                    continue
            
            # Try to read identifier
            if self.is_CHAR(text[pos]):
                id_val, new_pos = self.read_ID(text, pos)
                if id_val:
                    tokens.append(Token(TokenType.IDENTIFIER, id_val, line, column))
                    pos = new_pos
                    continue
            
            # Try single character tokens
            if text[pos] in self.single_chars:
                token_type = self.single_chars[text[pos]]
                tokens.append(Token(token_type, text[pos], line, column))
                pos += 1
                continue
            
            # Unknown character - lexical error
            self.errors.append(LexicalError(f"Unknown character '{text[pos]}'", line, column))
            pos += 1
        
        return tokens
    
    def build_fip_and_ts(self, tokens):

        for token in tokens:
            if token.type == TokenType.IDENTIFIER or token.type == TokenType.CONSTANT:
                # Add to symbol table and get position (integer index)
                ts_position = self.symbol_table.add(token.value)
                # Add to FIP with TS position and atom value
                self.fip.add(token.type.value, ts_position, token.value)
            elif token.type == TokenType.DENUMIRE:
                # String literals are also stored in TS
                ts_position = self.symbol_table.add(token.value)
                self.fip.add(token.type.value, ts_position, token.value)
            else:
                # Keywords and operators: add to FIP without TS position
                self.fip.add(token.value, -1, None)
    
    def analyze_file(self, input_filename: str, 
                     fip_filename: str = None, 
                     ts_filename: str = None,
                     fip_readable_filename: str = None,
                     tokens_filename: str = None,
                     errors_filename: str = None):
        
        self.symbol_table = SymbolTable()
        self.fip = FIPWithCodes()
        self.errors = []
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        programs_dir = os.path.join(script_dir, '..', 'programs')
        
        # Build input file path
        input_path = os.path.join(programs_dir, input_filename)
        
        # Get base name without extension for output files
        base_name = input_filename.rsplit('.', 1)[0]
        if not tokens_filename:
            tokens_filename = os.path.join(programs_dir, f"{base_name}_tokens.txt")
        if not fip_filename:
            fip_filename = os.path.join(programs_dir, f"{base_name}_fip.txt")
        if not fip_readable_filename:
            fip_readable_filename = os.path.join(programs_dir, f"{base_name}_fip_readable.txt")
        if not ts_filename:
            ts_filename = os.path.join(programs_dir, f"{base_name}_ts.txt")
        if not errors_filename:
            errors_filename = os.path.join(programs_dir, f"{base_name}_errors.txt")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_path}' not found")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
        # Tokenize
        tokens = self.tokenize(source_code)

        with open(tokens_filename, 'w', encoding='utf-8') as f:
            f.write("Tokens:\n")
            f.write("="*50 + "\n")
            for token in tokens:
                f.write(f"{token.type.value} ('{token.value}') at line {token.line}, column {token.column}\n")
        
        # Build FIP and TS
        self.build_fip_and_ts(tokens)
        
        # Save outputs
        self.fip.save_to_file(fip_filename)
        self.fip.save_readable_to_file(fip_readable_filename)
        self.symbol_table.save_to_file(ts_filename)
        
        # Save or display errors
        if self.errors:
            with open(errors_filename, 'w', encoding='utf-8') as f:
                for error in self.errors:
                    f.write(str(error) + '\n')
            print(f"\n{'='*60}")
            print(f"LEXICAL ERRORS FOUND IN: {input_filename}")
            print(f"{'='*60}")
            for error in self.errors:
                print(error)
            print(f"\nErrors saved to: {errors_filename}")
            return False
        else:
            # No errors
            with open(errors_filename, 'w', encoding='utf-8') as f:
                f.write("No lexical errors found.\n")
            
            print(f"\n{'='*60}")
            print(f"ANALYSIS SUCCESSFUL: {input_filename}")
            print(f"{'='*60}")
            return True



def main():
    """Main function to test the lexical analyzer."""
    analyzer = LexicalAnalyzer()
    
    # Test files
    test_files = ['cerc.cpp', 'cmmdc.cpp', 'suma_n.cpp', 'err_1.cpp', 'err_2.cpp']
    
    for test_file in test_files:
        print(f"\n{'#'*70}")
        print(f"# Analyzing: {test_file}")
        print(f"{'#'*70}")
        
        success = analyzer.analyze_file(test_file)
        
        if success:
            print("\n✓ Analysis completed successfully!")
        else:
            print("\n✗ Analysis completed with errors!")
        
        print()


if __name__ == "__main__":
    main()
