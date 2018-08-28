#!/usr/bin/env python3
# responseUtil.py
# This file contains helper functions to return a bot response given a query
# and a category

from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tag.stanford import StanfordNERTagger
import json

PERSONAL_EQUITY = {'income':6000,
                  'rent':-3000,
                  'utilGroceries':-1000,
                  'shopping':-1000,
                  'dining':-500}

BANK_ACCOUNTS = {'boa':{
                        'checking':{
                                    'lastFour':9898,
                                    'balance':9000
                                    },
                        'savings':{
                                    'balance':100000
                                  }
                       },
                 'chase':{
                          'savings':{
                                     'lastFour':9898,
                                     'balance':80000
                                     }
                         },
                 'creditCard':-15000
                }

with open('src/data/conversation.json') as f:
    intents = json.load(f)

def conversationFlow(category, userRequest):
    word_tokens = word_tokenize(userRequest)
    POS = pos_tag(word_tokens)
    if category == 'balance':
        botResponse = balanceFlow(word_tokens)
    elif category == 'budgeting':
        botResponse = budgetingFlow(word_tokens, POS)
    elif category == 'housing':
        botResponse = housingFlow(word_tokens, POS)
    return botResponse

def balanceFlow(word_tokens):
    bank = account = ""
    if 'checking' in word_tokens:
        account = 'checking'
        bank = 'BoA'
    elif 'savings' in word_tokens:
        account = 'savings'
        bank = getBank(word_tokens)

    if not account:
        account = input('\033[94m' + intents['categorySet'][0]['responseSet'][0]['whichAccount'] + '\033[0m\n--> ')
    while not bank:
        bank = getBank(input('\033[94m' + intents['categorySet'][0]['responseSet'][0]['whichBank'] + '\033[0m\n--> ').split())
    return intents['categorySet'][0]['responseSet'][0]['balance'].format(bank, account, BANK_ACCOUNTS[bank.lower()][account]['balance'])

def budgetingFlow(word_tokens, POS):
    print('c')

def housingFlow(word_tokens, POS):
    for index,item in enumerate(POS):
        if 'CD' in item:
            cost = item[0]

def getBank(word_tokens):
    bank = ""
    st = StanfordNERTagger('src/data/bank-ner-model.ser.gz', '../stanford-ner-2018-02-27/stanford-ner.jar')
    tagged_words = st.tag(word_tokens)
    for tag in tagged_words:
        if 'C-ORG' in tag:
            bank = 'Chase'
        elif 'B-ORG' in tag:
            bank = 'BoA'

    return bank

def unknownFlow():
    return random.choice(intents['categorySet'][3]['responseSet'])
