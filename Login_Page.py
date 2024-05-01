import os
import Common_Commands as cc

def sign_in(usr,pas):              # Signing / Logging in to a Account 
    try:
        with open("Users\\All Acounts Created.txt","r") as uac:
            a = uac.read().split(';')
            users = []
            passes = []
            if a != []:
                for i in a:
                    if i != "":
                        users.append(i.split(",")[0])
                        passes.append(i.split(",")[1])
            if usr in users:
                if pas == passes[users.index(usr)]:
                    print("Logged In")                                    
                    
                    with open("Users\\Current Signed In Account.txt","w") as f:
                        f.write(usr)
                    cc.get_user_account()
                    return "Logged In"

                else:
                    print("Password Incorret")
            else:
                print("Username Not In Database")
    except:
        print("Username Not in Database")

def sign_up(usr,pas):              # Creating an Account
    allchrsfor_pas = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890!@#*_:;"
    with open("Users\\All Acounts Created.txt","a+") as uac:
        uac.seek(0)
        a = uac.read().split(';')
        usrs = []
        if a != []:
            for i in a:
                usrs.append(i.split(",")[0])
            if usr in usrs:
                print("Username Already Exists")
            else:
                lpas = list(pas)    
                a = True
                
                if len(pas) < 8:
                    print("Password Is Short")

                elif len(pas) >= 8:
                    
                    for i in lpas:
                        
                        if i not in allchrsfor_pas:
                            a = False
                    
                    if a == False:
                        print("Password Is Not As Per Rules")
                    
                    else:
                        uac.write(usr+","+pas+";")
                        print("Account Created")
                        
                        directory = r"Users\\" + usr + r"\\Processing Files"
                        os.makedirs(directory)
