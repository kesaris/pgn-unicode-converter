import tkinter as tk
import os
import sys

# Mapping for white and black chess symbols
white_symbols = {'K':'♚','Q':'♛','R':'♜','B':'♝','N':'♞','P':'♟'}
black_symbols = {'K':'♔','Q':'♕','R':'♖','B':'♗','N':'♘','P':'♙'}

# Mapping for converting files a-h to Greek letters
file_to_greek = {'a':'α','b':'β','c':'γ','d':'δ','e':'ε','f':'ζ','g':'η','h':'θ'}

def convert_pgn(text: str, to_greek=False) -> str:
    """
    Converts a PGN string to Unicode symbols.
    Optionally replaces file letters with Greek letters.
    """
    lines = text.split('\n')
    out = []
    for line in lines:
        if not line or line.startswith('['):
            continue  # Skip empty lines or PGN tags
        parts = line.split()
        black = False  # Flag to alternate between white and black moves
        new = []
        for tok in parts:
            if tok.endswith('...'):
                new.append(tok)
                black = True
                continue
            if tok.endswith('.'):
                new.append(tok)
                black = False
                continue
            first = tok[0]
            if first in white_symbols:
                # Use the correct symbol based on color
                sym = black_symbols[first] if black else white_symbols[first]
                rest = tok[1:]
                if to_greek:
                    for lt, gr in file_to_greek.items():
                        rest = rest.replace(lt, gr)
                new.append(sym + rest)
            else:
                s = tok
                if to_greek:
                    for lt, gr in file_to_greek.items():
                        s = s.replace(lt, gr)
                new.append(s)
            black = not black  # Alternate color
        out.append(' '.join(new))
    return ' '.join(out)

def format_nested_variations(text: str) -> str:
    """
    Formats parentheses by indenting each nested variation.
    """
    result, indent = '', 0
    for ch in text:
        if ch == '(':
            result += '\n' + '  '*indent + '('
            indent += 1
        elif ch == ')':
            result += ')'
            indent = max(0, indent - 1)
            result += '\n' + '  '*indent
        else:
            result += ch
    return result.strip()

# Clipboard and conversion actions
def on_clear():
    text_input.delete("1.0", tk.END)
    text_output.delete("1.0", tk.END)

def on_convert_en():
    raw = text_input.get("1.0", tk.END)
    conv = convert_pgn(raw, False)
    formatted = format_nested_variations(conv)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, formatted)

def on_convert_gr():
    raw = text_input.get("1.0", tk.END)
    conv = convert_pgn(raw, True)
    formatted = format_nested_variations(conv)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, formatted)

def on_copy():
    root.clipboard_clear()
    root.clipboard_append(text_output.get("1.0", tk.END))

def resource_path(relative_path):
    """
    Returns correct path to resource file, compatible with PyInstaller
    """
    try:
        # When using PyInstaller, _MEIPASS is the temp folder
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# GUI setup
root = tk.Tk()
root.title("PGN Converter")
root.configure(bg='#222222')  # Dark background

# Set application icon (requires image file)
icon_path = resource_path("knight.png")
if os.path.exists(icon_path):
    root.iconphoto(True, tk.PhotoImage(file=icon_path))

# Frame for top buttons
frm = tk.Frame(root, bg='#222222')
frm.pack(fill=tk.X, pady=5, padx=5)

# Create control buttons
tk.Button(frm, text="Clear",      command=on_clear,      bg='#555555', fg='white').pack(side=tk.LEFT, padx=3)
tk.Button(frm, text="Convert EN", command=on_convert_en, bg='#555555', fg='white').pack(side=tk.LEFT, padx=3)
tk.Button(frm, text="Convert GR", command=on_convert_gr, bg='#555555', fg='white').pack(side=tk.LEFT, padx=3)
tk.Button(frm, text="Copy",       command=on_copy,       bg='#555555', fg='white').pack(side=tk.LEFT, padx=3)

# Input text box
text_input = tk.Text(root, height=10, bg='#333333', fg='white', insertbackground='white',
                     font=("Segoe UI Symbol", 14))
text_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Output text box
text_output = tk.Text(root, height=10, bg='#333333', fg='white', insertbackground='white',
                      font=("Segoe UI Symbol", 14))
text_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Start GUI loop
root.mainloop()
