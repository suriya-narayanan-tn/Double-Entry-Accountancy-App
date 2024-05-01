from tkinter import *
import ctypes


def icon(root):
    logo = PhotoImage(file="Miscellaneous\\Small Logo.png")
    root.iconphoto(False, logo)
    
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

usr = ""
def get_user_account():
    global usr
    with open("Users\\Current Signed In Account.txt","r") as f:
        usr = f.read()


accounts = ()
def acc_csv():
    get_user_account()                             # Storing all accounts in text file for easier creation of ledger
    global accounts
    a = open(f"Users\\{usr}\\Processing Files\\AllAcounts.txt","a+")
    a.seek(0)
    accounts = tuple(a.read()[:-1].split(','))
    a.close()