# ------------------------------------------------------------------ MODULES ------------------------------------------------------------------ #
from tkinter import *
from tkinter import ttk
import pandas as pd
import os

import Common_Commands as cc
import Login_Page as lp
import Journals
import Ledger
import Trial_Balance
#import AI

def startup():
    logo_window()
    login_signup_window()



# -------------------------------------------------------- SPLASH SCREEN -------------------------------------------------------- #
def logo_window():
    splash = Tk()
    splash.overrideredirect(True)              # Removing the borders/closing tab, etc

    screen_width = splash.winfo_screenwidth()                  # This para is to make app appear in middle of screen
    screen_height = splash.winfo_screenheight()
    window_width = 512
    window_height = 512
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)
    splash.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

    logo_image = PhotoImage(file="Miscellaneous\\Big Logo.png")           # Getting the image from file
    label = Label(splash, image=logo_image)                             # Adding image to the app
    label.pack(side="bottom", fill="both")

    def close_logo_screen():
        splash.destroy()

    splash.after(2000,close_logo_screen)

    splash.mainloop()

# -------------------------------------------------------- SIGN IN WINDOW -------------------------------------------------------- #

def login_signup_window():
    login = Tk()
    login.title("Login / Sign Up")
    
    screen_width = login.winfo_screenwidth()                       # Making app display in front of screen
    screen_height = login.winfo_screenheight()
    window_width = 600
    window_height = 500
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    login.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

    def show_form(page):        # To Change to each tab/window
        for f in pages:
            f.pack_forget()
        page.pack()

    def sign_in():
        usr = username_entry.get().strip()
        pas = password_entry.get().strip()
        a = lp.sign_in(usr,pas)
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        if a == "Logged In":
            login.destroy()
            mainapp()
            

    def sign_up():
        usr = nusername_entry.get().strip()
        pas = npassword_entry.get().strip()
        lp.sign_up(usr,pas)
        
        nusername_entry.delete(0, END)
        npassword_entry.delete(0, END)



    login_page = Frame(login)
    sign_up_page = Frame(login)
    pages = [login_page,sign_up_page]

    # -------------------- login_page -------------------- #

    username = ttk.Label(login_page, text="Username:")
    username.grid(row=0, column=1, sticky="w")
    username_entry = Entry(login_page)
    username_entry.grid(row=0, column=3, padx=5, pady=5)

    password = ttk.Label(login_page, text="Password:")
    password.grid(row=1, column=1, sticky="w")
    password_entry = Entry(login_page,show="*")
    password_entry.grid(row=1, column=3, padx=5, pady=5)

    submit_btn = ttk.Button(login_page, text="Submit", command = sign_in)
    submit_btn.grid(row=4, column=0, columnspan=2)

    sign_up_btn = ttk.Button(login_page, text="Sign Up", command=lambda: show_form(sign_up_page))
    sign_up_btn.grid(row=5, column=0, columnspan=2)

    # -------------------- sign_up_page -------------------- #

    nusername = ttk.Label(sign_up_page, text="Enter Username:")
    nusername.grid(row=0, column=1, sticky="w")
    nusername_entry = Entry(sign_up_page)
    nusername_entry.grid(row=0, column=3, padx=5, pady=5)

    npassword = ttk.Label(sign_up_page, text="Enter Password:")
    npassword.grid(row=1, column=1, sticky="w")
    npassword_entry = Entry(sign_up_page)
    npassword_entry.grid(row=1, column=3, padx=5, pady=5)

    nsubmit_btn = ttk.Button(sign_up_page, text="Create New Account",command = sign_up)
    nsubmit_btn.grid(row=4, column=0, columnspan=2)

    login_btn = ttk.Button(sign_up_page, text="Login", command=lambda: show_form(login_page))
    login_btn.grid(row=4, column=0, columnspan=2)

    show_form(login_page)
    login.mainloop()

# -------------------------------------------------------- MAIN APP -------------------------------------------------------- #

