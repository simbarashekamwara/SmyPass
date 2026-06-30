import sys
import getpass
import os
import time
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey , AlreadyFinalized
from cryptography.fernet import Fernet
from smypass_guard import Smypass_guard , Breached , WeakPass
from inputimeout import inputimeout, TimeoutOccurred
import secrets 
import csv
import tldextract
from prettytable import PrettyTable, ALL, NONE
from colorama import init, Fore, Style
from pyfiglet import Figlet





init(autoreset=True)
def show_banner():
    f = Figlet(font='slant')
    title = f.renderText('SmyPass')
    print(f"{Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}        Your passwords, secured{Style.RESET_ALL}\n")


def home():
    while True:
        os.system("cls")
        show_banner()

        print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Login")
        print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Create Account")
        print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Exit\n")

        choice = get_input(f"{Fore.YELLOW}Enter your choice:  {Style.RESET_ALL}", int)

        if choice == 1: 
            logged_in = login()
            if logged_in is not None and logged_in[0] == True:
                homepage(logged_in[1])
            
        elif choice == 2:
            Register(load_users())
        elif choice == 3:
            sys.exit()

        file_path = "user.txt"
        if not os.path.exists(file_path):
            open(file_path, "a").close()

        user = {}
        
        with open(file_path, "r") as f: 
            for line in f:
                key, val, salt, keyen = line.split()
                user[key] = [val, salt, keyen]

def Register(user):
    while True:

        username = get_input(f"{Fore.YELLOW}Enter your username:  {Style.RESET_ALL}")
        if username not in  user:
            break
        print(f"{Fore.MAGENTA}Username unavailable choose another. {Style.RESET_ALL}")

    while True:
        try:

            password = Smypass_guard(get_input(f"{Fore.YELLOW}Enter your password:  {Style.RESET_ALL}")).run()
            break
        
        except Breached:
            print(f"{Fore.RED}This password has been found in known data breaches. Choose a different, unique password.{Style.RESET_ALL}")
            time.sleep(1)
        except WeakPass:
            pass

    confirm_password = get_input(f"{Fore.YELLOW}Confirm your password:  {Style.RESET_ALL}")
    salt  = os.urandom(16)
    kdf   = Scrypt(salt=salt,length=32,n=2**14,r=8,p=1,)
    keyen = Fernet.generate_key()

    if password == confirm_password or confirm_password == "suggest":

        password = kdf.derive(password.encode()).hex() 
        user = load_users()
        user[username] = [password, salt.hex(), keyen.hex()]
        
        with open("user.txt", "a") as f:
            f.write(username + " " + password + " " + salt.hex() + " " + keyen.hex() + "\n")
            
        open(f"{username}.txt", "w").close()  
        print(f"{Fore.GREEN}Account Created successfully.{Style.RESET_ALL}\n")           
        time.sleep(1)
        home()
    else:       
        print(f"{Fore.RED}Password doesn't match.{Style.RESET_ALL}\n")
        time.sleep(1)


def login():
    os.system("cls")
    

def login():

    os.system("cls")
    print(f"{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════════╗")
    print(f"║                Login               ║")
    print(f"╚════════════════════════════════════╝{Style.RESET_ALL}\n")

    username = get_input(f"{Fore.YELLOW}Enter your username (or 'b' to go back): {Style.RESET_ALL}")
    if username.lower() == 'b':
        return None
    
    password = getpass.getpass(f"{Fore.YELLOW}Enter your password: {Style.RESET_ALL}")
    user = load_users()
    
    if username in user:
        try:
            
            kdf = Scrypt(salt=bytes.fromhex(user[username][1]),length=32,n=2**14,r=8,p=1,) 
            kdf.verify(password.encode(), bytes.fromhex(user[username][0])) 
            print(f"{Fore.GREEN}✓ Login successful! Welcome back, {username}.{Style.RESET_ALL}\n")
            time.sleep(1)
            return [True, username]
        
        except (InvalidKey, AlreadyFinalized):
            print(f"{Fore.RED}✗ Invalid username or password.{Style.RESET_ALL}\n")
            time.sleep(1)
        
    else:

        os.system("cls")
        print(f"{Fore.RED}✗ Account doesn't exist.{Style.RESET_ALL}\n")
        print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Create Account")
        print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Exit\n")

        choice = get_input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}", int)
        if choice == 1:
            Register(load_users())
        elif choice == 2:
            sys.exit()
        else:
            home()


def homepage_banner(username):

    print(f"{Fore.CYAN}{Style.BRIGHT}╔════════════════════════════════════╗")
    print(f"║         SmyPass - {username:<14}   ║")
    print(f"╚════════════════════════════════════╝{Style.RESET_ALL}\n")


