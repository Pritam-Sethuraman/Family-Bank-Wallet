import json
from datetime import datetime as dt


class Bank:
    # Variables
    __primary_acc_no = '123456'
    __primary_acc_bal = 1000.00

    __secondary_acc_no = '654321'
    __secondary_acc_bal = 700.00

    # Methods
    def getPrimaryAccNo(self):
        return self.__primary_acc_no

    def getSecondaryAccNo(self):
        return self.__secondary_acc_no

    def getPrimaryBalance(self):
        return self.__primary_acc_bal

    def getSecondaryBalance(self):
        return self.__secondary_acc_bal

    def debitPrimaryBank(self, amount: float):
        self.__primary_acc_bal -= amount
        print(f'Amount debited from Primary Bank: {amount}\n')
        print(f'Current Primary Account Balance: {self.__primary_acc_bal}\n')

    def debitSecondaryBank(self, amount: float):
        self.__secondary_acc_bal -= amount
        print(f'Amount debited from Secondary Bank: {amount}\n')
        print(f'Current Secondary Account Balance: {self.__secondary_acc_bal}\n')

    def creditPrimaryBank(self, amount: float):
        self.__primary_acc_bal += amount
        print(f'Amount credited from Primary Bank: {amount}\n')
        print(f'Current Primary Account Balance: {self.__primary_acc_bal}\n')

    def creditSecondaryBank(self, amount: float):
        self.__secondary_acc_bal += amount
        print(f'Amount credited from Secondary Bank: {amount}\n')
        print(f'Current Secondary Account Balance: {self.__secondary_acc_bal}\n')


class Wallet(Bank):
    # Variables
    __wallet_balance = 475.00
    child_txn_count = 0
    master_key = 'master'

    __users = {
        'Adam': 'Dad',
        'Eve': 'Mom',
        'Harry': 'Child',
        'Anna': 'Child',
        'Ron': 'Child',
        'Malfoy': 'Child',
        'Tom': 'Child',
        'Jerry': 'Child',
        'Rick': 'Child',
        'Morty': 'Child',
    }

    __user_access = {
        'Adam': 'Granted',
        'Eve': 'Granted',
        'Harry': 'Granted',
        'Anna': 'Granted',
        'Ron': 'Granted',
        'Malfoy': 'Granted',
        'Tom': 'Granted',
        'Jerry': 'Granted',
        'Rick': 'Granted',
        'Morty': 'Granted',
    }

    data = {
        'transactions': [

        ],
        'wallet_balance': None,
        'primary_bank_balance': None,
        'secondary_bank_balance': None
    }

    # Member Functions
    def getWalletBalance(self):
        return self.__wallet_balance

    def addMoney(self, amount: float, acc_no: str, user: str):
        if acc_no == self.getPrimaryAccNo():
            if amount > self.getPrimaryBalance():
                print('Insufficient Balance in Primary Bank!')
            else:
                self.__wallet_balance += amount
                self.debitPrimaryBank(amount)
        elif acc_no == self.getSecondaryAccNo():
            if amount > self.getSecondaryBalance():
                print('Insufficient Balance in Secondary Bank!')
            else:
                self.__wallet_balance += amount
                self.debitSecondaryBank(amount)
                self.recordTransaction(
                    {
                        "date": dt.now().strftime("%x"),
                        "time": dt.now().strftime("%X"),
                        "user": user,
                        "merchant": acc_no,
                        "amount": +amount,
                    }
                )

    def creditWallet(self, amount: float):
        self.__wallet_balance += amount
        print(f'Amount credited to wallet: {amount}\n')
        print(f'Current Wallet Balance: {self.__wallet_balance}\n')

    def debitWallet(self, amount: float):
        self.__wallet_balance -= amount
        print(f'Amount debited from wallet: {amount}\n')
        print(f'Current Wallet Balance: {self.__wallet_balance}\n')

    def payMoney(self, user: str, amount: float, merchant_name: str):
        if amount <= self.__wallet_balance:
            self.debitWallet(amount)
            self.recordTransaction(
                {
                    "date": dt.now().strftime("%x"),
                    "time": dt.now().strftime("%X"),
                    "user": user,
                    "merchant": merchant_name,
                    "amount": -amount,
                }
            )
        else:
            print('Insufficient Funds in Wallet')

    def payMoneyAsChild(self, user: str, amount: float, merchant: str):
        if amount <= self.__wallet_balance:
            if self.child_txn_count < 1:
                if amount > 50:
                    print('Value more than $50\n')
                    user_input = input('Ask mom for permission?(Y/N): ')
                    if user_input == 'Y' or user_input == 'y':
                        self.sendRequestToMom(user, amount)
                    else:
                        print('Thank you!\n')
            else:
                print('Transaction Limit exceeded!')
                user_input = input('Ask for permission?(Y/N): ')
                if user_input == 'Y' or user_input == 'y':
                    access_code = input('Enter masterkey password: ')
                    if access_code == self.master_key:
                        self.child_txn_count -= 1
                        self.payMoney(user, amount, merchant)
                        self.child_txn_count += 1
        else:
            print('Insufficient Funds in Wallet')

    def withdrawMoney(self, user: str, amount: float, merchant_name: str):
        self.debitWallet(amount)
        self.recordTransaction(
            {
                "date": dt.now().strftime("%x"),
                "time": dt.now().strftime("%X"),
                "user": user,
                "merchant": merchant_name,
                "amount": -amount,
                "balance": self.__wallet_balance
            }
        )

    def recordTransaction(self, txn: dict):
        with open("data.json", "r+") as file:
            file_data = json.load(file)
            file_data["transactions"].append(txn)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def saveBalance(self):
        with open("data.json", 'r+') as file:
            file_data = json.load(file)
            file_data["wallet_balance"] = self.getWalletBalance()
            file_data["primary_bank_balance"] = self.getPrimaryBalance()
            file_data["secondary_bank_balance"] = self.getSecondaryBalance()
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def viewTransactions(self):
        with open("data.json", "r") as read_file:
            print(json.load(read_file))

    def blockUser(self):
        for key in self.__user_access.keys():
            print(key, ': ', self.__user_access[key])
        choice = input('Choose the user to block/unblock: ')
        for key in self.__user_access:
            if choice == key:
                if self.__user_access[key] == 'Granted':
                    tempDict = {choice: 'Denied'}
                    self.__user_access.update(tempDict)
                else:
                    tempDict = {choice: 'Granted'}
                    self.__user_access.update(tempDict)
                print('Access Modified Successfully')

    def sendRequestToMom(self, user: str, amount: float):
        user_input = input(f'[Mom] Accept transaction of ${amount}? (Y/N): ')
        if user_input == 'Y' or user_input == 'y':
            self.payMoney(user, amount, merchant)
            self.child_txn_count += 1
        else:
            user_input = input(f'Transfer request of ${amount} to Dad? (Y/N): ')
            if user_input == 'Y' or user_input == 'y':
                self.sendRequestToDad(amount)
            else:
                print('Your mother decline the transaction. Good luck kiddo :)\n')

    def sendRequestToDad(self, amount: float):
        user_input = input(f'[Dad] Accept transaction of ${amount}? (Y/N): ')
        if user_input == 'Y' or user_input == 'y':
            return True
        else:
            return False

    def checkLowBalance(self):
        if self.__wallet_balance < 100:
            return True

    def isGranted(self, user_name: str):
        for key in self.__user_access.keys():
            if user_name == key:
                if self.__user_access[key] == 'Granted':
                    return True
                else:
                    return False

