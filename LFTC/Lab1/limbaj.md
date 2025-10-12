(* EBNF : *)

(* Program si Intructiuni * )

PROGRAM = "#include" "<iostream>" { STRUCT } "int" "main "(" ")" "{" { INSTR } INSTR_RETURN ";" "}" .
STRUCT = "STRUCT" DENUMIRE "{" {INSTR_ATRIBUIRE} {METODA} "}" ";" .
METODA = TIP_DATE DENUMIRE "(" [TIP_DATE ID {","TIP_DATE ID} ] ")" "{" { THIS | INSTR } INSTR_RETURN ";" "}". 
THIS = "this->"ID "=" PARAM .

INSTR = ( INSTR_ATRIBUIRE | INSTR_RETURN | INSTR_OP | INSTR_IN | INSTR_OUT | INSTR_COND | INSTR_CICLARE | INSTR_METODA ) ";" .
INSTR_ATRIBUIRE = TIP_DATE LIST_VAR .
INSTR_RETURN = "return" PARAM
INSTR_OP = (ID "=" PARAM ) | INC | DEC
INSTR_IN = "std::cin" ">>" ID { ">>" ID }
INSTR_OUT = "std:cout""<<" ( PARAM | INSTR_METODA | ( """DENUMIRE""" ) | "std::endl" ) {"<<" ( PARAM | INSTR_METODA | ( """ DENUMIRE """ ) | "std::endl" ) } .
INSTR_COND = "if" "(" LIST_COND ")" "{" { INSTR } "}" [ "else" "{" { INSTR } "}" ] .\
INSTR_CICLARE = "while" "(" LIST_COND ")" "{" { INSTR } "}" .
INSTR_METODA = ID"."DENUMIRE"(" { PARAM } ")" .

(* Contante si variabile + Operatie *)

SEMN_OP = "+" | "-" | "*" | "%" | "/" .
ID = CHAR { CHAR | CIF | "0" } .
CIF = "1" | ... | "9"  .
CONST = "0" | CIF { CIF | "0" } [ "." ( CIF | "0" ) { CIF | "0" } ] .
DENUMIRE = CHAR { CHAR } .
TIP_DATE = "int" | "double" | STRUCT .
LIST_VAR = ( ID | ID "=" CONST ) {"," ID | ID "=" CONST}.
CHAR = "_" | " A " | "B" | ... | "Z" | "a" | ... | "z" .
OPERATIE = (ID | CONST) SEMN_OP (ID | CONST) { SEMN_OP (ID | CONST) } .
INC = ID"++" .
DEC = ID"--" .

PARAM = ID | CONST | OPERATIE .

LIST_COND = COND { ( "&&" | "||" ) COND } .
COND = PARAM ( " == " | " != " ) PARAM .