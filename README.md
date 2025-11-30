# diff.py

A tiny Longest Common Subsequence–based diff tool.

## Features
- Compare **strings** or **files**
- Computes the **LCS** and uses it to align differences
- Output markers:
  - `<<` items only in the first input  
  - `>>` items only in the second  
  - `===` items shared
- Prints the full DP table and LCS pairs for debugging

## Usage
```bash
python diff.py <string1> <string2>
python diff.py <file1> <file2>
