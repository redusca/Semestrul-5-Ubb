#https://en.cppreference.com/w/c/language/integer_constant.html

from enum import Enum
from dataclasses import dataclass
import os
import sys
from typing import List

from symbol_table import SymbolTable
from fip import FIPWithCodes

# Import finite automaton
from finite_automaton import AutomatFinit

class TokenType(Enum):
    # Cuvinte rezervate
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
    
    # Semne
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


class LexicalAnalyzerFA:
    """Lexical Analyzer using Finite Automata for identifiers, integers, and real numbers."""
    
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
        
        # Load finite automata
        self.fa_identifier = AutomatFinit()
        self.fa_integer = AutomatFinit()
        self.fa_real = AutomatFinit()
        
        self._load_af()
    
    def _load_af(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        id_file = os.path.join(script_dir, 'af_identifier.txt')
        if not self.fa_identifier.read_from_file(id_file):
            print(f"Warning: Failed to load identifier automaton from {id_file}")
        int_file = os.path.join(script_dir, 'af_integer.txt')
        if not self.fa_integer.read_from_file(int_file):
            print(f"Warning: Failed to load integer automaton from {int_file}")
        real_file = os.path.join(script_dir, 'af_real.txt')
        if not self.fa_real.read_from_file(real_file):
            print(f"Warning: Failed to load real number automaton from {real_file}")
    
    def is_CHAR(self, char):
        """CHAR = "_" | "A" | "B" | ... | "Z" | "a" | ... | "z"."""
        return char.isalpha() or char == '_' or char == "'"
    
    def is_CIF_OR_ZERO(self, char):
        """CIF | "0" = "0" | "1" | ... | "9"."""
        return char.isdigit()
    
    def recognize_with_af(self, fa, text, pos):
        if pos >= len(text):
            return "", pos
        
        current_state = fa.initial_state
        longest_match = ""
        longest_match_pos = pos
        start_pos = pos
        
        while pos < len(text):
            char = text[pos]

            #Tranzitia   
            key = (current_state, char)
            
            # daca exista tranzitie
            if key in fa.transitions and fa.transitions[key]:
                current_state = fa.transitions[key][0]
                pos += 1
                
                if current_state in fa.final_states:
                    longest_match = text[start_pos:pos]
                    longest_match_pos = pos
            else:
                break
        
        return longest_match, longest_match_pos
    
    def read_ID_with_FA(self, text, pos):
        return self.recognize_with_af(self.fa_identifier, text, pos)
    
    def read_CONSTANT_with_FA(self, text, pos):
        real_match, real_pos = self.recognize_with_af(self.fa_real, text, pos)
        
        int_match, int_pos = self.recognize_with_af(self.fa_integer, text, pos)
        if len(real_match) > len(int_match):
            return real_match, real_pos
        elif len(int_match) > 0:
            return int_match, int_pos
        
        return "", pos
    
    def skip_whitespace(self, text, pos):
        while pos < len(text) and text[pos] in ' \t':
            pos += 1
        return pos
    
    def detect_integer_error(self, text, pos):
        start = pos
        
        # Check for incomplete hex literal (0x without digits)
        if pos + 1 < len(text) and text[pos:pos+2] in ['0x', '0X']:
            end_pos = pos + 2
            # Check if followed by valid hex digits
            if end_pos >= len(text) or not text[end_pos] in '0123456789abcdefABCDEF':
                # Consume any remaining invalid characters
                while end_pos < len(text) and (text[end_pos].isalnum() or text[end_pos] in "'."):
                    end_pos += 1
                return f"Incomplete hexadecimal literal '{text[start:end_pos]}' - missing hex digits after '0x'", end_pos
        
        # Check for incomplete binary literal (0b without digits)
        if pos + 1 < len(text) and text[pos:pos+2] in ['0b', '0B']:
            end_pos = pos + 2
            # Check if followed by valid binary digits
            if end_pos >= len(text) or not text[end_pos] in '01':
                # Consume any remaining invalid characters
                while end_pos < len(text) and (text[end_pos].isalnum() or text[end_pos] in "'."):
                    end_pos += 1
                return f"Incomplete binary literal '{text[start:end_pos]}' - missing binary digits after '0b'", end_pos
        
        # Check for invalid octal digits (8 or 9 in octal)
        if text[pos] == '0' and pos + 1 < len(text) and text[pos+1].isdigit():
            end_pos = pos
            while end_pos < len(text) and text[end_pos].isdigit():
                if text[end_pos] in '89':
                    # Found invalid octal digit
                    while end_pos < len(text) and (text[end_pos].isalnum() or text[end_pos] in "'."):
                        end_pos += 1
                    return f"Invalid octal literal '{text[start:end_pos]}' - contains invalid octal digits (8 or 9)", end_pos
                end_pos += 1
        
        # Check for invalid prefix (0 followed by invalid letter like 0c, 0d, etc.)
        if text[pos] == '0' and pos + 1 < len(text) and text[pos+1].isalpha():
            if text[pos+1] not in 'xXbB':
                end_pos = pos
                while end_pos < len(text) and (text[end_pos].isalnum() or text[end_pos] in "'."):
                    end_pos += 1
                return f"Invalid numeric prefix in '{text[start:end_pos]}' - expected '0x', '0X', '0b', or '0B'", end_pos
        
        # Check for invalid hex digits
        if pos + 1 < len(text) and text[pos:pos+2] in ['0x', '0X']:
            end_pos = pos + 2
            while end_pos < len(text) and (text[end_pos] in '0123456789abcdefABCDEF' or text[end_pos] == "'"):
                end_pos += 1
            # Check if followed by invalid characters
            if end_pos < len(text) and text[end_pos].isalnum():
                temp = end_pos
                while temp < len(text) and (text[temp].isalnum() or text[temp] in "'."):
                    temp += 1
                return f"Invalid hexadecimal literal '{text[start:temp]}' - contains non-hex characters", temp
        
        # Check for invalid binary digits
        if pos + 1 < len(text) and text[pos:pos+2] in ['0b', '0B']:
            end_pos = pos + 2
            while end_pos < len(text) and (text[end_pos] in '01' or text[end_pos] == "'"):
                end_pos += 1
            # Check if followed by invalid characters (2-9 or letters)
            if end_pos < len(text) and text[end_pos].isalnum():
                temp = end_pos
                while temp < len(text) and (text[temp].isalnum() or text[temp] in "'."):
                    temp += 1
                return f"Invalid binary literal '{text[start:temp]}' - contains non-binary digits", temp
        
        # Check for invalid suffixes (like UU, LUL, Lu, etc.)
        # This will be caught by the FA, but we can provide better messages
        end_pos = pos
        while end_pos < len(text) and (text[end_pos].isdigit() or text[end_pos] == "'"):
            end_pos += 1
        
        if end_pos < len(text) and text[end_pos] in 'uUlLwW':
            suffix = ''
            while end_pos < len(text) and text[end_pos] in 'uUlL':
                suffix += text[end_pos]
                end_pos += 1
            
            # Check for invalid suffix combinations
            # Valid suffixes in C++: u, U, l, L, ll, LL, ul, UL, ull, ULL, llu, LLU
            # Key: u/U can come before or after l/ll but NOT after l (no Lu, no lU)
            suffix_lower = suffix.lower()
            valid_suffixes = ['u', 'l', 'll', 'ul', 'ull', 'llu']
            
            if suffix_lower not in valid_suffixes:
                return f"Invalid integer suffix in '{text[start:end_pos]}' - '{suffix}' is not a valid suffix (use u, l, ll, ul, ull, llu)", end_pos
        
        return None, pos
    
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

            # AF CONSTANT
            if self.is_CIF_OR_ZERO(text[pos]):
                const_val, new_pos = self.read_CONSTANT_with_FA(text, pos)

                if const_val and new_pos > pos:
                    # Check if the recognized constant is followed by invalid characters
                    # This includes: digits, letters (including suffix chars like u,U,l,L which indicate invalid suffix)
                    if new_pos < len(text) and (self.is_CIF_OR_ZERO(text[new_pos]) or self.is_CHAR(text[new_pos])):
                        # FA recognized partial constant, but there's invalid continuation
                        # Call error detection function
                        error_msg, error_pos = self.detect_integer_error(text, pos)
                        if error_msg:
                            self.errors.append(LexicalError(error_msg, line, column))
                            pos = error_pos
                        else:
                            # Fallback error message
                            invalid_start = pos
                            invalid_pos = new_pos
                            while invalid_pos < len(text) and (self.is_CHAR(text[invalid_pos]) or 
                                                               self.is_CIF_OR_ZERO(text[invalid_pos]) or
                                                               text[invalid_pos] in "'"):
                                invalid_pos += 1
                            invalid_value = text[invalid_start:invalid_pos]
                            self.errors.append(LexicalError(
                                f"Invalid numeric constant '{invalid_value}' - unrecognized format", 
                                line, column))
                            pos = invalid_pos
                        continue
                    
                    # Valid constant recognized
                    tokens.append(Token(TokenType.CONSTANT, const_val, line, column))
                    pos = new_pos
                    continue
                else:
                    # FA couldn't recognize anything - check for specific integer errors
                    error_msg, error_pos = self.detect_integer_error(text, pos)
                    if error_msg:
                        self.errors.append(LexicalError(error_msg, line, column))
                        pos = error_pos
                        continue
                    else:
                        # Generic error
                        invalid_start = pos
                        while pos < len(text) and (self.is_CIF_OR_ZERO(text[pos]) or 
                                                   text[pos] in "'.xXbBaAcCdDeEfF"):
                            pos += 1
                        invalid_value = text[invalid_start:pos]
                        self.errors.append(LexicalError(
                            f"Invalid numeric constant '{invalid_value}' - unrecognized format", 
                            line, column))
                        continue
                    
            # AF INDENTIFIER
            if self.is_CHAR(text[pos]):
                id_val, new_pos = self.read_ID_with_FA(text, pos)
                
                if id_val:
                    tokens.append(Token(TokenType.IDENTIFIER, id_val, line, column))
                    pos = new_pos
                    continue
                else:
                    # FA couldn't recognize it (shouldn't happen for valid identifiers)
                    self.errors.append(LexicalError(
                        f"Invalid identifier starting at '{text[pos]}'", 
                        line, column))
                    pos += 1
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
                ts_position = self.symbol_table.add(token.value)
                self.fip.add(token.type.value, ts_position, token.value)
            elif token.type == TokenType.DENUMIRE:
                ts_position = self.symbol_table.add(token.value)
                self.fip.add(token.type.value, ts_position, token.value)
            else:
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
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(script_dir, input_filename)
        if not os.path.exists(input_path):
            programs_dir = os.path.join(script_dir, '..', 'Lab1', 'programs')
            input_path = os.path.join(programs_dir, input_filename)
        
        base_name = input_filename.rsplit('.', 1)[0]
        output_dir = script_dir
        
        if not tokens_filename:
            tokens_filename = os.path.join(output_dir, f"{base_name}_tokens.txt")
        if not fip_filename:
            fip_filename = os.path.join(output_dir, f"{base_name}_fip.txt")
        if not fip_readable_filename:
            fip_readable_filename = os.path.join(output_dir, f"{base_name}_fip_readable.txt")
        if not ts_filename:
            ts_filename = os.path.join(output_dir, f"{base_name}_ts.txt")
        if not errors_filename:
            errors_filename = os.path.join(output_dir, f"{base_name}_errors.txt")
        
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
            print(f"  Tokens file: {tokens_filename}")
            print(f"  FIP file: {fip_filename}")
            print(f"  FIP readable: {fip_readable_filename}")
            print(f"  Symbol Table: {ts_filename}")
            return True


def main():
    analyzer = LexicalAnalyzerFA()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    programe_dir = os.path.join(script_dir, 'programe')
    if not os.path.exists(programe_dir):
        print(f"Error: Directory '{programe_dir}' not found")
        return
    test_files = []
    for filename in os.listdir(programe_dir):
        if filename.endswith('.cpp'):
            test_files.append(os.path.join('programe', filename))
    test_files.sort()
    if not test_files:
        print(f"No .cpp files found in {programe_dir}")
        return
    
    print(f"\nFound {len(test_files)} .cpp file(s) to analyze")
    
    for test_file in test_files:
        print(f"\n{'#'*70}")
        print(f"# Analyzing: {test_file}")
        print(f"{'#'*70}")
        
        success = analyzer.analyze_file(test_file)
        
        if success:
            print("\n[OK] Analysis completed successfully!")
        else:
            print("\n[ERROR] Analysis completed with errors!")
        
        print()


if __name__ == "__main__":
    main()
