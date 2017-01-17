import os
import json

import bottle
from bottle import request, route, run

from mst2grc import mst_to_grc

@route("/grcupdate", method=['get', 'post'])
def update_grc():
    year = request.params.get('year', 'all')
    api_key = request.params.get('key')

    cfg_file = os.environ['MSTGRC_CFG'] if 'MSTGRC_CFG' in os.environ else 'config.json'

    with open(cfg_file) as fp:
        config = json.load(fp)

    if api_key != config['app']['key']:
        return json.dumps({'status': 'error', 'msg': "Unrecognized API key."})


    mst_to_grc(year, cfg_file)

    return json.dumps({'status': 'ok', 'msg': 'Update complete.'})


@route('/')
def hello():
    return json.dumps({'status': 'ok', 'msg': 'I\'m alive.'})


if __name__ == "__main__":
    app.run(debug=True)

app = bottle.default_app()
