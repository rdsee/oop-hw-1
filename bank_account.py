import uuid
from abc import ABC, abstractmethod


class AccountFrozenError(Exception):
    ...


class AccountClosedError(Exception):
    ...


class InvalidOperationError(Exception):
    ...


class InsufficientFundsError(Exception):
    ...


class AbstractAccount(ABC):
    def __init__(self, wallet_id, name, surname, balance, wallet_status):
        self.wallet_id = wallet_id
        self.name = name
        self.surname = surname
        self._balance = balance
        self._wallet_status = wallet_status

    @abstractmethod
    def deposit(self, amount):
        ...

    @abstractmethod
    def withdraw(self, amount):
        ...

    @abstractmethod
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

        if isinstance(balance, bool) or not isinstance(balance, (int, float)):
            raise InvalidOperationError("Balance must be a number.")
        elif balance != balance:
            raise InvalidOperationError("Balance cannot be NaN.")
        elif balance == float("inf") or balance == float("-inf"):
            raise InvalidOperationError("Balance cannot be inf or -inf.")
        elif balance < 0:
            raise InvalidOperationError("Balance cannot be negative.")

        if wallet_status not in wallet_info:
            raise InvalidOperationError(f"Wallet status '{wallet_status}' is not supported.")

    def __str__(self):
        return (f"account type: BankAccount |"
                f" client: {self.name} {self.surname} |"
                f" last 4 characters of the ID: ...{self.wallet_id[-4:]} |"
                f" status: {self._wallet_status} |"
                f" balance: {self._balance} |"
                f" currency: {self.currency}"
                )

    def get_account_info(self):
        print(f"Your account info: "
              f"1. Name: {self.name}. "
              f"2. Surname: {self.surname}. "
              f"3. wallet-ID: {self.wallet_id}, "
              f"4. Balance: {self._balance}, "
              f"5. Wallet status: {self._wallet_status}, "
              f"6. Currency: {self.currency}"
              )

    def get_balance(self):
        if self._wallet_status == "closed":
            raise AccountClosedError("You cant get your balance when account is closed.")
        elif self._wallet_status == "frozen" or self._wallet_status == "active":
            print(f"Your balance: {self._balance}.")
        else:
            raise InvalidOperationError("Invalid wallet status.")

    def deposit(self, amount):
        if self._wallet_status == "frozen":
            raise AccountFrozenError(f"Your account is frozen. You can not deposit money.")
        elif self._wallet_status == "closed":
            raise AccountClosedError(f"Your account is closed. You can not deposit money.")
        elif self._wallet_status == "active":
            if isinstance(amount, bool) or not isinstance(amount, (int, float)):
                raise InvalidOperationError("Amount must be a number.")
            elif amount != amount:
                raise InvalidOperationError("Amount cannot be NaN.")
            elif amount == float("-inf") or amount == float("inf"):
                raise InvalidOperationError("Amount cannot be inf or -inf.")
            elif amount <= 0:
                raise InvalidOperationError("Amount must be greater than zero.")
            else:
                self._balance += amount
                print(f"Balance deposited. Your balance: {self._balance}.")
        else:
            raise InvalidOperationError("Invalid wallet status.")

    def withdraw(self, amount):
        if self._wallet_status == "frozen":
            raise AccountFrozenError(f"Your account is frozen. You can not withdraw money.")

        elif self._wallet_status == "closed":
            raise AccountClosedError(f"Your account is closed. You can not withdraw money.")

        elif self._wallet_status == "active":
            if isinstance(amount, bool) or not isinstance(amount, (int, float)):
                raise InvalidOperationError("Amount must be a number.")
            elif amount != amount:
                raise InvalidOperationError("Amount cannot be NaN.")
            elif amount == float("-inf") or amount == float("inf"):
                raise InvalidOperationError("Amount cannot be inf or -inf.")
            elif amount <= 0:
                raise InvalidOperationError("Amount must be greater than zero.")
            elif amount > self._balance:
                raise InsufficientFundsError("Amount cannot be greater than balance.")
            else:
                self._balance -= amount
                print(f"Balance withdrawn. Your balance: {self._balance}.")
        else:
            raise InvalidOperationError("Invalid wallet status.")


if __name__ == "__main__":
    account = BankAccount(
        name="Anna",
        surname="Brown",
        balance=100,
        wallet_status="active",
        currency="USD"
    )

    account2 = BankAccount(
        name="Petr",
        surname="Bobrov",
        balance=40.34,
        wallet_status="closed",
        currency="RUB"
    )

    try:
        account3 = BankAccount(
            name="Tom",
            surname="Cock",
            balance=100,
            wallet_status="frozen",
            currency="KZT"
        )
    except InvalidOperationError as e:
        print(e)

    try:
        account4 = BankAccount(
            name="Tim",
            surname="bobs",
            balance=230,
            wallet_status="unsupported",
            currency="CNY"
        )
    except InvalidOperationError as e:
        print(e)


    account.get_account_info()
    account2.get_account_info()

    try:
        account2.deposit(100)
    except AccountClosedError as e:
        print(e)

    try:
        account.withdraw(300)
    except InsufficientFundsError as e:
        print(e)

    try:
        account.withdraw(0)
    except InvalidOperationError as e:
        print(e)

    try:
        account.deposit(-23)
    except InvalidOperationError as e:
        print(e)

    account.deposit(200)
    account.get_balance()
    account.withdraw(20.5)
    account.get_balance()

    try:
        account3.deposit(100)
    except AccountFrozenError as e:
        print(e)