def mainapp():
    mapp = Tk()
    mapp.title("Ledger Logic")
    
    screen_width = mapp.winfo_screenwidth()                       # Making app display in front of screen
    screen_height = mapp.winfo_screenheight()
    window_width = 800
    window_height = 600
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    mapp.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")


    # ----------------------------------- Pre Defined Stuff ----------------------------------- #

    def signout():
        mapp.quit()
        mapp.destroy()
        login_signup_window()
    
    def show_form(form):        # To Change to each tab/window
        for f in forms:
            f.pack_forget()
        form.pack()

    def get_journal():                                  # Get Journal Entries
        debit = debit_entry.get().strip()
        credit = credit_entry.get().strip()
        amount = amt_entry.get().strip()
        narration = narration_entry.get().strip()
    
        Journals.save_journal(debit,credit,amount,narration)
        display_journals()
        debit_entry.delete(0, END)
        credit_entry.delete(0, END)
        amt_entry.delete(0, END)
        narration_entry.delete(0, END)

    def display_journals():
        try:
            data = pd.read_csv(f"Users\\{cc.usr}\\Processing Files\\journal_entries.csv", header=None)
            data.columns = ['Date', 'Debit', 'Credit', 'Amount', 'Narration']
            data.insert(0, 'Index', range(1, len(data) + 1))

            tree.delete(*tree.get_children())
            for index, row in data.iterrows():
                tree.insert("", END, values=row.tolist())
        except:
            pass
    
    def gentb():
        Trial_Balance.create_trial_balance()
        updatetb()

    def updatetb():
        try:
            data = pd.read_excel(f"Users\\{cc.usr}\\Processing Files\\Trial Balance.xlsx", header=0,na_filter=False)
            data = pd.DataFrame(data)
            data.fillna(" ")    

            for i, row in data.iterrows():
                tree.insert('', 'end', values = row.tolist())
        except:
            pass
    
    #def ai(que):
     #   res = AI.enquire(que)

      #  chat_his.config(state='normal')
       # chat_his.insert(END, f"You: {que}\nGemini: {res}\n")       # Adding chat to end
        #chat_his.see(END)
        #chat_his.config(state='disabled')
        
        #queentry.delete(0,END)
            






    # ----------------------------------- UI ----------------------------------- #
    appbar = Frame(mapp, bg="#333")
    appbar.pack(side="left", fill="y")

    home_form = Frame(mapp)
    journal_form = Frame(mapp)
    ledger_form = Frame(mapp)
    tb_form = Frame(mapp)
    fs_form = Frame(mapp)
    gemini_form = Frame(mapp)
    stt_form = Frame(mapp)
    forms = [home_form, journal_form, ledger_form, tb_form,fs_form, gemini_form, stt_form]

    hm = Button(appbar, text="Home", bg="#555", fg="white", padx=10, command=lambda: show_form(home_form))
    hm.pack(pady=10)

    jb = Button(appbar, text="Journal", bg="#555", fg="white", padx=10, command=lambda: show_form(journal_form))
    jb.pack(pady=10)

    lb = Button(appbar, text="Ledger", bg="#555", fg="white", padx=10, command=lambda: show_form(ledger_form))
    lb.pack(pady=10)

    tbb = Button(appbar, text="Trial\nBalance", bg="#555", fg="white", padx=10, command=lambda: show_form(tb_form))
    tbb.pack(pady=10)

    fsb = Button(appbar, text="Financial\nStatement", bg="#555", fg="white", padx=10, command=lambda: show_form(fs_form))
    fsb.pack(pady=10)
            
    gmb = Button(appbar, text="Gemini\nChatbot", bg="#555", fg="white", padx=10, command=lambda: show_form(gemini_form))
    gmb.pack(pady=10)

    stt = Button(appbar, text="Settings", bg="#555", fg="white", padx=10, command=lambda: show_form(stt_form))
    stt.pack(pady=10)

    logout = Button(appbar, text="Log Out", bg="#555", fg="white", padx=10,command = signout)
    logout.pack(pady=10)
    

    # ----------------------------------- Journals ----------------------------------- #

    debit = ttk.Label(journal_form, text="Debit Account:")
    debit.grid(row=0, column=0, sticky="w")
    debit_entry = Entry(journal_form)
    debit_entry.grid(row=0, column=1, padx=5, pady=5)

    credit = ttk.Label(journal_form, text="Credit Account:")
    credit.grid(row=1, column=0, sticky="w")
    credit_entry = Entry(journal_form)
    credit_entry.grid(row=1, column=1, padx=5, pady=5)

    amt = ttk.Label(journal_form, text="Amount:")
    amt.grid(row=2, column=0, sticky="w")
    amt_entry = Entry(journal_form)
    amt_entry.grid(row=2, column=1, padx=5, pady=5)

    narration = ttk.Label(journal_form, text="Narration:")
    narration.grid(row=3, column=0, sticky="w")
    narration_entry = Entry(journal_form)
    narration_entry.grid(row=3, column=1, padx=5, pady=5)

    submit_btn = ttk.Button(journal_form, text="Submit", command = get_journal)
    submit_btn.grid(row=4, column=0, columnspan=2)

    tree = ttk.Treeview(journal_form, columns=("Index","Date","Debit Account", "Credit Account", "Amount", "Narration"),show="headings")

    tree.heading("Index", text="Index")
    tree.heading("Date", text="Date")
    tree.heading("Debit Account", text="Debit Account")
    tree.heading("Credit Account", text="Credit Account")
    tree.heading("Amount", text="Amount")
    tree.heading("Narration", text="Narration")

    tree.column('Index', width=50)
    tree.column('Date', width=100)
    tree.column('Debit Account', width=150)
    tree.column('Credit Account', width=150)
    tree.column('Amount', width=100)
    tree.column('Narration', width=200)

    tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky = EW)
    display_journals()

    # ----------------------------------- Ledgers ----------------------------------- #

    create_ledger_btn = ttk.Button(ledger_form, text="Create Ledger",command = Ledger.create_ledger_xlsx)
    create_ledger_btn.grid(row=0, column=0)

    # ----------------------------------- Trial Balance ----------------------------------- #

    create_display_trial_balance_btn = ttk.Button(tb_form, text="Generate Trial Balance", command = gentb)
    create_display_trial_balance_btn.grid(row=0, column=0)

    tree = ttk.Treeview(tb_form, columns=("Particulars", 'Debit', 'Credit'), show = 'headings')

    tree.heading('Particulars', text = 'Particulars')
    tree.heading('Debit', text = 'Debit')
    tree.heading('Credit', text = 'Credit')

    tree.column('Particulars', width = 150)
    tree.column('Debit', width = 50)
    tree.column('Credit', width = 50)
    tree.grid(padx=10,pady=10)
    
    # ----------------------------------- Gemini Chatbot ----------------------------------- #
    que = ttk.Label(gemini_form, text="Enter Queries")
    que.grid(row=0, column=0, sticky="w")
    queentry = Entry(gemini_form)
    queentry.grid(row=0, column=1, padx=5, pady=10)

    chat_his = Text(gemini_form, height=30, width=80)
    chat_his.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    #submit_bttn = ttk.Button(gemini_form, text="Submit", command=lambda: ai(queentry.get().strip()))
    #submit_bttn.grid(row=1, column=0, columnspan=2)


    mapp.mainloop()
    os.remove("Users\\Current Signed In Account.txt")


startup()