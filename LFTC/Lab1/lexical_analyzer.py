from enum import Enum
from dataclasses import dataclass

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

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = {
            '#include': TokenType.INCLUDE,
            '<iostream>': TokenType.IOSTREAM,
            'STRUCT': TokenType.STRUCT,
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
        
        if text[pos] == '0':
            pos += 1
            if pos < len(text) and text[pos] == '.':
                pos += 1
                while pos < len(text) and self.is_CIF_OR_ZERO(text[pos]):
                    pos += 1
            return text[start:pos], pos
        
        if not (self.is_CIF_OR_ZERO(text[pos]) and text[pos] != '0'):
            return "", pos
        
        pos += 1
        
        while pos < len(text) and self.is_CIF_OR_ZERO(text[pos]):
            pos += 1
        
        if pos < len(text) and text[pos] == '.':
            pos += 1
            while pos < len(text) and self.is_CIF_OR_ZERO(text[pos]):
                pos += 1
        
        return text[start:pos], pos
    
    def skip_whitespace(self, text, pos):
        while pos < len(text) and text[pos] in ' \t':
            pos += 1
        return pos
    
    def tokenize(self, text) :
        tokens = []
        pos = 0
        line = 1
        line_start = 0
        
        while pos < len(text):
            if text[pos] in ' \t':
                pos = self.skip_whitespace(text, pos)
                continue
            
            if text[pos] == '\n':
                line += 1
                line_start = pos + 1
                pos += 1
                continue
            
            column = pos - line_start + 1
            
            found_multi = False
            for op_text, token_type in sorted(self.multi_char_ops.items(), key=len, reverse=True):
                if text[pos:pos+len(op_text)] == op_text:
                    tokens.append(Token(token_type, op_text, line, column))
                    pos += len(op_text)
                    found_multi = True
                    break
            
            if found_multi:
                continue
            
            found_keyword = False
            for keyword, token_type in sorted(self.keywords.items(), key=len, reverse=True):
                if text[pos:pos+len(keyword)] == keyword:
                    if keyword.isalpha():
                        if (pos + len(keyword) >= len(text) or 
                            not self.is_CHAR_OR_CIF_OR_ZERO(text[pos + len(keyword)])):
                            tokens.append(Token(token_type, keyword, line, column))
                            pos += len(keyword)
                            found_keyword = True
                            break
                    else:
                        tokens.append(Token(token_type, keyword, line, column))
                        pos += len(keyword)
                        found_keyword = True
                        break
            
            if found_keyword:
                continue
            
            if self.is_CIF_OR_ZERO(text[pos]):
                const_val, new_pos = self.read_CONSTANT(text, pos)
                if const_val:
                    tokens.append(Token(TokenType.CONSTANT, const_val, line, column))
                    pos = new_pos
                    continue

            if self.is_CHAR(text[pos]):
                id_val, new_pos = self.read_ID(text, pos)
                if id_val:
                    tokens.append(Token(TokenType.IDENTIFIER, id_val, line, column))
                    pos = new_pos
                    continue
            
            if text[pos] in self.single_chars:
                token_type = self.single_chars[text[pos]]
                tokens.append(Token(token_type, text[pos], line, column))
                pos += 1
                continue
            
            # skip unknown characters
            pos += 1
        return tokens
    
    def print_tokens(self, tokens):
        for token in tokens:
            print(f"{token.value}")
    
    def write_tokens_to_file(self, tokens, output_filename):
        try:
            with open(output_filename, 'w', encoding='utf-8') as file:
                for token in tokens:
                    file.write(f"{token.value}\n")
                    
        except Exception as e:
            print(f"Error writing tokens to file: {e}")

    def analyze_file(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            tokens = self.tokenize(content)
            
            base_name = filename.split('.')[0]
            output_filename = f"{base_name}_tokens.txt"
            
            self.write_tokens_to_file(tokens, output_filename)
            print(f"Tokens written to: {output_filename}")
            
            self.print_tokens(tokens)
            return tokens
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

def main():
    analyzer = LexicalAnalyzer()
    
    
    cpp_files = ['err_1.cpp', 'err_2.cpp']
    
    for cpp_file in cpp_files:
       print(f"\n--- {cpp_file} ---")
       analyzer.analyze_file(cpp_file)

if __name__ == "__main__":
    main()