def homepage(username):

    while True: 
        
        os.system("cls")
        homepage_banner(username)
        data = []

        with open(f"{username}.txt", "r") as f:
            for line in f:
                uuid, name, user_name, password, website_url = line.strip().split() 
                data.append([   decrypter(bytes.fromhex(uuid), username).decode("utf-8"),
                                decrypter(bytes.fromhex(name), username).decode("utf-8"),
                                decrypter(bytes.fromhex(user_name), username).decode("utf-8"), decrypter(bytes.fromhex(password), username).decode("utf-8"),
                                decrypter(bytes.fromhex(website_url), username).decode("utf-8")])
            
            data.sort(key=lambda row: int(row[0]))
            table(data, headers = ["Uuid", "Name", "Username", "Password", "Website_url"])

        print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Add")
        print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Import CSV")
        print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Update")
        print(f"  {Fore.GREEN}[4]{Style.RESET_ALL} Delete")
        print(f"  {Fore.GREEN}[5]{Style.RESET_ALL} Settings")
        print(f"  {Fore.GREEN}[6]{Style.RESET_ALL} Log-out")
        
       
        choice = get_input(f"{Fore.YELLOW}Enter option:  {Style.RESET_ALL}", int ,300)


        if choice == 1:
            add_password(username)
            print(f"{Fore.GREEN} Account successfully added.{Style.RESET_ALL}\n")
            time.sleep(1)
            
        elif choice == 2:
            import_csv(username)
            

        elif choice == 3:
            update_password(username)
            print(f"{Fore.GREEN} Account successfully updated.{Style.RESET_ALL}\n")
            time.sleep(1)

        elif choice == 4:
            delete_account(username)
            print(f"{Fore.RED} Account Deleted {username}.{Style.RESET_ALL}\n")
            time.sleep(1)

        elif choice == 5:
            account_settings(username)
            return
        
        elif choice == 6:
            return
            
def encrypter(text, username):
    f = Fernet(bytes.fromhex(load_users()[username][2]))
    return  f.encrypt(text.encode())

def decrypter(text, username):
     f = Fernet(bytes.fromhex(load_users()[username][2]))
     return f.decrypt(text)


#File to save password
def add_password(username):

    name = encrypter(get_input(f"{Fore.YELLOW}Enter account name:{Style.RESET_ALL}"), username).hex()
    account_username = encrypter(get_input(f"{Fore.YELLOW}Enter the  account username:{Style.RESET_ALL}"), username).hex()
    acc_password     = get_input(f"{Fore.YELLOW}Enter the account password:{Style.RESET_ALL}")
    website_url = encrypter(get_input(f"{Fore.YELLOW}Enter the account website(type - if none){Style.RESET_ALL}"), username).hex()
    uuid =  encrypter(unique_id(), username).hex()


    try:
        print(f"{Fore.YELLOW}Password does not meet the recommended strength requirements. Consider making the following changes:{Style.RESET_ALL}\n")
        Smypass_guard(acc_password).strength_checker()
       
    except Breached:
        print(f"{Fore.RED}NB: This password has been found in known data breaches. Consider using  a different, unique password.{Style.RESET_ALL}\n")
        time.sleep(1)
        
    acc_password = encrypter(acc_password, username).hex()
    

    with open(f"{username}.txt", "a") as f:
        f.write(uuid + " " + name + " " +  account_username + " " + acc_password + " " + website_url + "\n")


def update_password(username, useraccount=False):

    if not useraccount:
         
        unique_id    = get_input(f"{Fore.YELLOW}Enter the UUID of the  account you want to update:{Style.RESET_ALL}")

    new_password = get_input(f"{Fore.YELLOW}Enter the new account password:{Style.RESET_ALL}")
    

    try:
        
        Smypass_guard(new_password).strength_checker()
    
    except Breached:
          print(f"{Fore.RED}NB: This password has been found in known data breaches. Consider using  a different, unique password.{Style.RESET_ALL}\n")
          time.sleep(1)
    except WeakPass:
        pass      

    if useraccount: 
        user = load_users()
        with open("user.txt", "r") as f:
            lines = f.readlines()
        with open("user.txt", "w") as f:
        
            for line in lines:
                user_name, password, salt , key = line.strip().split()
                #user_name =  decrypter(bytes.fromhex(user_name), global_key).decode("utf-8") to actuvate when the logic for uysername encrpt is in place
                
                if user_name == username:
                    kdf   = Scrypt(salt=bytes.fromhex(salt),length=32,n=2**14,r=8,p=1,)
                    new_password = kdf.derive(new_password.encode()).hex()
                    
                    print(f"Debugger users: {user}")
                    user[username][0] = new_password

                    f.write(username + " " + new_password + " " + salt + " " + key + "\n")
                    

                else:
                    f.write(user_name + " " + password + " " + salt + " " + key + "\n")

                

    else: 
        with open(f"{username}.txt", "r") as f:
            lines = f.readlines()
        with open(f"{username}.txt", "w") as f:
            for line in lines:
                uuid, name, account, password, website_url = line.strip().split() 
                uuid = decrypter(bytes.fromhex(uuid), username).decode("utf-8")

                if uuid == unique_id:
                    f.write(encrypter(uuid, username).hex() + " " + name + " " + account + " " + encrypter(new_password, username).hex() + " " + website_url + "\n")
                else:
                    f.write(encrypter(uuid, username).hex() + " " + name + " " + account + " " +  password + " " + website_url + "\n")
        
        

        
