class AutomatFinit:
    
    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.initial_state = None
        self.final_states = set()
        self.transitions = {}  # {(from_state, symbol): [to_states]}
    
    def _validate_state_format(self, state):
        if not state or len(state) < 2:
            return False
        # First character should be a letter (CHAR)
        if not state[0].isalpha():
            return False
        # Remaining characters should be digits (number)
        if not state[1:].isdigit():
            return False
        return True
    
    def _validate_initial_state_format(self, state):
        if not state or len(state) < 2:
            return False
        # First character should be a letter
        if not state[0].isalpha():
            return False
        # Should end with "0"
        if not state.endswith('0'):
            return False
        # Middle part (if any) should be digits
        if len(state) > 2 and not state[1:-1].isdigit():
            return False
        return True
    
    def _validate_alphabet_symbol(self, symbol):
        if len(symbol) == 1 and symbol.isdigit():
            return True
        if len(symbol) == 1 and symbol.isalpha():
            return True
        if symbol in ['-', '+', '.', "'"]:
            return True
        return False
    
    def read_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if len(lines) < 4:
                print("Eroare: Fisierul trebuie sa contina cel putin 4 linii (alfabet, stari, stare initiala, stari finale)")
                return False
            
            # Alphabet (lista_alfabet)
            alphabet_symbols = [s.strip() for s in lines[0].split(',')]
            for symbol in alphabet_symbols:
                if not self._validate_alphabet_symbol(symbol):
                    print(f"Error: Simbolul '{symbol}' nu respecta specificatia EBNF pentru alfabet")
                    print("  Expected: cifra (0-9), litera (a-z, A-Z) sau simboluri speciale (-, +, .)")
                    return False

            # States (stari)
            state_list = [s.strip() for s in lines[1].split(',')]
            for state in state_list:
                if not self._validate_state_format(state):
                    print(f"Error: Starea '{state}' nu respecta formatul EBNF")
                    print("  Format Expected: litera urmata de numar (ex: q0, q1, s10)")
                    return False
            
            # Initial state 
            initial_state = lines[2].strip()
            if not self._validate_initial_state_format(initial_state):
                print(f"Error: Starea initiala '{initial_state}' nu respecta formatul EBNF")
                print("  Format Expected: litera urmata de '0' (ex: q0, s0)")
                return False

            if initial_state not in state_list:
                print(self.states)
                print(f"Eroare: Starea initiala '{initial_state}' nu se afla in multimea starilor")
                return False
            
            # Final states (stari_finale)
            final_state_list = [s.strip() for s in lines[3].split(',')]
            for state in final_state_list:
                if not self._validate_state_format(state):
                    print(f"Error: Starea finala '{state}' nu respecta formatul EBNF")
                    return False
            
            if not set(final_state_list).issubset(set(state_list)):
                print("Eroare: Unele stari finale nu se afla in multimea starilor")
                return False
            
            # tranzitii
            transitions = {}
            for i in range(4, len(lines)):
                parts = [p.strip() for p in lines[i].split(',')]
                if len(parts) < 3:
                    print(f"Error: Se omite tranzitia invalida de la linia {i+1}")
                    print(f"  Format Expected: stare_sursa,stare_dest,simbol1[,simbol2,...]")
                    return False
                
                from_state = parts[0]
                to_state = parts[1]
                symbols = parts[2:]
                
                # Validate transition format
                if not self._validate_state_format(from_state):
                    print(f"Error: Starea sursa '{from_state}' din tranzitia de la linia {i+1} nu respecta formatul EBNF")
                    return False
                          
                if from_state not in state_list:
                    print(f"Eroare: Starea sursa '{from_state}' din tranzitia de la linia {i+1} nu se afla in multimea starilor")
                    return False

                if not self._validate_state_format(to_state):
                    print(f"Error: Starea destinatie '{to_state}' din tranzitia de la linia {i+1} nu respecta formatul EBNF")
                    return False

                if to_state not in state_list:
                    print(f"Eroare: Starea destinatie '{to_state}' din tranzitia de la linia {i+1} nu se afla in multimea starilor")
                    return False
                
                for symbol in symbols:
                    if symbol not in alphabet_symbols:
                        print(f"Eroare: Simbolul '{symbol}' din tranzitia de la linia {i+1} nu se afla in alfabet")
                        return False
                    
                    key = (from_state, symbol)
                    if key not in transitions:
                        transitions[key] = []
                    transitions[key].append(to_state)

            self.alphabet = set(alphabet_symbols)
            self.states = set(state_list)
            self.initial_state = initial_state
            self.final_states = set(final_state_list)
            self.transitions = transitions
            
            print(f"\nAutomat finit incarcat cu succes din '{filename}'")
            print(f"  Stari: {len(self.states)}, Alfabet: {len(self.alphabet)}, Tranzitii: {len(self.transitions)}")
            return True
            
        except FileNotFoundError:
            print(f"Eroare: Fisierul '{filename}' nu a fost gasit")
            return False
        except Exception as e:
            print(f"Eroare la citirea fisierului: {e}")
            return False
    
    def read_from_keyboard(self):
        try:
            print("\n" + "="*60)
            print("Introduceti Definitia Automatului Finit (Format EBNF)")
            print("="*60)
            print("Cerinte EBNF:")
            print("  - Alfabet: cifre (0-9), litere (a-z, A-Z) sau -, +, .")
            print("  - Stari: litera urmata de numar (ex: q0, q1, s10)")
            print("  - Stare initiala: litera urmata de 0 (ex: q0, s0)")
            print("="*60)
            
            # Read alphabet
            print("\nIntroduceti simbolurile alfabetului (separate prin virgula):")
            print("Exemplu: 0,1,2,a,b,-")
            alphabet_input = input("> ").strip()
            alphabet_symbols = [s.strip() for s in alphabet_input.split(',')]
            
            # Validate alphabet
            invalid_symbols = []
            for symbol in alphabet_symbols:
                if not self._validate_alphabet_symbol(symbol):
                    invalid_symbols.append(symbol)
            
            if invalid_symbols:
                print(f"\nError: Urmatoarele simboluri nu respecta EBNF:")
                for symbol in invalid_symbols:
                    print(f"  - '{symbol}' (Expected: cifra, litera sau -, +, .)")
                return False
            
            # Read states
            print("\nIntroduceti starile (separate prin virgula):")
            print("Format: litera + numar (ex: q0,q1,q2 sau s0,s1,s2)")
            states_input = input("> ").strip()
            state_list = [s.strip() for s in states_input.split(',')]
            
            # Validate states
            for state in state_list:
                if not self._validate_state_format(state):
                    print(f"\nError: Starea '{state}' nu respecta EBNF")
                    print(f"  Expected: litera urmata de numar, ex: q0, s10")
                    return False
            
            # Read initial state
            print("\nIntroduceti starea initiala:")
            print("Format: litera + 0 (ex: q0, s0)")
            initial_state = input("> ").strip()
            
            if not self._validate_initial_state_format(initial_state):
                print(f"\nError: Starea initiala '{initial_state}' nu respecta EBNF")
                print("  Expected: litera urmata de 0 (ex: q0, s0)")
                return False
            
            if initial_state not in state_list:
                print(f"Eroare: Starea initiala '{initial_state}' nu se afla in multimea starilor")
                return False
            
            # Read final states
            print("\nIntroduceti starile finale (separate prin virgula):")
            final_states_input = input("> ").strip()
            final_state_list = [s.strip() for s in final_states_input.split(',')]
            
            # Validate final states
            for state in final_state_list:
                if not self._validate_state_format(state):
                    print(f"\nError: Starea finala '{state}' nu respecta EBNF")
                    return False
            
            if not set(final_state_list).issubset(set(state_list)):
                print("Eroare: Unele stari finale nu se afla in multimea starilor")
                return False
            
            # Read transitions
            print("\nIntroduceti tranzitiile (format: stare_sursa,stare_dest,simbol1,simbol2,...)")
            print("Exemplu: q0,q1,a,b")
            print("Introduceti linie goala pentru a termina:")
            transitions = {}
            
            while True:
                transition_input = input("> ").strip()
                if not transition_input:
                    break
                
                parts = [p.strip() for p in transition_input.split(',')]
                if len(parts) < 3:
                    print("  Format invalid. Necesar cel putin: stare_sursa,stare_dest,simbol")
                    continue
                
                from_state = parts[0]
                to_state = parts[1]
                symbols = parts[2:]
                
                # Validate transition states
                if not self._validate_state_format(from_state):
                    print(f"  Error: Starea sursa '{from_state}' nu respecta formatul EBNF")
                    continue
                
                if not self._validate_state_format(to_state):
                    print(f"  Error: Starea destinatie '{to_state}' nu respecta formatul EBNF")
                    continue
                
                if from_state not in state_list:
                    print(f"  Eroare: Starea sursa '{from_state}' nu se afla in multimea starilor")
                    continue
                
                if to_state not in state_list:
                    print(f"  Eroare: Starea destinatie '{to_state}' nu se afla in multimea starilor")
                    continue
                
                # Add transitions for each symbol
                for symbol in symbols:
                    if symbol not in alphabet_symbols:
                        print(f"  Error: Simbolul '{symbol}' nu se afla in alfabet. Se omite.")
                        continue
                    
                    key = (from_state, symbol)
                    if key not in transitions:
                        transitions[key] = []
                    transitions[key].append(to_state)
            
            # Only initialize instance attributes after all validation passes
            self.alphabet = set(alphabet_symbols)
            self.states = set(state_list)
            self.initial_state = initial_state
            self.final_states = set(final_state_list)
            self.transitions = transitions
            
            print("\n" + "="*60)
            print("Automat finit incarcat cu succes de la tastatura")
            print(f"Stari: {len(self.states)}, Alfabet: {len(self.alphabet)}, Tranzitii: {len(self.transitions)}")
            print("="*60)
            return True
            
        except Exception as e:
            print(f"Eroare la citirea de la tastatura: {e}")
            return False
    
    def display_states(self):
        print("\n=== Stari ===")
        print(f"Stari: {', '.join(sorted(self.states))}")
        print(f"Total: {len(self.states)} stari")
    
    def display_alphabet(self):
        print("\n=== Alfabet ===")
        print(f"Alfabet: {', '.join(sorted(self.alphabet))}")
        print(f"Total: {len(self.alphabet)} simboluri")
    
    def display_transitions(self):
        print("\n=== Tranzitii ===")
        if not self.transitions:
            print("Nu sunt definite tranzitii")
            return
        
        transitions_by_state = {}
        for (from_state, symbol), to_states in self.transitions.items():
            if from_state not in transitions_by_state:
                transitions_by_state[from_state] = []
            for to_state in to_states:
                transitions_by_state[from_state].append((symbol, to_state))
        
        for state in sorted(transitions_by_state.keys()):
            print(f"\nDin starea '{state}':")
            for symbol, to_state in sorted(transitions_by_state[state]):
                print(f"  --[{symbol}]--> {to_state}")
    
    def display_final_states(self):
        """Display the set of final states."""
        print("\n=== Stari Finale ===")
        print(f"Stari finale: {', '.join(sorted(self.final_states))}")
        print(f"Total: {len(self.final_states)} stari finale")
    
    def is_deterministic(self):
        for to_states in self.transitions.values():
            if len(to_states) > 1:
                return False
        return True

    #determinist 
    def verify_sequence(self, sequence):
        if not self.is_deterministic():
            return False, "Eroare: Verificarea secventei functioneaza doar pentru automate finite deterministe (AFD)"
        
        # Parse sequence - handle both comma-separated and continuous strings
        if ',' in sequence:
            symbols = [s.strip() for s in sequence.split(',') if s.strip()]
        else:
            symbols = list(sequence)
        
        current_state = self.initial_state
        path = [current_state]
        
        for symbol in symbols:
            if symbol not in self.alphabet:
                return False, f"Simbolul '{symbol}' nu se afla in alfabet"
            
            key = (current_state, symbol)
            if key not in self.transitions or not self.transitions[key]:
                return False, f"Nu exista tranzitie din starea '{current_state}' cu simbolul '{symbol}'"
            
            # For DFA, there's only one next state
            current_state = self.transitions[key][0]
            path.append(current_state)
        
        is_accepted = current_state in self.final_states
        path_str = ' -> '.join(path)
        
        if is_accepted:
            return True, f"ACCEPTAT. Cale: {path_str}"
        else:
            return False, f"RESPINS. Cale: {path_str}. Starea finala '{current_state}' nu este o stare de acceptare"
    
    #determinist
    def find_longest_prefix(self, sequence):
        if not self.is_deterministic():
            return "", "Eroare: Cautarea celui mai lung prefix functioneaza doar pentru automate finite deterministe (AFD)"
        
        # Parse sequence - handle both comma-separated and continuous strings
        if ',' in sequence:
            symbols = [s.strip() for s in sequence.split(',') if s.strip()]
        else:
            symbols = list(sequence)
        
        current_state = self.initial_state
        longest_prefix = ""
        longest_prefix_length = 0
        path = [current_state]
        
        # Check if initial state is final (empty string accepted)
        if current_state in self.final_states:
            longest_prefix = ""
            longest_prefix_length = 0
        
        for i, symbol in enumerate(symbols):
            if symbol not in self.alphabet:
                break
            
            key = (current_state, symbol)
            if key not in self.transitions or not self.transitions[key]:
                break
            
            # For DFA, there's only one next state
            current_state = self.transitions[key][0]
            path.append(current_state)
            
            # Check if current state is a final state
            if current_state in self.final_states:
                if ',' in sequence:
                    longest_prefix = ','.join(symbols[:i+1])
                else:
                    longest_prefix = ''.join(symbols[:i+1])
                longest_prefix_length = i + 1
        
        path_str = ' -> '.join(path[:longest_prefix_length + 1])
        
        if longest_prefix_length == 0 and self.initial_state in self.final_states:
            return "", f"sirul vid este acceptat (starea initiala este finala). Cale: {self.initial_state}"
        elif longest_prefix_length == 0:
            return "", "Niciun prefix nu este acceptat"
        else:
            return longest_prefix, f"Cel mai lung prefix acceptat: '{longest_prefix}' (lungime: {longest_prefix_length}). Cale: {path_str}"


