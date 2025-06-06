def auto_review_assignment(assignment):
    """
    Auto-review simplificat:
    - titlul trebuie să conțină minim 5 caractere
    - titlul trebuie să conțină cuvântul "tema"
    """
    issues = []
    if len(assignment.title) < 5:
        issues.append("Titlul este prea scurt.")
    if "tema" not in assignment.title.lower():
        issues.append("Titlul nu conține cuvântul 'tema'.")
    return issues

def auto_fix_suggestions(assignment):
    """
    Sugestii automate pentru titlu:
    - Propune completarea cuvântului 'tema' dacă lipsește
    - Sugerează un titlu mai lung dacă este prea scurt
    """
    suggestions = []
    title = assignment.title.strip()
    if "tema" not in title.lower():
        suggestions.append("Adaugă cuvântul 'tema' în titlu. Exemplu: 'Tema despre ...'")
    if len(title) < 5:
        suggestions.append("Lungește titlul pentru a fi mai descriptiv. Exemplu: 'Tema despre ecologie'.")
    return suggestions