import csv
import datetime as dt
import Login_Page as lg
import Common_Commands as cc

def save_journal(debit,credit,amount,narration):
    if debit and credit and amount and narration:                                      # Saving them in csv file
        with open(f"Users\\{cc.usr}\\Processing Files\\journal_entries.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([dt.date.today(), debit, credit, amount, narration])
    create_accounts()

def create_accounts():                                                              # Saving accounts in txt file
    with open(f"Users\\{cc.usr}\\Processing Files\\AllAcounts.txt","a+") as a:
        with open(f"Users\\{cc.usr}\\Processing Files\\journal_entries.csv", 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                a.seek(0)
                acc = a.read()[:-1].split(',')
                date, debit, credit, amount, narration = row
                if debit not in acc:
                    a.write(debit + ",")
                if credit not in acc:
                    a.write(credit + ",")
