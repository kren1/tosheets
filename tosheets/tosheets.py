#!/usr/bin/python3
doc = """tosheets, send stdin to your google sheets

Usage:
  tosheets -c <cell> [-u] [-k] [-s <sheet>] [--spreadsheet=<spreadsheet>] [--new-sheet=<name>] [-d <delimiter>] [-q <quote char>]
  tosheets (-h | --help)
  tosheets --version

Options:
  -h --help                     Prints help.
  --version                     Show version.
  -u                            Update CELL(s) instead of appending.
  -k                            Keep fields as they are (do not try to convert int or float).
  -c CELL                       Start appending to CELL.
  -s SHEET                      Use sheet name SHEET, otherwise tries to use
                                TOSHEETS_SHEET (default: first visible sheet).
  -d DELIMITER                  Use DELIMITER to split each line (default: whitespace).
  -q QUOTE_CHAR                 A one-character string used to quote fields containing special characters,
                                such as the delimiter or quotechar, or which contain new-line characters.
                                (default: '"').
  --spreadsheet=<spreadsheet>   Send to the spreadsheet identified by spreadshetId
                                (ie. docs.google.com/spreadsheets/d/<spreadsheetId>/...),
                                if empty uses TOSHEETS_SPREADSHEET enviroment variable.
  --new-sheet=<name>            Create a new spreadsheet with the chosen name. Prints the
                                spreadsheetId so it can be piped/stored.
"""
import httplib2
import os
import re
import sys
import csv

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from docopt import docopt

import pkg_resources

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = pkg_resources.resource_filename(__name__, "client.json")
APPLICATION_NAME = 'tosheets'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-tosheets.json')

    store = Storage(credential_path)
    credentials = store.get()
    sys.argv = ['']
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

# creates a new sheet with the chosen Name
def newSheet(name):
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                  'version=v4')
  service = discovery.build('sheets', 'v4', http=http,
                            discoveryServiceUrl=discoveryUrl)

  sheet = {
    'properties'  : {
      'autoRecalc': 'ON_CHANGE',
      'title': name,
      'locale': 'en_US',
      'timeZone': 'America/New_York'
    },
    'sheets'    : [{
      'properties'  : {
        'gridProperties': {'columnCount':26,'rowCount':200},
        'index': 0,
        'sheetId': 0,
        'sheetType': 'GRID',
        'title': 'tosheets'
      }
    }]
  }

  try:
        result = service.spreadsheets().create(body=sheet).execute()
        spreadsheetId = result['spreadsheetId']
        print(spreadsheetId)
        return spreadsheetId
  except Exception as e:
        print(e)
        exit(1)


# appendToSheet that updates instead of appending, should retain virtually identical semantics
def updateSheet(values, spreadsheetId, rangeName):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheetId, range=rangeName,
            valueInputOption='RAW', body = {'values': values}).execute()
    except Exception as e:
        print(e)
        exit(1)
    exit(0)

def appendToSheet(values, spreadsheetId, rangeName):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range=rangeName,
            valueInputOption='RAW', body = {'values': values}).execute()
    except Exception as e:
        print(e)
        exit(1)
    exit(0)

def tryToConvert(x):
  try:
     return int(x)
  except ValueError:
    try:
      return float(x)
    except ValueError:
      return x.strip()

def dummyConvert(x):
    return x.strip()

# If the given ID looks like a full URL instead of an ID, extract the ID
def canonicalizeSpreadsheetId(spreadsheetId):
    match = re.match('^https?://docs.google.com/spreadsheets/d/([^/]+)', spreadsheetId)
    if match:
        return match.groups()[0]

    return spreadsheetId

def main():
    version = pkg_resources.require('tosheets')[0].version
    arguments = docopt(doc, version='tosheets ' + str(version))

    spreadsheetId = arguments['--spreadsheet']
    newSheetName = arguments['--new-sheet']

    if spreadsheetId:
        spreadsheetId = canonicalizeSpreadsheetId(spreadsheetId)

    if spreadsheetId is None and newSheetName is None:
        if not "TOSHEETS_SPREADSHEET" in os.environ:
            print("TOSHEETS_SPREADSHEET is not set and --spreadsheet was not given")
            exit(1)
        spreadsheetId = os.environ['TOSHEETS_SPREADSHEET']

    if newSheetName is not None:
      spreadsheetId = newSheet(newSheetName)

    cell = arguments['-c']
    sheet = arguments['-s']

    if sheet is None:
        if not "TOSHEETS_SHEET" in os.environ:
          sheet = ""
        else:
          sheet = os.environ['TOSHEETS_SHEET'] + "!"
    else:
        sheet += "!"

    separator = arguments['-d'] or ' '
    quote = arguments['-q'] or '"'
    keep = arguments['-k']
    reader = csv.reader(sys.stdin, delimiter=separator, quotechar=quote)

    values = []
    for line in reader:
        values.append(list(map(dummyConvert if keep else tryToConvert, line)))

    update = arguments['-u']
    if update is False:
      appendToSheet(values, spreadsheetId, sheet + cell)
    else:
      updateSheet(values, spreadsheetId, sheet + cell)

if __name__ == '__main__':
    main()

