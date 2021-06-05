Betterment to Bean (betterment2bean.py)
=======================================

`betterment2bean.py` is a simple Python script that converts transaction CSV files downloaded from a [Betterment]
investment, checking, or 401k account to a plaintext ledger file that is readable by [Beancount]. 

Beancount is open source command-line accounting software that stores your financial transaction data in structured but
human-readable plain text files.

Betterment is an investment and robo-advisor platform that automatically invests and diversifies money that you deposit
into your account with them.


Installation and Usage
----------------------

Nothing fancy here installation-wise. Just clone this repo (or download the Python script itself). Once you have it, you
can open a terminal window, `cd` to the directory that contains the `betterment2bean.py` file, and run:

    python3 betterment2bean.py betterment.csv ledger.beancount

where `betterment.csv` is a CSV file downloaded from a Betterment account and `ledger.beancount` is the filename you
want to save the Beancount ledger file as. If the `ledger.beancount` argument is omitted then the ledger file will be
saved with the same name as the input CSV file (`betterment.csv`) but with the `.beancount` extension instead (e.g.
`betterment.beancount`). 


File Formats
------------

Betterment CSV files are expected to be in this format:

```csv
Goal Name,Account Name,Transaction Description,Amount,Ending Balance,Date Created,Date Completed
"Catalist, LLC Traditional 401(k)",Traditional 401(k),5/28/2021 Payroll Contribution,115.88,19848.98,2021-05-28 04:06:51 -0400,2021-06-03 10:29:50 -0400
```


See Also
--------

* Similar project: [banks2ledger] 
* More information about plaintext accounting software options [here][pta].



<!-- Links -->
[Betterment]: https://www.betterment.com
[Beancount]: https://beancount.github.io
[banks2ledger]: https://github.com/tomszilagyi/banks2ledger
[pta]: https://plaintextaccounting.org
