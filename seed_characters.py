import requests
import json
import sys
import re


def format(character):
    year_finder = re.compile('(\d{1,}) (BC|AC)')

    if not character.get('name', False) and bool(character.get('aliases', False)):
        character['name'] = character['aliases'][0]
    character['name'] = str(character['name'])

    character['born'] = year_finder.findall(character['born'])
    if character['born']:
        character['born'] = [int(character['born'][0][0]), str(character['born'][0][1])]

    return {key: character[key] for key in ['name', 'born', 'allegiances']}


def scrape():
    results = []
    page = 1

    while True:
        characters = json.loads(requests.get('https://anapioficeandfire.com/api/characters?pagesize=50&page={}'.format(page)).content)
        for character in characters:
            results.append(format_character(character))
        if len(characters) < 50:
            break
        page += 1

    return results


def load(characters, db_url):
    pass


if __name__ == "__main__":
    characters = scrape_characters()
    load_characters(characters, sys.argv[0])
