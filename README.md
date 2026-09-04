# Affinity Answers Data Engineer Intern Assignment

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql&logoColor=white)
![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?logo=gnubash&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Debian%20%7C%20Ubuntu%20%7C%20WSL-lightgrey)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

This repository contains solutions for the Affinity Answers Data Engineer Intern assignment. The work is organized by assignment area: Python, SQL, and Unix shell scripting.

## Table of Contents

- [Assignment Coverage](#assignment-coverage)
- [Video Demonstration](#video-demonstration)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Python Setup and Run](#python-setup-and-run)
- [SQL Setup and Run with DBeaver](#sql-setup-and-run-with-dbeaver)
- [Unix Shell Scripting Setup and Run](#unix-shell-scripting-setup-and-run)
- [Notes](#notes)

## Assignment Coverage

| Assignment area | Solution file | Summary |
| --- | --- | --- |
| Question 1: Python | `python/scraper.py` | Scrapes MDComputers search results for a user-provided search term and writes structured product data to JSON. |
| Question 2: SQL and databases | `sql/question1.sql`, `sql/question2.sql`, `sql/question3.sql` | Contains SQL queries for the public Rfam MySQL dataset. |
| Question 3: Unix shell scripting | `unix_shell_scripting/csv_parser.sh` | Downloads a company CSV from a URL, extracts company name, location, and founding year, then sorts by founding year. |

## Video Demonstration

Demo video link: https://drive.google.com/file/d/1rgCpwu1J4ykt07jM7Wwgv4p_ENa0PqHn/view?usp=sharing

The video demonstration will show the execution of:

- The Python scraper in `python/scraper.py`
- The SQL queries from the `sql/` folder using DBeaver
- The Unix shell script in `unix_shell_scripting/csv_parser.sh`

## Repository Structure

```text
.
|-- python/
|   `-- scraper.py
|-- sql/
|   |-- question1.sql
|   |-- question2.sql
|   `-- question3.sql
|-- unix_shell_scripting/
|   `-- csv_parser.sh
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Prerequisites

- Git
- Python 3.10.20 or a compatible Python 3.10+ version
- Internet access for the MDComputers website, the Rfam public MySQL database, and the company CSV URL
- DBeaver or another MySQL client for running the SQL queries
- A Debian, Ubuntu, or WSL environment
- Shell utilities: `bash`, `curl`, `gawk`, `sort`, and `column`

## Python Setup and Run

Install Python, Git, and virtual environment support on Debian, Ubuntu, or WSL:

```bash
sudo apt update
sudo apt install git python3 python3-pip python3-venv
```

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/Jaymin151617/affinity-answers-de-assignment.git
cd affinity-answers-de-assignment

python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Run the scraper:

```bash
python3 python/scraper.py
```

When prompted, enter a product search term, for example:

```text
Enter search term: external hard disk
```

The script writes the result to `python/products.json`. The JSON output includes the search URL, the expected number of products reported by the site, the number of unique products scraped, and a list of product records.

The product records include:

- Product ID
- Product name
- Current price
- Original price, when available
- Discount percentage, when available
- Product page link
- Product image URL

## SQL Setup and Run with DBeaver

The SQL answers are written for the public read-only Rfam MySQL database. Rfam's public database documentation lists these connection details:

| Setting | Value |
| --- | --- |
| Database type | MySQL |
| Host | `mysql-rfam-public.ebi.ac.uk` |
| Port | `4497` |
| Database | `Rfam` |
| Username | `rfamro` |
| Password | Leave blank / none |

To run the SQL files in DBeaver:

1. Open DBeaver and create a new MySQL connection.
2. Enter the host, port, database, username, and blank password shown above.
3. Download the MySQL driver if DBeaver prompts for it.
4. Test the connection.
5. Open a SQL editor for the Rfam connection.
6. Open and execute the queries from the `sql/` folder:
   - `sql/question1.sql`
   - `sql/question2.sql`
   - `sql/question3.sql`

The SQL files include comments describing the question being answered. Some answers may vary if the public Rfam database is updated after the queries were originally run.

Official Rfam database documentation: https://docs.rfam.org/en/latest/database.html

## Unix Shell Scripting Setup and Run

The shell script requires GNU awk because it uses `FPAT` to parse CSV fields. Make sure the required command-line tools are available:

```bash
command -v bash
command -v curl
command -v gawk
command -v sort
command -v column
```

On Debian, Ubuntu, or WSL, install missing tools with:

```bash
sudo apt update
sudo apt install curl gawk util-linux
```

On some Linux versions, `column` may be provided by `bsdextrautils` instead of `util-linux`.

If the script is not executable yet, grant execute permission:

```bash
chmod +x unix_shell_scripting/csv_parser.sh
```

Run the script with the company CSV URL from the assignment:

```bash
./unix_shell_scripting/csv_parser.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
```

The script prints a table with:

- Company Name
- Location
- Founding Year

The rows are sorted by founding year in ascending order.

If you get a `cannot execute: required file not found` error, the script may have Windows-style CRLF line endings. Convert it to Unix-style LF line endings with:

```bash
sed -i 's/\r$//' unix_shell_scripting/csv_parser.sh
```

Then run the script again.

## Notes

- The Python scraper depends on the current HTML structure of MDComputers. If the site changes its markup, selectors in `python/scraper.py` may need to be updated.
- The Unix script validates the expected CSV column positions before printing output.
- The Rfam database is public and read-only, and it may be updated by Rfam over time.
