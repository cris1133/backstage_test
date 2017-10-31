from models import *
import requests
import json
import sys
import re


def format_character(character):
    year_finder = re.compile('(\d{1,}) (BC|AC)')

    if not character.get('name', False) and bool(character.get('aliases', False)):
        character['name'] = character['aliases'][0]
    character['name'] = str(character['name'])

    character['born'] = year_finder.findall(character['born'])
    if character['born']:
        character['born'] = [int(character['born'][0][0]), str(character['born'][0][1])]
        if character['born'][1] == 'BC':
            character['born'][0] *= -1
        character['born'] = character['born'][0]
    else:
        character['born'] = None

    return {key: character[key] for key in ['name', 'born', 'allegiances']}


def format_house(house):
    house['number'] = house['url'].split('/')[-1]
    return {key: house[key] for key in ['name', 'number']}


format_functions = {
    'characters': format_character,
    'houses': format_house
}


def scrape(endpoint):
    results = []
    page = 1

    while True:
        items = json.loads(requests.get('https://anapioficeandfire.com/api/{}?pagesize=50&page={}'.format(endpoint, page)).content)
        for item in items:
            results.append(format_functions[endpoint](item))
        if len(items) < 50:
            break
        page += 1

    return results


def load(characters, houses):
    with db.atomic():
        for idx in range(0, len(houses), 100):
            House.insert_many(houses[idx:idx+100]).execute()
    with db.atomic():
        for character in characters:
            character_obj = Character.create(name=character['name'], born=character['born'])
            for allegiance in character['allegiances']:
                number = int(allegiance.split('/')[-1])
                character_obj.allegiances.add(House.select().where(House.number == number))


if __name__ == "__main__":
    Character.create_table(fail_silently=True)
    House.create_table(fail_silently=True)
    House.members.get_through_model().create_table(fail_silently=True)
    houses = scrape('houses')
    characters = scrape('characters')
    load(characters, houses)
