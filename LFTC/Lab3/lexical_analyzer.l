%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Structuri pentru tabela de simboluri (Hash Table) */
#define TS_SIZE 211  // Numar prim pentru hash table
#define MAX_IDENTIFIERS 1000
#define MAX_CONSTANTS 1000

typedef struct TSEntry {
    char *value;
    int line_number;
    struct TSEntry *next;
} TSEntry;

typedef struct {
    TSEntry *table[TS_SIZE];
    int count;
} SymbolTable;

/* Declarare tabele de simboluri */
SymbolTable ts_identifiers;
SymbolTable ts_constants;

/* Declarare fisiere */
FILE *fip_file;
FILE *ts_id_file;
FILE *ts_const_file;

int line_number = 1;
int error_count = 0;

/* Functii pentru tabela de simboluri */
unsigned int hash_function(const char *str) {
    unsigned int hash = 0;
    while (*str) {
        hash = (hash * 31 + *str) % TS_SIZE;
        str++;
    }
    return hash;
}

void init_symbol_table(SymbolTable *st) {
    for (int i = 0; i < TS_SIZE; i++) {
        st->table[i] = NULL;
    }
    st->count = 0;
}

int add_to_symbol_table(SymbolTable *st, const char *value, FILE *ts_file) {
    unsigned int hash = hash_function(value);
    TSEntry *current = st->table[hash];
    
    /* Verificare daca exista deja */
    while (current != NULL) {
        if (strcmp(current->value, value) == 0) {
            return current->line_number;
        }
        current = current->next;
    }
    
    /* Adaugare element nou */
    TSEntry *new_entry = (TSEntry*)malloc(sizeof(TSEntry));
    new_entry->value = strdup(value);
    new_entry->line_number = st->count + 1;
    new_entry->next = st->table[hash];
    st->table[hash] = new_entry;
    st->count++;
    
    /* Scriere in fisier TS */
    fprintf(ts_file, "%s\n", value);
    
    return new_entry->line_number;
}

void write_to_fip(int token_code, int ts_position) {
    fprintf(fip_file, "%d %d\n", token_code, ts_position);
}

void cleanup_symbol_table(SymbolTable *st) {
    for (int i = 0; i < TS_SIZE; i++) {
        TSEntry *current = st->table[i];
        while (current != NULL) {
            TSEntry *temp = current;
            current = current->next;
            free(temp->value);
            free(temp);
        }
    }
}

%}

/* Definitii */
DIGIT           [1-9]
DIGIT_ZERO      [0-9]
LETTER          [a-zA-Z_]
IDENTIFIER      {LETTER}({LETTER}|{DIGIT_ZERO})*
INTEGER         (0|{DIGIT}{DIGIT_ZERO}*)
DOUBLE          {INTEGER}\.{DIGIT_ZERO}+
CONSTANT        {INTEGER}|{DOUBLE}
STRING          \"[^\"]*\"
WHITESPACE      [ \t\r]+
NEWLINE         \n

%%
{WHITESPACE}    { /* Ignora spatiile */ }
{NEWLINE}       { line_number++; }

"#include"      { write_to_fip(0, -1); }
"<iostream>"    { write_to_fip(1, -1); }
"struct"        { write_to_fip(2, -1); }
"int"           { write_to_fip(3, -1); }
"double"        { write_to_fip(4, -1); }
"main"          { write_to_fip(5, -1); }
"return"        { write_to_fip(6, -1); }
"if"            { write_to_fip(7, -1); }
"else"          { write_to_fip(8, -1); }
"while"         { write_to_fip(9, -1); }
"std::cin"      { write_to_fip(10, -1); }
"std::cout"     { write_to_fip(11, -1); }
"std::endl"     { write_to_fip(12, -1); }
"this->"        { write_to_fip(13, -1); }

