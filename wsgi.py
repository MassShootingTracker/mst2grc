import os
from MSTtoGRC import mst_to_grc

from flask import Flask, request
app = Flask('__name__')


@app.route("/update/grc", methods=['GET', 'POST'])
def update_grc():
    year = request.args.get('year', 'all')
    api_key = request.args.get('key', '')

    if api_key != os.environ['MSTGRC_KEY'] if 'MSTGRC_KEY' in os.environ else '':
        return "Unrecognized API key."

    cfg_file = os.environ['MSTGRC_CFG'] if 'MSTGRC_CFG' in os.environ else 'config.json'

    mst_to_grc(year, cfg_file)

    return "Done."


@app.route('/')
def hello():
    return "I'm alive!"


if __name__ == "__main__":
    app.run(debug=True)