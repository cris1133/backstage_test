from models import *
from flask import Flask, jsonify
app = Flask(__name__)


@app.route('/api/years/<year>', methods=['GET'])
@app.route('/api/years/', methods=['GET'])
def years_endpoint(year=None):
    if year:
        return jsonify({
            'characters': Character.select().where(Character.born == year).count()
        })
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
