import time
import os
import tracemalloc

recursive_calls = 0


def dpll(clauses, assignment=[]):
    global recursive_calls
    recursive_calls += 1

    clauses = [clause for clause in clauses if not any(lit in assignment for lit in clause)]
    simplified = []

    for clause in clauses:
        simplified_clause = [lit for lit in clause if -lit not in assignment]
        simplified.append(simplified_clause)

    if not simplified:
        return True, assignment
    if any(len(clause) == 0 for clause in simplified):
        return False, []

    for clause in simplified:
        if len(clause) == 1:
            lit = clause[0]
            return dpll(simplified, assignment + [lit])

    lit = simplified[0][0] 
    sat, result = dpll(simplified, assignment + [lit])
    if sat:
        return True, result
    return dpll(simplified, assignment + [-lit])


def citeste_clauze():
    print("Introdu clauzele (literali separați prin spațiu, ENTER după fiecare clauză).")
    print("Apasă ENTER de două ori pentru a termina.\n")

    clauses = []
    while True:
        linie = input()
        if linie.strip() == "":
            break
        try:
            clauza = list(map(int, linie.strip().split()))
            if clauza:
                clauses.append(clauza)
        except ValueError:
            print("Eroare: introdu doar numere întregi separate prin spațiu.")
    return clauses


def main():
    global recursive_calls
    recursive_calls = 0
    clauses = citeste_clauze()
    tracemalloc.start()
    start_time = time.time()
    satisfiable, assignment = dpll(clauses)
    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    exec_time = end_time - start_time
    peak_kb = peak_mem / 1024 
    nr_clauze = len(clauses)
    nr_literali = [len(clauza) for clauza in clauses]
    stare = "DA" if satisfiable else "NU"
    with open("output.cnf", "a") as f:
        if os.path.getsize("output.cnf") == 0:
            f.write("Timp_Executie(sec) | Nr_Clauze | Literali_pe_Clauza | Memorie_max(KB) | Satisfiabila\n")
        f.write(
            "{:<18.6f} | {:<10} | {:<20} | {:<16.2f} | {}\n".format(
                exec_time, nr_clauze, ",".join(map(str, nr_literali)), peak_kb, stare
            ))
    with open("recursivitate.log", "a") as rfile:
        rfile.write(f"{recursive_calls} apeluri recursive pentru {nr_clauze} clauze\n")

    if satisfiable:
        print("\nFormula este SATISFIABILĂ.")
        print("Atribuire validă:", assignment)
    else:
        print("\nFormula este NESATISFIABILĂ.")

    print(f"Timp de execuție: {exec_time:.6f} secunde")
    print(f"Memorie maximă utilizată: {peak_kb:.2f} KB")
    print(f"Număr apeluri recursive DPLL: {recursive_calls} (salvat în 'recursivitate.log')")


if __name__ == "__main__":
    main()
