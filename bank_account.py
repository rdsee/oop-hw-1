import uuid
class AccountFrozenError(Exception):
    ...
class AccountClosedError(Exception):
    ...
class InvalidOperationError(Exception):
    ...
class InsufficientFundsError(Exception):
    ...

class AbstractAccount:
    def __init__(self, wallet_id, name, surname, balance, wallet_status):
        self.wallet_id = wallet_id
        self.name = name
        self.surname = surname
        self._balance = balance
        self.wallet_status = wallet_status

    def deposit(self, amount):
        ...
    def withdraw(self, amount):
        ...
    def get_account_info(self):
        ...

class BankAccount(AbstractAccount):
    def __init__(self, wallet_id=None, name=None, surname=None, balance=0, wallet_status=None, currency=None):
        super().__init__(wallet_id, name, surname, balance, wallet_status)
        self.currency = currency

        allowed_currency = ("RUB", "USD", "EUR", "KZT", "CNY")
        wallet_info = ("active", "frozen", "closed")

        if self.wallet_id is None:
            self.wallet_id = uuid.uuid4().hex[:6]

        if currency not in allowed_currency:
            raise InvalidOperationError(f"Currency {currency} is not supported.")

        if self.name is None:
            raise InvalidOperationError("Name cannot be None.")

        if self.surname is None:
            raise InvalidOperationError("Surname cannot be None.")

        if balance < 0:
            raise InvalidOperationError("Balance cannot be negative.")

        if wallet_status not in wallet_info:
            raise InvalidOperationError(f"Wallet status {wallet_status} is not supported.")

    def __str__(self):
        return (f"account type: BankAccount |"
                f" client: {self.name} {self.surname} |"
                f" last 4 characters of the ID: ...{self.wallet_id[-4:]} |"
                f" status: {self.wallet_status} |"
                f" balance: {self._balance} |"
                f" currency: {self.currency}"
                )
    def get_account_info(self):
        print(f"Your account info: "
              f"1. Name: {self.name}. "
              f"2. Surname: {self.surname}. "
              f"3. wallet-ID: {self.wallet_id}, "
              f"4. Balance: {self._balance}, "
              f"5. Wallet status: {self.wallet_status}, "
              f"6. Currency: {self.currency}"
        )

    def get_balance(self):
        if self.wallet_status == "closed":
            raise AccountClosedError("You cant get your balance when account is closed.")
        else:
            print(f"Your balance: {self._balance}.")

    def deposit(self, amount):
        if self.wallet_status == "frozen":
            raise AccountFrozenError(f"Your account is frozen. You can not deposit money.")
        elif self.wallet_status == "closed":
            raise AccountClosedError(f"Your account is closed. You can not deposit money.")
        elif amount <= 0:
            raise InvalidOperationError("Amount must be greater than zero.")
        self._balance += amount
        print(f"Balance deposited. Your balance: {self._balance}.")

    def withdraw(self, amount):
        if self.wallet_status == "frozen":
            raise AccountFrozenError(f"Your account is frozen. You can not withdraw money.")
        elif self.wallet_status == "closed":
            raise AccountClosedError(f"Your account is closed. You can not withdraw money.")
        elif amount <= 0:
            raise InvalidOperationError("Amount must be greater than zero.")
        elif amount > self._balance:
            raise InsufficientFundsError("Amount cannot be greater than balance.")
        else:
            self._balance -= amount
            print(f"Balance withdrawn. Your balance: {self._balance}.")

account = BankAccount(
    name="Anna",
    surname="Brown",
    balance=100,
    wallet_status="active",
    currency="USD"
)

print(account.name)
print(account.surname)
account.deposit(100)
account.get_balance()
account.get_account_info()
account.withdraw(30)
account.get_balance()
account.get_account_info()

account2 = BankAccount(
    name="Petr",
    surname="Bobrov",
    balance=40,
    wallet_status="closed",
    currency="RUB"
)

print(account2.name)
print(account2.surname)
print(account2)

account3 = BankAccount(
    name="Tom",
    surname="Cock",
    balance=1020,
    wallet_status="frozen",
    currency="KZT"
)

print(account3.name)
print(account3.surname)
account3.deposit(100)
print(account3)
