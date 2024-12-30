# srt_editor.py

from tkinter import Tk, Text, Button
from tkinter.messagebox import showinfo

# Open SRT for editing in a Tkinter text editor
def edit_srt(srt_file):
    def save_and_close():
        with open(srt_file, "w") as f:
            f.write(text_editor.get("1.0", "end-1c"))
        root.destroy()

    root = Tk()
    root.title("Edit Subtitles")
    text_editor = Text(root, wrap="word", width=80, height=30)
    with open(srt_file, "r") as f:
        text_editor.insert("1.0", f.read())
    text_editor.pack(padx=10, pady=10)
    Button(root, text="Save and Close", command=save_and_close).pack(pady=10)
    root.mainloop()
