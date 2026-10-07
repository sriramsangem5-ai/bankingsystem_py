import os
import random

import MySQLdb


class bank:

    def __init__(self):

        self.con = MySQLdb.connect(
            host="localhost",
            user="root",
            password=os.environ["BANKING_DB_PASSWORD"]
        )

        self.cur = self.con.cursor()

        self.cur.execute("CREATE DATABASE IF NOT EXISTS banking")

        self.cur.execute("USE banking")

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_no BIGINT PRIMARY KEY,
                holder_name VARCHAR(100),
                mobile VARCHAR(10),
                aadhar VARCHAR(12),
                account_type VARCHAR(20),
                balance DOUBLE
            )
        """)

        self.con.commit()


    def create_account(self):

        holder_name = input("Enter holder name: ")

        mobile = input("Enter mobile number: ")

        aadhar = input("Enter Aadhar number: ")


        # Mobile validation without re

        if len(mobile) != 10 or not mobile.isdigit():

            print("Invalid mobile number")

            return

        if mobile[0] not in "6789":

            print("Invalid mobile number")

            return


        # Aadhar validation without re

        if len(aadhar) != 12 or not aadhar.isdigit():

            print("Invalid Aadhar number")

            return


        account_type = input(
            "Enter account type (saving/zero): "
        ).lower()


        # Generate account number

        account_no = random.randint(
            1000000000,
            9999999999
        )


        if account_type == "saving":

            try:

                balance = float(
                    input("Enter initial deposit: ")
                )

            except ValueError:

                print("Please enter a valid amount")

                return


            if balance < 1000:

                print("Minimum deposit should be 1000")

                return


        elif account_type == "zero":

            balance = 0


        else:

            print("Invalid account type")

            return


        query = """
        INSERT INTO accounts
        (account_no, holder_name, mobile, aadhar, account_type, balance)
        VALUES (%s, %s, %s, %s, %s, %s)
        """


        values = (
            account_no,
            holder_name,
            mobile,
            aadhar,
            account_type,
            balance
        )


        try:

            self.cur.execute(query, values)

            self.con.commit()

            print("\nAccount created successfully")

            print("Your account number:", account_no)


        except MySQLdb.Error as e:

            self.con.rollback()

            print("Database error:", e)


    def deposit(self):

        try:

            account_no = int(
                input("Enter account number: ")
            )

            amount = float(
                input("Enter deposit amount: ")
            )

        except ValueError:

            print("Please enter valid numbers")

            return


        if amount <= 0:

            print("Deposit amount must be greater than 0")

            return


        query = """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_no = %s
        """


        self.cur.execute(
            query,
            (amount, account_no)
        )

        self.con.commit()


        if self.cur.rowcount > 0:

            print("Amount deposited successfully")

        else:

            print("Account not found")


    def withdraw(self):

        try:

            account_no = int(
                input("Enter account number: ")
            )

            amount = float(
                input("Enter withdrawal amount: ")
            )

        except ValueError:

            print("Please enter valid numbers")

            return


        if amount <= 0:

            print("Withdrawal amount must be greater than 0")

            return


        query = """
        SELECT balance
        FROM accounts
        WHERE account_no = %s
        """


        self.cur.execute(
            query,
            (account_no,)
        )


        result = self.cur.fetchone()


        if result:

            balance = result[0]


            if amount <= balance:

                query = """
                UPDATE accounts
                SET balance = balance - %s
                WHERE account_no = %s
                """


                self.cur.execute(
                    query,
                    (amount, account_no)
                )

                self.con.commit()

                print("Amount withdrawn successfully")


            else:

                print("Insufficient balance")


        else:

            print("Account not found")


    def check_balance(self):

        try:

            account_no = int(
                input("Enter account number: ")
            )

        except ValueError:

            print("Invalid account number")

            return


        query = """
        SELECT balance
        FROM accounts
        WHERE account_no = %s
        """


        self.cur.execute(
            query,
            (account_no,)
        )


        result = self.cur.fetchone()


        if result:

            print("Current balance:", result[0])

        else:

            print("Account not found")


    def account_details(self):

        try:

            account_no = int(
                input("Enter account number: ")
            )

        except ValueError:

            print("Invalid account number")

            return


        query = """
        SELECT *
        FROM accounts
        WHERE account_no = %s
        """


        self.cur.execute(
            query,
            (account_no,)
        )


        result = self.cur.fetchone()


        if result:

            print("\n----- ACCOUNT DETAILS -----")

            print("Account Number :", result[0])
            print("Holder Name    :", result[1])
            print("Mobile         :", result[2])
            print("Aadhar         :", result[3])
            print("Account Type   :", result[4])
            print("Balance        :", result[5])


        else:

            print("Account not found")


    def menu(self):

        while True:

            print("\n========== BANKING APPLICATION ==========")

            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Account Details")
            print("6. Exit")


            choice = input("Enter your choice: ")


            if choice == "1":

                self.create_account()


            elif choice == "2":

                self.deposit()


            elif choice == "3":

                self.withdraw()


            elif choice == "4":

                self.check_balance()


            elif choice == "5":

                self.account_details()


            elif choice == "6":

                print("Thank you for using Banking Application")

                break


            else:

                print("Invalid choice")


# Create object

obj = bank()

# Start application

obj.menu()