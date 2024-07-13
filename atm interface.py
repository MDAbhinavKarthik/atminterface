import random
import datetime

class User:
    def __init__(self, user_id, pin, name, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.name = name
        self.balance = balance
        self.transactions = []

    def display_balance(self):
        return f"Current Balance: ${self.balance}"

class Transaction:
    def __init__(self, amount):
        self.amount = amount
        self.timestamp = datetime.datetime.now()

    def execute(self, user):
        pass

class Withdrawal(Transaction):
    def execute(self, user):
        if user.balance >= self.amount:
            user.balance -= self.amount
            user.transactions.append(f"Withdrawal: ${self.amount} ({self.timestamp})")
            return True
        else:
            return False

class Deposit(Transaction):
    def execute(self, user):
        user.balance += self.amount
        user.transactions.append(f"Deposit: ${self.amount} ({self.timestamp})")

class Transfer(Transaction):
    def __init__(self, amount, recipient):
        super().__init__(amount)
        self.recipient = recipient

    def execute(self, user):
        if user.balance >= self.amount:
            user.balance -= self.amount
            self.recipient.balance += self.amount
            user.transactions.append(f"Transfer: ${self.amount} to {self.recipient.user_id} ({self.timestamp})")
            self.recipient.transactions.append(f"Transfer: ${self.amount} from {user.user_id} ({self.timestamp})")
            return True
        else:
            return False

class ATM:
    def __init__(self, bank_name="Octanet"):
        self.users = {}
        self.current_user = None
        self.atm_id = random.randint(1000, 9999)  # Simulating a unique ATM ID
        self.bank_name = bank_name

    def create_account(self, user_id, name, pin, initial_balance=0):
        user = User(user_id, pin, name, initial_balance)
        self.users[user_id] = user
        return user

    def create_multiple_users(self, user_data):
        for user_id, name, pin, initial_balance in user_data:
            self.create_account(user_id, name, pin, initial_balance)

    def authenticate_user(self, user_id, pin):
        if user_id in self.users and self.users[user_id].pin == pin:
            self.current_user = self.users[user_id]
            return True
        return False

    def display_welcome_screen(self):
        print(f"Welcome to {self.bank_name} Bank ATM (ATM ID: {self.atm_id})")

    def display_goodbye_screen(self):
        print(f"Thank you for using {self.bank_name} Bank ATM. Have a great day!")

    def display_transaction_history(self):
        print("\nTransaction History:")
        for transaction in self.current_user.transactions:
            print(transaction)

    def perform_withdrawal(self, amount):
        withdrawal = Withdrawal(amount)
        if withdrawal.execute(self.current_user):
            print(f"Withdrawal successful. {self.current_user.display_balance()}")
            self.display_transaction_history()
        else:
            print("Insufficient funds for withdrawal.")

    def perform_deposit(self, amount):
        deposit = Deposit(amount)
        deposit.execute(self.current_user)
        print(f"Deposit successful. {self.current_user.display_balance()}")
        self.display_transaction_history()

    def perform_transfer(self, amount, recipient_user_id):
        recipient = self.users.get(recipient_user_id)
        if recipient:
            transfer = Transfer(amount, recipient)
            if transfer.execute(self.current_user):
                print(f"Transfer successful. {self.current_user.display_balance()}")
                self.display_transaction_history()
            else:
                print("Insufficient funds for transfer.")
        else:
            print("Recipient not found.")

    def check_balance(self):
        print(self.current_user.display_balance())

def menu():
    print("\nMenu:")
    print("1. View Transaction History")
    print("2. Withdraw")
    print("3. Deposit")
    print("4. Transfer")
    print("5. Balance Inquiry")
    print("6. Quit")



atm = ATM()


user_data = [
    ("1001", "Abhinav", "4321", 15000),
    ("1002", "Rakesh", "5678", 12000),
    ("1003", "Nithin", "9876", 10000),
    ("1004", "Sunil", "5432", 13000),
    ("1005", "Gowtham", "1234", 11000)
]
atm.create_multiple_users(user_data)


atm.display_welcome_screen()


user_id_input = input("Enter User ID: ")
pin_input = input("Enter PIN: ")

if atm.authenticate_user(user_id_input, pin_input):
    print(f"Welcome, {atm.current_user.name}!")

    while True:
        menu()
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            atm.display_transaction_history()
        elif choice == "2":
            withdrawal_amount = float(input("Enter withdrawal amount: "))
            atm.perform_withdrawal(withdrawal_amount)
        elif choice == "3":
            deposit_amount = float(input("Enter deposit amount: "))
            atm.perform_deposit(deposit_amount)
        elif choice == "4":
            recipient_user_id = input("Enter recipient's User ID: ")
            transfer_amount = float(input("Enter transfer amount: "))
            atm.perform_transfer(transfer_amount, recipient_user_id)
        elif choice == "5":
            atm.check_balance()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

else:
    print("Invalid User ID or PIN.")


atm.display_goodbye_screen()