class Dad(Wallet):
    # Attributes
    __password = 'adam'
    dad_menu = {
        1: 'Pay using Wallet',
        2: 'Withdraw Money',
        3: 'Add Funds',
        4: 'View Transactions',
        5: 'Block/Unblock User',
        6: 'Logout',
        7: 'Exit',
    }

    # Member Functions
    def printDadMenu(self):
        for key in self.dad_menu.keys():
            print(key, '--', self.dad_menu[key])

    def authDad(self, pwd: str):
        if pwd == self.__password:
            return True
        else:
            return False


class Mom(Wallet):
    # Variables
    __password = 'eve'
    mom_menu = {
        1: 'Pay using Wallet',
        2: 'Withdraw Money',
        3: 'Add Funds',
        4: 'View Transactions',
        5: 'Logout',
        6: 'Exit',
    }

    # Methods
    def printMomMenu(self):
        for key in self.mom_menu.keys():
            print(key, '--', self.mom_menu[key])

    def authMom(self, pwd: str):
        if pwd == self.__password:
            return True
        else:
            return False


class Child(Wallet):
    # Variables
    child_select = {
        1: 'Harry',
        2: 'Anna',
        3: 'Ron',
        4: 'Malfoy',
        5: 'Tom',
        6: 'Jerry',
        7: 'Rick',
        8: 'Morty',
    }

    child_menu = {
        1: 'Pay using Wallet',
        2: 'Logout',
        3: 'Exit',
    }

    # Member Functions
    def printChildMenu(self):
        for key in self.child_menu.keys():
            print(key, '--', self.child_menu[key])

    def printChildSelectMenu(self):
        for key in self.child_select.keys():
            print(key, '--', self.child_select[key])


