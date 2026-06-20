import sys
import getpass
from tabulate import tabulate
import os
import time
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey , AlreadyFinalized
from cryptography.fernet import Fernet







def home():
    os.system("cls")
    print("####################################\nWelcome To SmyPass\n####################################")
    print("1. Login\n2. Register\n3. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1: 
        logged_in = login()
        if logged_in is not None and logged_in[0]== True:
            homepage(logged_in[1])
        

    elif choice == 2:
        Register()
    elif choice == 3:
        sys.exit()

file_path = "user.txt"
if not os.path.exists(file_path):
    open(file_path, "a").close()

user={}
 
with open(file_path, "r") as f:
    for line in f:
        (key, val, salt, keyen) = line.split()
        user[key] = [val, salt, keyen]

def Register():
    username=input("Enter your username: ")
    password=input("Enter your password: ")
    confirm_password=input("Confirm your password: ")
    salt = os.urandom(16)
    kdf = Scrypt(salt=salt,length=32,n=2**14,r=8,p=1,)
    keyen = Fernet.generate_key()

    if password == confirm_password:

        user[username] = kdf.derive(password.encode())
        with open("user.txt", "a") as f:
            f.write(username + " " + user[username].hex() + " " + salt.hex() + " " + keyen.hex() + "\n")

        open(f"{username}.txt", "w").close()            
        print("Registration successful")
        time.sleep(3)
        home()
    else:       
        print("Password Does not match")



def login():
    os.system("cls")
    print("####################################\nLogin\n####################################")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    
    
    if username in user:
        try:
            kdf = Scrypt(salt=bytes.fromhex(user[username][1]),length=32,n=2**14,r=8,p=1,) #need to change user to carry 3 fileds including salt
            kdf.verify(password.encode(), bytes.fromhex(user[username][0])) #neeed to store the created salt value in reg 
            print("Login successful")
            return [True, username]
        except (InvalidKey, AlreadyFinalized):
            print("Incorrect Password")
        
    else:
        choice = int(input("Account Doesn't exist\nType 1 to Create Account\n or 2 to exit\n"))
        if choice ==1:
            Register()
        elif choice == 2:
            sys.exit()
        else:
            home()

def homepage(username):
    while True:
        
        os.system("cls")
        data = []

        with open(f"{username}.txt", "r") as f:
            for line in f:
                account, password = line.strip().split()  # Assumes space-separated values
                data.append([decrypter(bytes.fromhex(account), username), decrypter(bytes.fromhex(password), username)])

        print(tabulate(data, headers=["Account", "Password"])) 

    
        print("1. Add\n2.Update\n3.Delete\n4.Settings\n5.Exit\n")
        choice=int(input("Enter Option: "))

        if choice == 1:
            add_password(username)
            print("Password Added")
        
        elif choice == 2:
            update_password(username)
            print("Password Updated")
        
        elif choice == 3:
            delete_account(username)
            print("Account Deleted")
        
        elif choice == 4:
            account_settings(username)

        elif choice == 5:
            sys.exit()
            
def encrypter(text, username):
    f = Fernet(bytes.fromhex(user[username][2]))
    return  f.encrypt(text.encode())

def decrypter(text, username):
     f = Fernet(bytes.fromhex(user[username][2]))
     return f.decrypt(text)


#File to save password
def add_password(username):
    
    Account_UserName = encrypter(input("Enter the account username: "), username)
    Acc_Password = encrypter(input("Enter the account Password: "), username)
    with open(f"{username}.txt", "a") as f:
        f.write(Account_UserName.hex() + " " + Acc_Password.hex() + "\n")

#Update Password
def update_password(username):
    acc = encrypter(input("Enter the account you want to update: "), username)
    new_password = encrypter(input("Enter the new password: "), username)

    with open(f"{username}.txt", "r") as f:
        lines = f.readlines()
    with open(f"{username}.txt", "w") as f:
        for line in lines:
            if acc in line:
                f.write(acc + " " + new_password + "\n")
            else:
                f.write(line)
    

            
def delete_account(username):
    acc= encrypter(input("Enter the account you want to delete: "), username)

    with open(f"{username}.txt", "r") as f:
        lines = f.readlines()
    with open(f"{username}.txt", "w") as f:
        for line in lines:
            if acc not in line:
                f.write(line)
    

def delete_useraccount(username):
    

    with open("user.txt", "r") as f:
        lines = f.readlines()
    with open("user.txt", "w") as f:
        for line in lines:
            if username not in line:
                f.write(line)
    os.remove(f"{username}.txt")

def account_settings(username):

    print("1. Change Password\n2. Delete Account\n3. Back")
    choice = int(input("Enter your choice: "))
    

    if choice == 1:
        update_password(username)
        print("Password Changed")
    elif choice == 2:
        delete_useraccount(username)
        print("Account Deleted")
        time.sleep(3)
        home()
        

    elif choice == 3:
        homepage(username)

def main():
    home()



























































































if __name__  == "__main__":
    main()



