#!/usr/bin/env python3
"""
Task: Case Study-Based Analysis and Design using PDA and CFG
Case Studies:
  1. Multi-Delimiter Balanced Parentheses (DPDA Stack Machine)
  2. Unambiguous Arithmetic Expression Validator (CFG Recursive/Stack Parser)
  3. Programming-Language Conditional Syntax (If-Then-Else PDA Validator)
"""

# =====================================================================
# CASE STUDY 1: Multi-Delimiter Balanced Parentheses PDA
# =====================================================================
def validate_parentheses_pda(s: str):
    stack = ["Z0"]
    trace = [f"(q0, {s or 'ε'}, Z0)"]
    pairs = {")": "(", "]": "[", "}": "{"}

    for i, ch in enumerate(s):
        rem = s[i + 1:] or "ε"
        if ch in "([{":
            stack.append(ch)
            trace.append(f"(q0, {rem}, {''.join(reversed(stack))})")
        elif ch in ")]}":
            if stack[-1] == pairs[ch]:
                stack.pop()
                trace.append(f"(q0, {rem}, {''.join(reversed(stack))})")
            else:
                trace.append(f"CRASH(expected match for {ch}, top={stack[-1]})")
                return False, " -> ".join(trace)
        else:
            trace.append(f"CRASH(invalid symbol {ch})")
            return False, " -> ".join(trace)

    if stack == ["Z0"]:
        trace.append("(qf, ε, Z0)")
        return True, " -> ".join(trace)
    trace.append(f"REJECT(unclosed stack={''.join(reversed(stack))})")
    return False, " -> ".join(trace)


# =====================================================================
# CASE STUDY 2: Unambiguous Arithmetic Expression CFG/PDA (G2)
# =====================================================================
def tokenize_expr(expr: str):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i:i+2] == "id":
            tokens.append("id")
            i += 2
        elif expr[i] in "+*()":
            tokens.append(expr[i])
            i += 1
        else:
            return None
    return tokens


def validate_arithmetic_pda(expr: str):
    tokens = tokenize_expr(expr)
    if not tokens:
        return False, "Lexical error or empty input"

    stack = ["Z0", "E"]
    idx = 0
    steps = [f"Stack:[E Z0] Input:{' '.join(tokens)}"]

    while stack[-1] != "Z0":
        top = stack[-1]
        tok = tokens[idx] if idx < len(tokens) else "$"

        if top in ("id", "+", "*", "(", ")"):
            if top == tok:
                stack.pop()
                idx += 1
                steps.append(f"Match '{tok}' -> Stack:[{' '.join(reversed(stack))}]")
            else:
                steps.append(f"Mismatch: expected '{top}', got '{tok}'")
                return False, " | ".join(steps)
        elif top == "E":
            if tok in ("id", "("):
                stack.pop()
                stack.extend(["E'", "T"])
                steps.append("Expand E -> T E'")
            else:
                steps.append(f"Syntax error at '{tok}' in state E")
                return False, " | ".join(steps)
        elif top == "E'":
            if tok == "+":
                stack.pop()
                stack.extend(["E'", "T", "+"])
                steps.append("Expand E' -> + T E'")
            elif tok in (")", "$"):
                stack.pop()
                steps.append("Expand E' -> ε")
            else:
                steps.append(f"Syntax error at '{tok}' in state E'")
                return False, " | ".join(steps)
        elif top == "T":
            if tok in ("id", "("):
                stack.pop()
                stack.extend(["T'", "F"])
                steps.append("Expand T -> F T'")
            else:
                steps.append(f"Syntax error at '{tok}' in state T")
                return False, " | ".join(steps)
        elif top == "T'":
            if tok == "*":
                stack.pop()
                stack.extend(["T'", "F", "*"])
                steps.append("Expand T' -> * F T'")
            elif tok in ("+", ")", "$"):
                stack.pop()
                steps.append("Expand T' -> ε")
            else:
                steps.append(f"Syntax error at '{tok}' in state T'")
                return False, " | ".join(steps)
        elif top == "F":
            if tok == "id":
                stack.pop()
                stack.append("id")
                steps.append("Expand F -> id")
            elif tok == "(":
                stack.pop()
                stack.extend([")", "E", "("])
                steps.append("Expand F -> ( E )")
            else:
                steps.append(f"Syntax error at '{tok}' in state F")
                return False, " | ".join(steps)

    if idx == len(tokens):
        steps.append("ACCEPT (Stack=Z0, Input=$)")
        return True, " | ".join(steps)
    steps.append(f"REJECT (Unconsumed tokens: {tokens[idx:]})")
    return False, " | ".join(steps)


# =====================================================================
# CASE STUDY 3: Programming-Language Conditional Syntax PDA (G3)
# =====================================================================
def validate_conditional_pda(code: str):
    tokens = code.split()
    if not tokens:
        return False, "Empty input"

    stack = ["Z0", "S"]
    idx = 0
    trace = [f"Init Stack:[S Z0]"]

    while stack[-1] != "Z0":
        top = stack.pop()
        tok = tokens[idx] if idx < len(tokens) else "$"

        if top in ("if", "c", "then", "else", "a"):
            if top == tok:
                idx += 1
                trace.append(f"Consumed '{tok}'")
            else:
                trace.append(f"CRASH: Expected '{top}', got '{tok}'")
                return False, " -> ".join(trace)
        elif top == "S":
            if tok == "if":
                stack.extend(["ELSE_OPT", "S", "then", "c", "if"])
                trace.append("Expand S -> if c then S [else S]")
            elif tok == "a":
                stack.append("a")
                trace.append("Expand S -> a")
            else:
                trace.append(f"CRASH: Invalid statement start '{tok}'")
                return False, " -> ".join(trace)
        elif top == "ELSE_OPT":
            if tok == "else":
                stack.extend(["S", "else"])
                trace.append("Match closest 'else' -> else S")
            else:
                trace.append("ELSE_OPT -> ε (Unmatched if closed)")

    if idx == len(tokens):
        trace.append("ACCEPT (Stack=Z0)")
        return True, " -> ".join(trace)
    trace.append(f"REJECT (Orphaned tokens: {tokens[idx:]})")
    return False, " -> ".join(trace)


if __name__ == "__main__":
    print("=" * 95)
    print(" PDA & CFG CASE STUDY VALIDATION DEMONSTRATION")
    print("=" * 95)

    suites = [
        ("1. Balanced Parentheses PDA", validate_parentheses_pda, [
            ("{[()()]}", True),
            ("([)]", False),
            ("((()", False),
        ]),
        ("2. Unambiguous Arithmetic Expression PDA", validate_arithmetic_pda, [
            ("id + id * id", True),
            ("id * (id + id)", True),
            ("id + * id", False),
            ("(id + id", False),
        ]),
        ("3. Conditional Syntax (If-Then-Else) PDA", validate_conditional_pda, [
            ("if c then if c then a else a", True),
            ("if c then a else a", True),
            ("if c then a else a else a", False),
            ("if c else a", False),
        ]),
    ]

    for title, fn, cases in suites:
        print(f"\n[{title}]")
        print("-" * 95)
        for sample, expected in cases:
            ok, log = fn(sample)
            status = "ACCEPT" if ok else "REJECT"
            check = "PASS" if ok == expected else "FAIL"
            print(f"Input: {sample:<30} | {status:<6} | {check:<4} | {log}")