import json
import requests
from flask import Blueprint, jsonify, request
from src.constants.http_satus_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

search = Blueprint('search', __name__, url_prefix='/api/v1/search')

@search.get('/')
def mencari():

    nama = request.get_json().get('name', '')

    url = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'
    r = requests.get(url)
    json_obj = r.json()
    data = json_obj['data']
    for name, attributes in data.items():
        if attributes['name'].find(str(nama.capitalize())) != -1:
            return jsonify({
                #"data":attributes
                "Version":attributes['version'],
                "Id":attributes['id'],
                "Key":attributes['key'],
                "Name":attributes['name'],
                "Title":attributes['title'],
                "blurb":attributes['blurb'],
                "info":attributes['info'],
                "image":attributes['image'],
                "tags":attributes['tags'],
                "partype":attributes['partype'],
                "stats":attributes['stats']
                }), HTTP_200_OK

    return jsonify({
        "msg":"Data not found"
    }), HTTP_404_NOT_FOUND


    