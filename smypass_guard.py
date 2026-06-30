
import pwnedpasswords
import urllib
from password_strength import PasswordPolicy 
from password_strength.tests import Length, Uppercase, Numbers, Special, NonLetters
import secrets
import string
from colorama import init, Fore, Style
import time


class Smypass_guard:
    def __init__ (self, password: any):
        self.password = password
        self.policy = PasswordPolicy.from_names(length=8, uppercase=2, numbers=2, special=2, nonletters=2) #rules to check strength of password can be changed as per the needs
    
    def run(self):
        if self.password == "suggest":
           return self.password_generator()
        else:
            return self.strength_checker()


    def strength_checker(self):
        
        try:
            breaches =  pwnedpasswords.check(self.password)
        
        except urllib.error.URLError:
            breaches = 0
            
        if breaches:
                raise Breached
        else: 
            result =  self.policy.test(self.password)
            if not result:
                return self.password
            else:
                comment = { Length        :   "Password must be at least 8 characters long."
                           , Uppercase    :    "Add at least 2 uppercase letters (A-Z)."
                           , Numbers       :   "Add at least 2 numbers (0-9)."
                           , Special       :   "Add at least 2 special characters (e.g., ! @ # $ %)."
                           , NonLetters    :   "Add at least 2 non-letter characters (numbers or symbols)."
                           }
                for fail in result:
                    print(f"{Fore.CYAN}{comment[type(fail)]}{Style.RESET_ALL}")
                    time.sleep(1)
                raise WeakPass
    def password_generator(self):
        while True:
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            generated_password = ''.join(secrets.choice(alphabet) for _ in range(16))

            if not self.policy.test(generated_password):
        
                 return generated_password
    
        

class Breached(Exception):
    pass
class WeakPass(Exception):
    pass