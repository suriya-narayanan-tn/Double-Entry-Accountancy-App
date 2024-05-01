import google.generativeai as genai
import pandas as pd
from tkinter import messagebox

genai.configure(api_key="AIzaSyD031AAPGXs0xyWx1nBhNDxBAt7YZZQR6c")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

chat = model.start_chat(history=[])
chat

def chatinfo():
    try:
        with open("Chatbot\\Accounts Info.txt") as info:             # Sending accounting information
            chat.send_message(info.read())
        with open("Chatbot\\Accounts Commands.txt") as coms:         # Sending commands to follow     
            chat.send_message(coms.read()) 
        with open("Chatbot\\Gemini_Chat_History.txt","a+") as gch:           # Sending past history if any
            chat.send_message("Past Messages\n" + gch.read())
    except:
        messagebox.showinfo("Error Uploading File")

def enquire(ques):
    if ques == "/checkledger":
        try:
            with open("Processing Files\\journal_entries.csv", "r",) as f:
                file = pd.ExcelFile("Ledgers.xlsx")
                sheet_names = file.sheet_names
                gle = str(pd.read_excel("Ledgers.xlsx",sheet_name = sheet_names))
                    
                a = response.text
                return a
        except:
            a = "Journals and Ledgers Not Found In Directory"
            return a 
    
    elif ques == "/checktb":
        try:
            file = pd.ExcelFile("Processing Files\\Ledgers.xlsx")
            sheet_names = file.sheet_names
            gle = str(pd.read_excel("Ledgers.xlsx",sheet_name = sheet_names))
            gtb = str(pd.read_excel("Trial Balance.xlsx"))
            response = chat.send_message("/checktb Ledgers:\n" + gle + "Trial Balance:" + gtb)
            a = response.text
            return a
        except:
            a = "Ledger and Trial Balance Not Found In Directory"
            return a 


    elif ques != '':
        response = chat.send_message(ques)
        a = response.text
        return a