import csv
import xlsxwriter as xlsx
import Login_Page as lp
import Journals
import Common_Commands as cc

ledger_dict = {}

def create_ledgerdict():            
    cc.acc_csv()
    global ledger_dict
    ledger_dict = {}
    for i in Journals.accounts:
        ledger_dict[i] = {"debit":[],"credit":[]}         # Creating dictionary of ledgers format Acouunt: {Debit,Credit}
    with open(f"Users\\{cc.usr}\\Processing Files\\journal_entries.csv", 'r') as f:      
        reader = csv.reader(f)
        for row in reader:
            date, debit, credit, amount, narration = row
            ledger_dict[debit]['debit'].append([date,credit, float(amount)])
            ledger_dict[credit]['credit'].append([date,debit, float(amount)])
             
    for i in ledger_dict:                       # Finding the balance to be c/d
        dtot, ctot = 0, 0
        for x,y,z in ledger_dict[i]['debit']:
            dtot = dtot + z
        for x,y,z in ledger_dict[i]['credit']:
            ctot = ctot + z

        if dtot > ctot:
            a = dtot - ctot
            ledger_dict[i]['credit'].append(['2024-04-30',"Balance c/d",a])
            ledger_dict[i]['total'] = dtot
            ledger_dict[i]['next year balance'] = [["To Balance b/d",a]]
        elif ctot > dtot:
            a = ctot - dtot
            ledger_dict[i]['debit'].append(['2024-04-30',"Balance c/d",a])
            ledger_dict[i]['total'] = ctot
            ledger_dict[i]['next year balance'] = [["By Balance b/d",a]]
        elif dtot == ctot:
            ledger_dict[i]['total'] = [dtot]
            ledger_dict[i]['next year balance'] = "N/a"

def create_ledger_xlsx():
    create_ledgerdict()

    workbook = xlsx.Workbook(f"Users\\{cc.usr}\\Processing Files\\Ledgers.xlsx")
    for account, values in ledger_dict.items():                # Writing dictionary of ledgers into xlsx file
        dbal,cbal = [],[]
        worksheet = workbook.add_worksheet(account)
        setup_worksheet(worksheet)
        drow = 1
        for date, other_account, amount in values['debit']:
            worksheet.write(drow, 0, date)
            worksheet.write(drow, 1, f'To {other_account}')
            worksheet.write(drow, 2, float(amount))
            drow += 1
            
        crow = 1
        for date, other_account, amount in values['credit']:
            worksheet.write(crow, 3, date)
            worksheet.write(crow, 4, f'By {other_account}')
            worksheet.write(crow, 5, float(amount))
            crow += 1
        

        if drow > crow:
            drow = drow + 1
            worksheet.write(drow, 2, ledger_dict[account]['total'])
            worksheet.write(drow, 5, ledger_dict[account]['total'])  

        if crow > drow:
            crow = crow + 1
            worksheet.write(crow, 2, ledger_dict[account]['total'])
            worksheet.write(crow, 5, ledger_dict[account]['total'])

        if crow == drow:
            crow = crow + 1
            worksheet.write(crow, 2, ledger_dict[account]['total'])
            worksheet.write(crow, 5, ledger_dict[account]['total'])
    workbook.close()

def setup_worksheet(worksheet):                       # Format for xlsx sheet for ledger
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 35)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 35)
    worksheet.set_column('F:F', 15)

    worksheet.write('A1', 'Date')
    worksheet.write('B1', 'Particulars')
    worksheet.write('C1', 'Debit Amount')
    worksheet.write('D1', 'Date')
    worksheet.write('E1', 'Particulars')
    worksheet.write('F1', 'Credit Amount')