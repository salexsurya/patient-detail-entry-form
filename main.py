from tkinter import END, Button, Entry, Frame, Label, Tk, messagebox, ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
import pandas as pd

#from auto_complete import AutoCompleteEntry


class DataForm(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.load_data()
        self.create_widgets()
        self.columns = ['date', 'phone', 'name', 'age', 'gender', 'town', 'district',
                        'consultation_fee', 'scan_fee', 'medicine_fee']
        

    def create_widgets(self):
        # Create form labels and entries
        self.date_label = Label(self.master, text='* Date')
        self.date_label.grid(row=0, column=0)
        self.date_entry = AutocompleteCombobox(self.master, completevalues=list(self.df['date'].dropna().unique()))
        self.date_entry.grid(row=0, column=1, padx=2, pady=8)
        self.date_entry.focus()
        # self.date_entry.bind('<FocusOut>', self.gen_focus_out)

        self.phone_label = Label(self.master, text='* Phone')
        self.phone_label.grid(row=1, column=0)
        self.phone_entry = AutocompleteCombobox(self.master, completevalues=list(self.df['phone'].dropna().unique()))
        # self.phone_entry = AutoCompleteEntry(self.master, self.df, 'phone') # Entry(self.master)
        self.phone_entry.grid(row=1, column=1, padx=2, pady=8)        
        self.phone_entry.bind('<FocusOut>', self.on_phone_focusout)

        self.name_label = Label(self.master, text='* Name')
        self.name_label.grid(row=2, column=0)
        self.name_entry = AutocompleteCombobox(self.master, completevalues=list(self.df['name'].dropna().unique()))
        # self.name_entry = AutoCompleteEntry(self.master, self.df, 'name')
        self.name_entry.grid(row=2, column=1, padx=2, pady=8)
        # self.name_entry.bind('<FocusOut>', self.gen_focus_out)

        self.age_label = Label(self.master, text='Age')
        self.age_label.grid(row=3, column=0)
        self.age_entry = Entry(self.master)
        self.age_entry.grid(row=3, column=1, padx=2, pady=8)

        self.genger_label = Label(self.master, text='* Gender')
        self.genger_label.grid(row=4, column=0)
        self.gender_options = ["Female", "Male", "Other"]
        self.gender_dropdown = ttk.Combobox(master=self.master, values=self.gender_options, width=18)
        self.gender_dropdown.current(0)
        self.gender_dropdown.grid(row=4, column=1, padx=2, pady=8)

        self.town_label = Label(self.master, text='* Town')
        self.town_label.grid(row=5, column=0)
        # self.town_entry = AutoCompleteEntry(self.master, self.df, 'town') #Entry(self.master)
        self.town_entry = AutocompleteCombobox(self.master, completevalues=list(self.df['town'].dropna().unique()))
        self.town_entry.grid(row=5, column=1, padx=2, pady=8)
        self.town_entry.bind('<FocusOut>', self.on_town_focusout)
        # # self.town_entry.bind("<KeyRelease>", self.autocomplete_town)

        self.district_label = Label(self.master, text='District')
        self.district_label.grid(row=6, column=0)
        # self.district_entry = AutoCompleteEntry(self.master, self.df, 'district') # Entry(self.master)
        self.district_entry = AutocompleteCombobox(self.master, completevalues=list(self.df['district'].dropna().unique()))
        self.district_entry.grid(row=6, column=1, padx=2, pady=8)
        # self.district_entry.bind('<FocusOut>', self.gen_focus_out)

        self.consultation_fee_label = Label(self.master, text='Consultation Fee')
        self.consultation_fee_label.grid(row=7, column=0)
        self.consultation_fee_entry = Entry(self.master)
        self.consultation_fee_entry.grid(row=7, column=1, padx=2, pady=8)
        self.consultation_fee_entry.insert(0, 150)

        self.scan_fee_label = Label(self.master, text='Scan Fee')
        self.scan_fee_label.grid(row=8, column=0)
        self.scan_fee_entry = Entry(self.master)
        self.scan_fee_entry.grid(row=8, column=1, padx=2, pady=8)

        self.medicine_fee_label = Label(self.master, text='Medicine Fee')
        self.medicine_fee_label.grid(row=9, column=0)
        self.medicine_fee_entry = Entry(self.master)
        self.medicine_fee_entry.grid(row=9, column=1, padx=2, pady=8)

        # Create save button
        self.save_button = Button(self.master, text='Save', command=self.save_data)
        self.save_button.grid(row=10, column=1)

        self.message_label = Label(self.master, text='')
        self.message_label.grid(row=11, column=0)
        
    # def autocomplete_town():
    #     pass
    def gen_focus_out(self, event):
        return

    def load_data(self):
        try:
            self.df = pd.read_csv('data.csv').astype({'phone': str})
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=self.columns)

    def on_phone_focusout(self, event):
        # validate inputs
        phone = str(self.phone_entry.get())          
        if len(phone) != 10:
            # messagebox.showwarning("Data Validation", "Phone number not 10 digits")
            # self.phone_entry.focus()
            return
        
        # Fill other fields
        row = self.df.loc[self.df['phone'] == str(phone)].replace('NaN', '')
        if not row.empty:
            self.name_entry.delete(0, END)
            self.name_entry.insert(0, row['name'].iloc[-1])

            self.age_entry.delete(0, END)
            self.age_entry.insert(0, row['age'].iloc[-1])

            self.gender_dropdown.delete(0, END)
            self.gender_dropdown.insert(0, row['gender'].iloc[-1])

            self.town_entry.delete(0, END)
            self.town_entry.insert(0, row['town'].iloc[-1])

            self.district_entry.delete(0, END)
            self.district_entry.insert(0, row['district'].iloc[-1])

            self.consultation_fee_entry.delete(0, END)
            self.consultation_fee_entry.insert(0, row['consultation_fee'].iloc[-1])

            self.scan_fee_entry.delete(0, END)
            self.scan_fee_entry.insert(0, row['scan_fee'].iloc[-1])

            self.medicine_fee_entry.delete(0, END)
            self.medicine_fee_entry.insert(0, row['medicine_fee'].iloc[-1])

    def on_town_focusout(self, event):
        # validate inputs
        town = str(self.town_entry.get())          
        if len(town) == 0:
            return
        
        # Fill other fields
        row = self.df.loc[self.df['town'] == town]
        if not row.empty:
            self.district_entry.delete(0, END)
            self.district_entry.insert(0, row['district'].iloc[-1])
            # self.district_entry.close()

    def save_data(self):
        # get data
        date = self.date_entry.get()
        phone = self.phone_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_dropdown.get()
        town = self.town_entry.get()
        district = self.district_entry.get()
        consultation_fee = self.consultation_fee_entry.get()
        scan_fee = self.scan_fee_entry.get()
        medicine_fee = self.medicine_fee_entry.get()

        # validate inputs
        if len(phone) != 10:
            messagebox.showwarning("Data Validatation", "Phone number not 10 digits")
            self.phone_entry.focus()
            return
    
        # validate inputs
        if date == '' or phone == '' or name == '' or age == '' or gender == '' or town == '':
            messagebox.showwarning("Data Validatation", "Check Date, Phone, Name, Age, Gender and Town")
            return
        
        # Append to df
        row = {'date': date, 'phone': phone, 'name': name, 'age': age, 'gender': gender,
               'town': town, 'district': district, 'consultation_fee': consultation_fee,
               'scan_fee': scan_fee, 'medicine_fee': medicine_fee}        
        self.df = self.df.append(row, ignore_index=True)

        # Save the dataframe to CSV file
        self.df.to_csv('data.csv', index=False)

        # Clear fields
        self.phone_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.gender_dropdown.current(0)
        self.town_entry.delete(0, END)
        self.district_entry.delete(0, END)
        # self.consultation_fee_entry.delete(0, END)
        self.scan_fee_entry.delete(0, END)
        self.medicine_fee_entry.delete(0, END)
        self.phone_entry.focus()

        # update dropdown
        self.phone_entry.set_completion_list(list(self.df['phone'].dropna().unique()))
        self.name_entry.set_completion_list(list(self.df['name'].dropna().unique()))
        self.town_entry.set_completion_list(list(self.df['town'].dropna().unique()))
        self.district_entry.set_completion_list(list(self.df['district'].dropna().unique()))


if __name__ == '__main__':
    root = Tk()
    root.title("Welcome to TutorialsPoint")
    root.geometry('350x400')
    #root.configure(background = "gray")
    app = DataForm(master=root)
    app.mainloop()
