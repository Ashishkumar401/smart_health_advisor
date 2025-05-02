import tkinter as tk
from tkinter import messagebox
import itertools

def solve_puzzle_gui(word1, word2, result, output_box):
    all_letters = ''.join(sorted(set(word1 + word2 + result)))
    if len(all_letters) > 10:
        messagebox.showerror("Error", "Too many unique letters (max 10 allowed).")
        return

    for perm in itertools.permutations(range(10), len(all_letters)):
        letter_map = dict(zip(all_letters, perm))

        if letter_map[word1[0]] == 0 or letter_map[word2[0]] == 0 or letter_map[result[0]] == 0:
            continue

        def to_number(word):
            return int(''.join(str(letter_map[c]) for c in word))

        num1 = to_number(word1)
        num2 = to_number(word2)
        num3 = to_number(result)

        if num1 + num2 == num3:
            output = (
                f"{word1} = {num1}\n"
                f"{word2} = {num2}\n"
                f"{result} = {num3}\n"
                f"Mapping: {letter_map}"
            )
            output_box.delete("1.0", tk.END)
            output_box.insert(tk.END, output)
            return

    messagebox.showinfo("No Solution", "No valid solution found.")

def create_gui():
    root = tk.Tk()
    root.title("Cryptarithmetic Solver")
    root.geometry("400x400")

    tk.Label(root, text="Word 1:").pack()
    entry1 = tk.Entry(root)
    entry1.pack()

    tk.Label(root, text="Word 2:").pack()
    entry2 = tk.Entry(root)
    entry2.pack()

    tk.Label(root, text="Result Word:").pack()
    entry3 = tk.Entry(root)
    entry3.pack()

    output_box = tk.Text(root, height=10, width=40)
    output_box.pack(pady=10)

    def on_solve():
        word1 = entry1.get().strip().upper()
        word2 = entry2.get().strip().upper()
        result = entry3.get().strip().upper()
        solve_puzzle_gui(word1, word2, result, output_box)

    tk.Button(root, text="Solve Puzzle", command=on_solve).pack(pady=5)

    root.mainloop()

create_gui()