def main_menu():
    """Display and handle the main menu."""
    af = AutomatFinit()
    print("\n" + "="*50)
    print("         PROGRAM AUTOMAT FINIT")

    def print_menu():
        print()
        print("="*50)
        print("1. Incarca AF din fisier")
        print("2. Introduceti AF de la tastatura")
        if af.states and af.alphabet and af.initial_state is not None and af.final_states and af.transitions:
            print("3. Afiseaza starile")
            print("4. Afiseaza alfabetul")
            print("5. Afiseaza tranzitiile")
            print("6. Afiseaza starile finale")
            if af.is_deterministic():
                print("7. Verifica daca o secventa este acceptata ")
                print("8. Gaseste cel mai lung prefix acceptat ")
        print("0. Iesire")
        print("h/help. Meniu Optiuni")
        print("="*50)
        print()

    print_menu()
    while True:
        
        choice = input("Introduceti optiunea: ").strip()
        print()

        if choice == '1':
            filename = input("Introduceti numele fisierului: ").strip()
            af.read_from_file(filename)
            print_menu()
        
        elif choice == '2':
            af.read_from_keyboard()
            print_menu()
        
        elif choice == '3':
            if not af.states:
                print("Niciun AF incarcat. incarcati mai intai un AF.")
            else:
                af.display_states()
        
        elif choice == '4':
            if not af.alphabet:
                print("Niciun AF incarcat. incarcati mai intai un AF.")
            else:
                af.display_alphabet()
        
        elif choice == '5':
            if not af.states:
                print("Niciun AF incarcat. incarcati mai intai un AF.")
            else:
                af.display_transitions()
        

        elif choice == '6':
            if not af.states:
                print("Niciun AF incarcat. incarcati mai intai un AF.")
            else:
                af.display_final_states()

        
        elif choice == '7':
            if af.is_deterministic():
                if not af.states:
                    print("Niciun AF incarcat. incarcati mai intai un AF.")
                else:
                    print("\nIntroduceti secventa de verificat:")
                    print("(Puteti introduce simboluri separate prin virgula sau ca sir continuu)")
                    sequence = input("> ").strip()
                    is_accepted, explanation = af.verify_sequence(sequence)
                    print(f"\n{explanation}")
                    if is_accepted:
                        print("✓ Secventa este ACCEPTATA")
                    else:
                        print("✗ Secventa este RESPINSA")
            else:
                print("Optiune invalida. incercati din nou.")
        
        elif choice == '8':
            if af.is_deterministic():
                if not af.states:
                    print("Niciun AF incarcat. incarcati mai intai un AF.")
                else:
                    print("\nIntroduceti secventa pentru cautarea celui mai lung prefix acceptat:")
                    sequence = input("> ").strip()
                    _, explanation = af.find_longest_prefix(sequence)
                    print(f"\n{explanation}")
            print("Optiune invalida. h/help pentru meniu de optiuni.")
        
        elif choice == '0':
            break

        elif choice in ['h', 'help']:
            print_menu()
        
        else:
            if af.states and af.alphabet and af.initial_state is not None and af.final_states and af.transitions:
                print("Optiune invalida. h/help pentru meniu de optiuni.")
            else :
                print("Niciun AF incarcat. incarcati mai intai un AF.")

if __name__ == "__main__":
    main_menu()