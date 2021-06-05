#!/usr/bin/env python3
"""
betterment2bean.py - Converts Betterment transactions CSV file to a Beancount-compatible ledger file.

Usage: python3 betterment2bean.py <betterment.csv> [ledger.beancount]

See README.md in project repo for more information: https://github.com/garrettheath4/betterment2bean
"""

import sys
import re
import csv

EQ_OPENING_BALANCES = "Equity:Opening-Balances          "
INCOME_PAYCHECK = "Income:Paycheck                  "

account_mapping = {
    # 2018-07-16 open Assets:401k:Roth:Betterment       USD
    # 2018-07-16 open Assets:401k:Trad:Betterment       USD
    # 2020-06-02 open Assets:Invest:Personal:Betterment USD
    # 2020-06-02 open Assets:Savings:TDBank             USD
    # 2020-06-02 open Assets:Savings:OneFin:SavePocket  USD
    # 2021-05-03 open Assets:Savings:OneFin:AutoSavePkt USD
    # 2019-11-01 open Assets:Stock:Square
    # 2019-11-01 open Assets:Stock:Square:Apple         AAPL
    # 2019-11-01 open Assets:Stock:Square:Disney        DIS
    # 2019-11-01 open Assets:Stock:Square:Shopify       SHOP
    # 2020-02-02 open Assets:Crypto:Square
    # 2020-02-02 open Assets:Crypto:Square:Bitcoin      BTC
    # 2020-02-02 open Assets:Crypto:Square:Ethereum     ETH
    # 2020-02-02 open Assets:Crypto:Square:Dogecoin     DOGE
    # 2018-07-01 open Equity:Opening-Balances
    "Roth 401(k)": "Assets:401k:Roth:Betterment      ",
    "Traditional 401(k)": "Assets:401k:Trad:Betterment      ",
    "Garrett's Personal Account": "Assets:Invest:Personal:Betterment",
}

source_mapping = {
    "Catalist, LLC 401(k) Plan Conversion": EQ_OPENING_BALANCES,
    "Deposit from ******2593": EQ_OPENING_BALANCES,
    "Automatic Deposit": INCOME_PAYCHECK,
    "Advisory Fee": "Expenses:Invest:Fee              ",
    "Dividend Reinvestment": "Income:Dividend                  ",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: betterment2bean.py <betterment.csv> [ledger.beancount]")
        sys.exit(9)
    in_filename = sys.argv[1]
    if len(sys.argv) < 3:
        if '.' in in_filename:
            out_filename = re.sub(r'\..+', ".beancount", in_filename)
        else:
            out_filename = in_filename + ".beancount"
    else:
        out_filename = sys.argv[2]

    with open(in_filename, 'r') as f_in:
        with open(out_filename, 'w') as f_out:
            f_out.write('option "title" "Garrett Heath Koller Personal"\n')
            f_out.write('option "operating_currency" "USD"\n\n')

            for src in source_mapping.values():
                f_out.write(f'2014-01-01 open {src} USD\n')

            f_out.write('\n')

            csv_reader = csv.DictReader(f_in, dialect='unix')
            for row in csv_reader:
                tx_acct = row['Account Name']
                if tx_acct in account_mapping:
                    account_name = account_mapping[tx_acct]
                else:
                    raise ValueError(f"Unexpected Account Name: {tx_acct}")
                tx_desc = row['Transaction Description']
                if tx_desc.startswith("Initial Allocation"):
                    # 2018-07-16 open Assets:401k:Roth:Betterment       USD
                    tx_date = row['Date Completed'][:10]
                    f_out.write(f'{tx_date} open {account_name} USD\n\n')
                    continue
                elif tx_desc.startswith("Deposit from "):
                    source_name = EQ_OPENING_BALANCES
                elif tx_desc.startswith("Portfolio Update") or tx_desc == "Rebalance":
                    continue
                elif "Payroll Contribution" in tx_desc:
                    source_name = INCOME_PAYCHECK
                elif tx_desc in source_mapping:
                    source_name = source_mapping[tx_desc]
                else:
                    raise ValueError(f"Unexpected Transaction Description: {tx_desc}")
                # "2021-06-03 10:29:50 -0400"[:10] = "2021-06-03"
                tx_date = row['Date Completed'][:10]
                tx_amnt = float(row['Amount'])
                f_out.write(f'{tx_date} * "{tx_desc}"\n  {account_name} {tx_amnt:10.2f} USD\n'
                            + f'  {source_name} {-tx_amnt:10.2f} USD\n\n')
                # tx_bal = row['Ending Balance']
                # f_out.write(f'{tx_date} balance {account_name} {tx_bal}\n\n')


if __name__ == "__main__":
    main()