def delete_account(username):

    unique_id = get_input(f"{Fore.YELLOW}Enter the UUID of the account you want to delete: {Style.RESET_ALL}")
   
    with open(f"{username}.txt", "r") as f:
        lines = f.readlines()
    with open(f"{username}.txt", "w") as f:
        for line in lines:
            uuid, name, account, password, website_url = line.strip().split() 
            uuid = decrypter(bytes.fromhex(uuid),  username).decode("utf-8")
           
        
            if uuid != unique_id:
                f.write(encrypter(uuid, username).hex() + " " + name + " " + account + " " +  password + " " + website_url+ "\n")
    

def delete_useraccount(username):
    
    with open("user.txt", "r") as f:
        lines = f.readlines()
    with open("user.txt", "w") as f:
        for line in lines:
            if username not in line:
                f.write(line)
    os.remove(f"{username}.txt")

def account_settings(username):

    print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Change password")
    print(f"  {Fore.GREEN}[2]{Style.RESET_ALL} Delete Account")
    print(f"  {Fore.GREEN}[3]{Style.RESET_ALL} Back")
    
    choice = get_input(f"{Fore.YELLOW}Enter option:  {Style.RESET_ALL}", int)
  

    if choice == 1:
        update_password( username, True)
        print(f"{Fore.GREEN}Password successfully changed.{Style.RESET_ALL}\n")
        time.sleep(1)

    elif choice == 2:
        delete_useraccount(username)
        print(f"{Fore.RED}Account successfully deleted.{Style.RESET_ALL}\n")
        time.sleep(1)
        return
        

    elif choice == 3:
        homepage(username)

def get_input(text, convert = str, timeout=None):
    while True:
        try:
            if timeout == None:
                return convert(input(text))
            else:
                return convert((inputimeout(text, timeout)).strip())
        except (ValueError, EOFError):
            pass
        except KeyboardInterrupt:
            home()
        except TimeoutOccurred:
            print(f"{Fore.RED}Session timed-out.{Style.RESET_ALL}\n")
            time.sleep(1)
            home()

def unique_id():
    low, high = 1000, 9999
    return str(low + secrets.randbelow(high - low + 1))





def load_users():
    user = {}
    if os.path.exists("user.txt"):
        with open("user.txt", "r") as f:
            for line in f:
                key, val, salt, keyen = line.split()
                user[key] = [val, salt, keyen]
    return user


def import_csv(username):


    
  
    while True:
        csv_file = get_input(f"{Fore.YELLOW}Enter the full path to the CSV file you want to import(or 'b' to go back): {Style.RESET_ALL}").strip('"')
        if csv_file.lower() == 'b':
            return
        
       
        try:
            if os.path.exists(csv_file):
                with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
                    reader = csv.reader(file)

                    header = next(reader)
                    for row in reader:
                        name, website_url , account_username, acc_password, _ = row
                        with open(f"{username}.txt", "a") as f:
                            f.write(encrypter(unique_id(), username).hex() + " " + encrypter(tldextract.extract(name).domain, username).hex() + " " +  encrypter(account_username, username).hex() + " " + encrypter(acc_password, username).hex() + " " + encrypter(website_url, username).hex() + "\n")
                print(f"{Fore.GREEN} CSV successfully imported.{Style.RESET_ALL}\n")
                time.sleep(1)
                break

            else:
                print(f"{Fore.RED}File {csv_file} does not exist.{Style.RESET_ALL}")
                time.sleep(1)

        except OSError as e:
            print(f"{Fore.RED}Error reading file: {e}.{Style.RESET_ALL}")
            time.sleep(1)



def table(data, headers):
    t = PrettyTable()
    t.field_names = headers
    for row in data:
        t.add_row(row)
    t.hrules = ALL   # horizontal line after every row
    t.vrules = NONE    # no vertical bars
    
    t.max_width["UUID"] = 4
    t.max_width["Name"] = 15
    t.max_width["Username"] = 45
    t.max_width["Password"] = 15
    t.max_width["Website_url"] = 50
    #print(t)

    output = str(t).split("\n")
    output[1] = f"{Style.BRIGHT}{Fore.CYAN}{output[1]}{Style.RESET_ALL}"
    print("\n".join(output))


def main():
    home()


































if __name__  == "__main__":
    main()

    