"=="            { write_to_fip(28, -1); }
"!="            { write_to_fip(29, -1); }
"++"            { write_to_fip(26, -1); }
"--"            { write_to_fip(27, -1); }
"&&"            { write_to_fip(30, -1); }
"||"            { write_to_fip(31, -1); }
">>"            { write_to_fip(32, -1); }
"<<"            { write_to_fip(33, -1); }

"="             { write_to_fip(20, -1); }
"+"             { write_to_fip(21, -1); }
"-"             { write_to_fip(22, -1); }
"*"             { write_to_fip(23, -1); }
"/"             { write_to_fip(24, -1); }
"%"             { write_to_fip(25, -1); }

"("             { write_to_fip(40, -1); }
")"             { write_to_fip(41, -1); }
"{"             { write_to_fip(42, -1); }
"}"             { write_to_fip(43, -1); }
";"             { write_to_fip(44, -1); }
","             { write_to_fip(45, -1); }
"."             { write_to_fip(46, -1); }
"\""            { write_to_fip(47, -1); }

{STRING}        {
                    int pos = add_to_symbol_table(&ts_constants, yytext, ts_const_file);
                    write_to_fip(102, pos);
                }

{CONSTANT}      {
                    int pos = add_to_symbol_table(&ts_constants, yytext, ts_const_file);
                    write_to_fip(101, pos);
                }

{IDENTIFIER}    {
                    int pos = add_to_symbol_table(&ts_identifiers, yytext, ts_id_file);
                    write_to_fip(100, pos);
                }

.               {
                    printf("EROARE LEXICALA la linia %d: caracter invalid '%s'\n", line_number, yytext);
                    error_count++;
                }

%%

int yywrap() {
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Utilizare: %s <fisier_sursa>\n", argv[0]);
        return 1;
    }
    
    /* Deschidere fisier intrare */
    FILE *input_file = fopen(argv[1], "r");
    if (!input_file) {
        printf("Eroare: Nu pot deschide fisierul '%s'\n", argv[1]);
        return 1;
    }
    
    /* Deschidere fisiere iesire */
    fip_file = fopen("FIP.out", "w");
    ts_id_file = fopen("TS_IDENTIFIERS.out", "w");
    ts_const_file = fopen("TS_CONSTANTS.out", "w");
    
    if (!fip_file || !ts_id_file || !ts_const_file) {
        printf("Eroare: Nu pot crea fisierele de iesire\n");
        return 1;
    }
    
    /* Initializare tabele de simboluri */
    init_symbol_table(&ts_identifiers);
    init_symbol_table(&ts_constants);
    
    /* Scriere header in FIP */
    fprintf(fip_file, "Token_Code TS_Position\n");
    fprintf(fip_file, "=======================\n");
    
    /* Analiza lexicala */
    yyin = input_file;
    yylex();
    
    /* Inchidere fisiere */
    fclose(input_file);
    fclose(fip_file);
    fclose(ts_id_file);
    fclose(ts_const_file);
    
    /* Cleanup */
    cleanup_symbol_table(&ts_identifiers);
    cleanup_symbol_table(&ts_constants);
    
    /* Raport final */
    printf("\n========================================\n");
    printf("Analiza lexicala finalizata!\n");
    printf("========================================\n");
    printf("Linii procesate: %d\n", line_number - 1);
    printf("Identificatori unici: %d\n", ts_identifiers.count);
    printf("Constante unice: %d\n", ts_constants.count);
    
    if (error_count == 0) {
        printf("\nSUCCES: Nu au fost gasite erori lexicale!\n");
        printf("\nFisiere generate:\n");
        printf("  - FIP.out (Forma Interna a Programului)\n");
        printf("  - TS_IDENTIFIERS.out (Tabela Simboluri - Identificatori)\n");
        printf("  - TS_CONSTANTS.out (Tabela Simboluri - Constante)\n");
    } else {
        printf("\nERORE: %d erori lexicale gasite!\n", error_count);
    }
    printf("========================================\n");
    
    return error_count > 0 ? 1 : 0;
}