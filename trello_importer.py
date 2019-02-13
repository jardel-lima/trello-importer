# coding: utf-8
import sys
import requests
import json
import copy
import datetime
import webbrowser

CONF_FOLDER = 'conf/'
CONF_FILE = 'trello_importer.config'
API_KEY = ''
TOKEN = ''
SECRET = ''
ORGANIZATION_ID = ''
SPLIT_CHAR = '\t'
INPUT_FILE = 'file.csv'

API_KEY = ''


class Label:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.id = ''


LABELS = {
        'DOING': Label('yellow', 'DOING'),
        'MELHORIAS': Label('purple', 'MELHORIAS'),
        'TO DO': Label('blue', 'TO DO'),
        'ABORTED': Label('red', 'ABORTED'),
        'IMPEDIMENTO': Label('red', 'IMPEDIMENTO'),
        'DONE': Label('green', 'DONE'),
        'PUBLISHED': Label('orange', 'PUBLISHED'),
        'USER STORY': Label('black', 'USER STORY'),
        'VALIDADO': Label('sky', 'VALIDADO'),
        'BUGS': Label('pink', 'BUGS')
    }


class Board:
    name = ''
    id = ''
    lists = []
    completed = 0.0
    total_cards = 0

    def __init__(self, name):
        self.name = name

    def append_list(self, list):
        self.lists.append(copy.copy(list))

    def total_cards(self):
        count = 0
        for list in self.lists:
            count += len(list.cards)
        self.total_cards = count


class List:
    name = ''
    id = ''
    cards = []

    def __init__(self, name):
        self.name = name
        del self.cards[:]


class Card:
    name = ''
    time = ''
    description = ''

    def __init__(self, name='', time='', description=''):
        self.name = name
        self.time = time
        self.description = description


def get_token():
    global TOKEN
    url = 'https://trello.com/1/authorize?' \
          'expiration=1hour&' \
          'name=Trello Importer&' \
          'scope=read,write&' \
          'response_type=token&key={}'.format(API_KEY)
    print('-Opening confirmation Page!')
    webbrowser.open_new_tab(url)
    TOKEN = raw_input('-Please paste your TOKEN:')


def get_trello_conf():
    print('-Reading Trello config file!')
    global API_KEY, TOKEN, SECRET, ORGANIZATION_ID
    try:
        with open(CONF_FOLDER + CONF_FILE, 'r') as file:
            for line in file:
                aux = line.split('=')
                if aux[0] == 'API_KEY':
                    API_KEY = aux[1].strip()
                elif aux[0] == 'TOKEN':
                    TOKEN = aux[1].strip()
                elif aux[0] == 'SECRET':
                    SECRET = aux[1].strip()
                elif aux[0] == 'ORGANIZATION_ID':
                    ORGANIZATION_ID = aux[1].strip()
    except Exception as ex:
        print('Error: Could not read configuration file!')
        print('Error: ' + ex.message)
        exit(1)

    if API_KEY == '':
        print('API_KEY was not found!')
        exit(1)


def read_csv(file_name):
    print('-Reading file to import!')
    try:
        with open(file_name, 'r') as file:
            count_line = 0
            list = None
            cards = []
            for line in file:

                if len(line) == 0:
                    continue

                if count_line == 0:
                    board_name = line.split(SPLIT_CHAR)[1].strip()
                    board = Board(board_name)

                elif count_line > 1:
                    aux = line.split(SPLIT_CHAR)
                    if len(aux[0]) > 0:
                        if list:
                            list.cards = copy.copy(cards)
                            board.append_list(list)
                            del cards[:]
                            del list
                        list_name = aux[0]
                        list = List(list_name)

                    if len(aux) > 1:
                        card = Card()
                        card.name = aux[1].strip()
                        if len(card.name) > 0:
                            if len(aux) > 2:
                                card.description = aux[2].strip()
                            if len(aux) > 3:
                                card.time = aux[3].strip()
                            cards.append(card)

                count_line += 1
            if list:
                list.cards = copy.copy(cards)
                board.append_list(list)

    except Exception as ex:
        print('Error: Could not read CSV file: {}!'.format(file_name))
        print('Error: ' + ex.message)
        exit(1)

    return board


