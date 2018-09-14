A simple command line utility that sends your stdin to sheets.

Available on pip by `pip install tosheets` (python3+ only)

***NOTE:***  On first use, tosheets will open a browser window to authorize OAuth2 token.
## Using `tosheets`
Pipe a local file to a new spreadsheet.
```
cat data.csv | tosheets -c A1 --new-sheet="tosheetsSheet"
```

Pipe a local file to an existing spreadsheet:
(Given a URL like `https://docs.google.com/spreadsheets/d/sample-spread-sheet-id-23sdf32543fs/edit#gid=0`)
```
cat data.csv | tosheets -c B4 --spreadsheet=sample-spread-sheet-id-23sdf32543fs
```

Send sequence from 1 to 10 to a column starting at B4:
```
seq 1 10 | tosheets -c B4 --spreadsheet=sample-spread-sheet-id-23sdf32543fs
```

Send a matrix:
```
1 2
3 4
```
To the same location:

```
echo -e '1 2\n3 4' | tosheets -c B4 --spreadsheet=sample-spread-sheet-id-23sdf32543fs
```


To sheets has a variety of other options listed:
```
tosheets, send stdin to your google sheets

Usage:
  tosheets -c <cell> [-u] [-s <sheet>] [--spreadsheet=<spreadsheet>] [--new-sheet=<name>] [-d <delimiter>]
  tosheets (-h | --help)
  tosheets --version

Options:
  -h --help                     Prints help.
  --version                     Show version.
  -u                            Update CELL(s) instead of appending.
  -c CELL                       Start appending to CELL.
  -s SHEET                      Use sheet name SHEET, otherwise tries to use
                                TOSHEETS_SHEET (default: first visible sheet).
  -d DELIMITER                  Use DELIMITER to split each line (default: whitespace).
  --spreadsheet=<spreadsheet>   Send to the spreadsheet identified by spreadshetId
                                (ie. docs.google.com/spreadsheets/d/<spreadsheetId>/...).
                                Falls back to TOSHEETS_SPREADSHEET enviroment variable,
                                or creates a new sheet if both are empty.
  --new-sheet=<name>            Create a new spreadsheet with the chosen name. Prints the
                                spreadsheetId so it can be piped/stored.
```

### Distribution
```
python setup.py sdist bdist_wheel
twine upload dist/*
```
