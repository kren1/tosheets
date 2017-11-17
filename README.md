A simple command line utility that sends your stdin to sheets.

Available on pip by `pip install tosheets` (python3+ only)

***NOTE:***  On first use, tosheets will open a browser window to authorize OAuth2 token.
## Using `tosheets`

Given a google sheets spreadsheet `https://docs.google.com/spreadsheets/d/sample-spread-sheet-id-23sdf32543fs/edit#gid=0`

You can send stdin to the spreadsheet. For example to send sequence from 1 to 10 to a column starting at B4:

```
seq 1 10 | tosheets -c B4 --spreadsheet sample-spread-sheet-id-23sdf32543fs
```

Alternatively to send a matrix 

```
1 2
3 4
```
To the same location:

```
echo '1 2\n3 4' | tosheets -c B4 --spreadsheet=1xF8oFP-QYgPV0AF0dzYSQe9PYj6BWlLanh_0Vc33JFc
```


To sheets has a variety of other options listed:
```
tosheets, send stdin to your google sheets

Usage:
  tosheets -c <cell>  [-s <sheet>] [--spreadsheet=<spreadsheet>] [-d <delimiter>]
  tosheets (-h | --help)
  tosheets --version

Options:
  -h --help                     Prints help.
  --version                     Show version.
  -c CELL                       Start appending to CELL.
  -s SHEET                      Use sheet name SHEET, otherwise tries to use 
                                TOSHEETS_SHEET (default: first visible sheet). 
  -d DELIMITER                  Use DELIMITER to split each line (default: whitespace).
  --spreadsheet=<spreadsheet>   Send to the spreadsheet identified by spreadshetId 
                                (ie. docs.google.com/spreadsheets/d/<spreadsheetId>/...), 
                                if empty uses TOSHEETS_SPREADSHEET enviroment variable.
```

### Distribution
```
python setup.py sdist bdist_wheel
twine upload dist/*
```