def board_exists(board):
    print('-Checking if board {} exists'.format(board.name))
    try:
        url = 'https://api.trello.com/1/boards/{0}?key={1}&token={2}'.format(board.name, API_KEY, TOKEN)
        response = requests.request("GET", url)

        if response.ok:
            board.id = board.name
            return True
        else:
            return False
    except Exception as ex:
        return False


def create_board(board):
    global PARAMS
    try:
        if not board_exists(board):
            print('-Creating Board: {}!'.format(board.name))

            url = 'https://api.trello.com/1/boards/?key={0}&token={1}'.format(API_KEY, TOKEN)

            params = {'name': board.name,
                      'keepFromSource': 'none',
                      'prefs_voting': 'disabled',
                      'prefs_comments': 'members',
                      'prefs_permissionLevel': 'private',
                      'prefs_invitations': 'admins',
                      'prefs_selfJoin': 'true',
                      'defaultLabels': 'false',
                      'defaultLists': 'false'}

            if len(ORGANIZATION_ID.strip()) > 0:
                params['idOrganization'] = ORGANIZATION_ID
                params['prefs_permissionLevel'] = 'org',

            response = requests.request("POST", url, params=params)

            if response.ok:
                board.id = json.loads(response.text)['id']
            else:
                print('Error: Could not create Board '+board.name+'!')
                print('Error: ' + response.text)
                exit(1)

        create_labels(board.id)
        for list in board.lists:
            create_list(list, board)

    except Exception as ex:
       print('Error: '+ex.message)
       exit(1)


def create_labels(board_id):
    global PARAMS
    print('--Creating Labels!')
    try:

        for label in LABELS.values():
            url = 'https://api.trello.com/1/labels/?key={0}&token={1}'.format(API_KEY, TOKEN)

            params = {'name': label.name,
                      'color': label.color,
                      'idBoard': board_id}

            response = requests.request("POST", url, params=params)
            if response.ok:
                label.id = json.loads(response.text)['id']
            else:
                print('Error: Could not create Label '+list.name+'!')
                print('Error: ' + response.text)
                exit(1)

    except Exception as ex:
        print('Error: '+ex.message)


def create_list(list, board):
    global PARAMS
    print('--Creating List: {}!'.format(list.name))
    try:
        url = 'https://api.trello.com/1/lists/?key={0}&token={1}'.format(API_KEY, TOKEN)

        params = {'name': list.name,
                  'idBoard': board.id}

        response = requests.request("POST", url, params=params)
        if response.ok:
            list.id = json.loads(response.text)['id']
        else:
            print('Error: Could not create List '+list.name+'!')
            print('Error: ' + response.text)
            exit(1)

        for card in list.cards:
            create_card(card, list.id, board)

    except Exception as ex:
        print('Error: '+ex.message)


def create_card(card, list_id, board):
    global PARAMS
    print('---Creating Card: {}! {:4.2f}%'.format(card.name, (board.completed/float(board.total_cards))*100))
    try:
        url = 'https://api.trello.com/1/cards/?key={0}&token={1}'.format(API_KEY, TOKEN)
        card_name = '({1}) {0}'.format(card.name, card.time) if card.time.isdigit() else '{0}'.format(card.name)
        params = {
                  'name': card_name,
                  'pos': 'bottom',
                  'desc': card.description,
                  'idList': list_id,
                  'keepFromSource': 'all',
                  'idLabels': LABELS['TO DO'].id
                }

        response = requests.request("POST", url, params=params)
        if not response.ok:
            print('Error: Could not create Card ' + card.name + '!')
            print('Error: '+response.text)
            exit(1)

        board.completed += 1

    except Exception as ex:
        print('Error: '+ex.message)
        exit(1)


def main():
    print("###Trello Importer!###\n")

    if len(sys.argv) < 2:
        input_file = INPUT_FILE
    else:
        input_file = sys.argv[1]

    get_trello_conf()
    get_token()
    begin = datetime.datetime.now()
    board = read_csv(input_file)
    board.total_cards()
    create_board(board)
    end = datetime.datetime.now()
    duration = end-begin

    print('-Completed! - 100%\n')
    print('-{} lists and {} cards were created!'.format(len(board.lists), board.total_cards))

    print('Time:{}\n'.format(duration))
    print("######################")
    raw_input()


if __name__ == '__main__':
    main()