if __name__ == '__main__':
    # Initializing Objects
    dad = Dad()
    mom = Mom()
    child = Child()

    # Main Menu Interface
    main_menu = {
        1: 'Dad',
        2: 'Mom',
        3: 'Child',
        4: 'Exit',
    }

    def printMainMenu():
        for key in main_menu.keys():
            print(key, '--', main_menu[key])

    # Console Menu
    while True:
        print('--------------------------------------------------------------------------------------')
        print('$$$ Family Bank Wallet $$$')
        print('--------------------------------------------------------------------------------------')
        printMainMenu()
        user_input = ''
        try:
            user_input = int(input('Enter your choice: '))
        except:
            print('Incorrect Input. Please enter a number...')
        # Dad Menu
        if user_input == 1:
            pwd = input('Enter Password: ')
            if dad.authDad(pwd):
                while True:
                    print('--------------------------------------------------------------------------------------')
                    print('Welcome Adam!')
                    print('--------------------------------------------------------------------------------------')
                    if dad.checkLowBalance():
                        print('Wallet Balance less than $100. Recharge Needed!\n')
                    dad.printDadMenu()
                    option = ''
                    try:
                        option = int(input('Enter your choice: '))
                    except:
                        print('Incorrect Input. Please enter a number...')
                    if option == 1:
                        amount = float(input('Enter amount to be paid: '))
                        merchant = input('Enter the name of merchant: ')
                        dad.payMoney('Adam', amount, merchant)
                    elif option == 2:
                        amount = float(input('Enter amount to be withdrawn: '))
                        dad.withdrawMoney('Adam', amount, 'Self Withdraw')
                    elif option == 3:
                        amount = float(input('Enter amount to be added: '))
                        acc_no = input('Enter Account Number: ')
                        dad.addMoney(amount, acc_no, 'Adam')
                    elif option == 4:
                        dad.viewTransactions()
                    elif option == 5:
                        dad.blockUser()
                    elif option == 6:
                        print('Logout Successful!')
                        break
                    elif option == 7:
                        dad.saveBalance()
                        print('Thank you!')
                        exit()
        # Mom Menu
        elif user_input == 2:
            if mom.isGranted('Eve'):
                pwd = input('Enter Password: ')
                if mom.authMom(pwd):
                    while True:
                        print('--------------------------------------------------------------------------------------')
                        print('Welcome Eve!')
                        print('--------------------------------------------------------------------------------------')
                        if mom.checkLowBalance():
                            print('Wallet Balance less than $100. Recharge Needed!\n')
                        mom.printMomMenu()
                        option = ''
                        try:
                            option = int(input('Enter your choice: '))
                        except:
                            print('Incorrect Input. Please enter a number...')
                        if option == 1:
                            amount = float(input('Enter amount to be paid: '))
                            merchant = input('Enter the name of merchant: ')
                            mom.payMoney('Eve', amount, merchant)
                        elif option == 2:
                            amount = float(input('Enter amount to be withdrawn: '))
                            mom.withdrawMoney('Eve', amount, 'Self Withdraw')
                        elif option == 3:
                            amount = float(input('Enter amount to be added: '))
                            acc_no = input('Enter Account Number: ')
                            mom.addMoney(amount, acc_no, 'Eve')
                        elif option == 4:
                            mom.viewTransactions()
                        elif option == 5:
                            print('Logout Successful!')
                            break
                        elif option == 6:
                            mom.saveBalance()
                            print('Thank you!')
                            exit()
            else:
                print('Eve is blocked from the Wallet!')
        # Child Menu
        elif user_input == 3:
            child.printChildSelectMenu()
            child_name = ''
            try:
                choice = int(input('Enter your choice: '))
                child_name = child.child_select[choice]
            except:
                print('Incorrect Input. Please enter a number...')
            if child.isGranted(child_name):
                while True:
                    print('--------------------------------------------------------------------------------------')
                    print(f'Welcome {child_name}!')
                    print('--------------------------------------------------------------------------------------')
                    child.printChildMenu()
                    option = ''
                    try:
                        option = int(input('Enter your choice: '))
                    except:
                        print('Incorrect Input. Please enter a number...')
                    if option == 1:
                        amount = float(input('Enter amount to be paid: '))
                        merchant = input('Enter the name of merchant: ')
                        child.payMoneyAsChild(child_name, amount, merchant)
                    elif option == 2:
                        print('Logout Successful!')
                        break
                    elif option == 3:
                        child.saveBalance()
                        print('Thank You!')
                        exit()
            else:
                print(f'{child_name} is Blocked from the Wallet!')
        # Exit Case
        elif user_input == 4:
            print('Thank you!')
            exit()
        else:
            print('Invalid Option. Please enter a number between 1 and 4')
