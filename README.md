# Case Study-Based Analysis and Design using PDA and CFG

**Author:** S G S V GANESH  
**University:** SRM Institute of Science and Technology  

This repository presents formal Context-Free Grammar (CFG) and Pushdown Automaton (PDA) models for three complex structural validation case studies: **Multi-Delimiter Balanced Parentheses**, **Unambiguous Arithmetic Expressions (Precedence Resolution)**, and **Programming-Language Conditional Syntax (Dangling-Else Resolution)**. It includes an interactive web front-end for browser-based simulation and automated unit tests.

---

## 1. Case Studies Covered
1. **Multi-Delimiter Balanced Parentheses ($D_3$):** Validates nested pairs `()`, `[]`, and `{}` using a DPDA stack machine.
2. **Arithmetic Expressions:** Eliminates structural ambiguity via stratified non-terminals ($E, T, F$) enforcing standard operator precedence ($*$ over $+$).
3. **Conditional Syntax (Dangling-Else):** Resolves ambiguous nesting by partitioning statements into Matched ($M$) and Unmatched ($U$) categories.

---

## 2. Project Structure
* `pda_cfg_validator.py` - Core Python simulation engine and trace demonstrator.
* `test_pda.py` - Automated `unittest` test suite.
* `index.html` - Interactive front-end web simulator for browser-based testing and stack inspection.

---

## 3. How to Run Locally

### Running the Python Engine & Tests
```bash
# Run the core validation demonstration script
python pda_cfg_validator.py

# Run the automated unit tests
python test_pda.py
