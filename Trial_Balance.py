from tkinter import *
from tkinter import ttk
import pandas as pd
import xlsxwriter as xlsx
import Login_Page as lp
import Journals
import Ledger
import Common_Commands as cc

def create_trial_balance():                            # Creation of Trial Balance and writing to xlsx file
    workbook = xlsx.Workbook(f"Users\\{cc.usr}\\Processing Files\\Trial Balance.xlsx")
    worksheet = workbook.add_worksheet("Trial Balance")
    worksheet.set_column('A:A', 35)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.write('A1', 'Particulars')
    worksheet.write('B1', 'Debit')
    worksheet.write('C1', 'Credit')
    
    cc.acc_csv()
    Ledger.create_ledgerdict()

    row = 1
    db,cb = 0,0         # Finding total
    for i in Journals.accounts:
        for x,y in Ledger.ledger_dict[i]['next year balance']:
            
            if x == "To Balance b/d":
                worksheet.write(row, 0, i) 
                worksheet.write(row, 1, y)
                worksheet.write(row, 2, " ")
                db += y
                row = row + 1
            elif x == "By Balance b/d":
                worksheet.write(row, 0, i)
                worksheet.write(row, 1, " ") 
                worksheet.write(row, 2, y)
                cb += y
                row = row + 1
            elif x == "N/a":
                pass
                
    row += 1
    worksheet.write(row, 0, "Total")
    worksheet.write(row, 1, db)
    worksheet.write(row, 2, cb)
                
    workbook.close()

def display_trialbalance():                             # Displaying trial balance
    create_trial_balance()

    