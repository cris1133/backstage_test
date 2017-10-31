from models import *
from flask import Flask, jsonify, request, make_response
app = Flask(__name__)


@app.route('/api/characters/', methods=['GET'])
def characters_endpoint(character=None):
    if request.args.get('born_near', False):
        if not Character.select().where(Character.id == int(request.args.get('born_near'))).count():
            return make_response(jsonify({'error': "Invalid character id given."}), 404)
        born_near = Character.select().where(Character.id == int(request.args.get('born_near'))).first()
        if born_near.born is None:
            result = {'characters': [born_near.__dict__['_data']]}
        else:
            years = int(request.args.get('years', 0))
            print born_near.born
            result = {
                'characters': [
                    character.__dict__['_data']
                    for character in list(
                        Character.select()
                        .where(
                            (Character.born >= (born_near.born - years)),
                            (Character.born <= (born_near.born + years))
                        ).execute()
                    )
                ]
            }
    else:
        result = {
            'characters': [
                character.__dict__['_data']
                for character in list(Character.select().execute())
            ]
        }
    for i in range(len(result['characters'])):
        if result['characters'][i]['born'] is None:
            result['characters'][i]['born'] = "Unknown"
        elif result['characters'][i]['born'] < 0:
            result['characters'][i]['born'] *= -1
            result['characters'][i]['born'] = "{} BC".format(result['characters'][i]['born'])
        else:
            result['characters'][i]['born'] = "{} AC".format(result['characters'][i]['born'])
    return jsonify(result)


@app.route('/api/born_on/<year>', methods=['GET'])
@app.route('/api/born_on/', methods=['GET'])
def year_endpoint(year=None):
    if year:
        return jsonify({
            'characters': Character.select().where(Character.born == year).count()
        })
    else:
        result = {
            'years': [
                {'year': result[0], 'characters': int(result[1])}
                for result in db.execute_sql("SELECT born, COUNT(*) FROM character GROUP BY born;").fetchall()
            ]
        }
        for i in range(len(result['years'])):
            if result['years'][i]['year'] is None:
                result['years'][i]['year'] = "Unknown"
            elif result['years'][i]['year'] < 0:
                result['years'][i]['year'] *= -1
                result['years'][i]['year'] = "{} BC".format(result['years'][i]['year'])
            else:
                result['years'][i]['year'] = "{} AC".format(result['years'][i]['year'])
        return jsonify(result)





if __name__ == '__main__':
    app.run(debug=True)
