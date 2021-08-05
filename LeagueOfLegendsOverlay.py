import tkinter as tk
from tkinter import ttk
"""
class Example(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.pack()
        btn = ttk.Button(self, text = "Press", command = self.openTopLevel)
        btn.pack()

    def openTopLevel(self):
        topLevelWindow = tk.Toplevel(self)
        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        topLevelWindow.attributes('-topmost', 'true')

root = tk.Tk()
text = tk.Text(root)
text.insert(tk.INSERT, "Hello.....")
text.pack()
root.attributes('-alpha', 0.1)
main = Example(root)
root.mainloop()
"""

root = tk.Tk()
# The image must be stored to Tk or it will be garbage collected.
label = tk.Label(root, bg='white')
root.overrideredirect(True)
root.geometry("+250+250")
root.lift()
root.wm_attributes("-topmost", True)
root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")
label.pack()
label.mainloop()