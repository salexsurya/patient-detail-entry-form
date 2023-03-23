import tkinter as tk
import tkinter.ttk as ttk

import pandas as pd


class AutoCompleteEntry(ttk.Entry):
    def __init__(self, master, df: pd.DataFrame, field: str):
        super().__init__(master)
        self.df = df
        self.field = field
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<FocusOut>", self.close)
        
        self.lb_show = False
        # self.pack()
        
        # self.bind("<Button-1>", self.close)

    def close(self, event=None):
        if self.lb_show:
            try:
                if not (self.focus_get is None and self.lb.focus_get is None):
                    self.lb.destroy()
                    self.lb_show = False
            except:
                pass

    def changed(self, name, index, mode):
        if self.var.get() == '':
            try:
                self.lb.destroy()
            except:
                pass
            self.lb_show = False
        else:
            suggestions = self.suggestions()
            if suggestions:
                if not self.lb_show:
                    self.lb = tk.Listbox(width=30)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.bind("<Tab>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_show = True
                self.lb.delete(0, tk.END)
                for w in suggestions:
                    self.lb.insert(tk.END,w)
            else:
                if self.lb_show:
                    self.lb.destroy()
                    self.lb_show = False

    def selection(self, event):
        if self.lb_show:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_show = False
            self.icursor(tk.END)
            self.focus_set()

    def up(self, event):
        if self.lb_show:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        if self.lb_show:
            if self.lb.curselection() == ():
                index = '-1'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def suggestions(self):
        pattern = '^' + self.var.get()
        field = self.df[self.field].dropna()
        match = field.str.contains(pattern, regex=True, case=False)
        return sorted(list(field[match].unique()))


if __name__ == '__main__':
    # Create a tkinter window
    root = tk.Tk()
    root.geometry("300x200")

    # Create an AutoCompleteEntry widget and pack it into the window
    name_entry = AutoCompleteEntry(root)
    # name_entry.pack()

    root.mainloop()
