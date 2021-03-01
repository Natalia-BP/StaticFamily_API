"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    # error = {
    # status_code = [400, 404]
    # }
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET METHOD ALL MEMBERS
@app.route('/members', methods=['GET'])
def all_members():
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }

    return jsonify(response_body), 200

# GET ONE MEMBER
@app.route('/member/<int:id>', methods=['GET'])
def getOne_member(id):
    oneMember = jackson_family.get_member(id)
    if oneMember is None:
        error_body = {
            "Error_Msg": "We couln't find that id, sorry"
        }
        return jsonify(error_body), 404

    else:
        api_body = {
                "family": oneMember
            }
        return jsonify(api_body), 200


# POST METHOD NEW MEMBER 
@app.route('/members', methods=['POST'])
def post_member():
    request_body = request.get_json()
    if isinstance(request_body, dict):
        memberPost = jackson_family.add_member(request_body)
        response_body = {
            "All_GoodMsg": "New member was added succesfully"
        }
        return jsonify(response_body), 200
    else: return jsonify({"Error_Msg":"400 Bad Request\nIt should be a python dictionary! Check again"}), 400


# PUT METHOD
@app.route('/members/<int:id>', methods=['PUT'])
def refresh_member(id):
    update_body = request.get_json()
    memberUpdate = jackson_family.update_member(id, update_body)
    if memberUpdate:
        response_body = {
            "All_GoodMsg": "The family member has been updated"
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"Error_Msg": "400 Bad Request\nWe can't update from a non-existing id, check again"}), 400

# DELETE METHOD
@app.route('/member/<int:id>', methods=['DELETE'])
def del_member(id):
    memberDelete = jackson_family.delete_member(id)
    if memberDelete:
        response_body = {
            "All_GoodMsg": "The family member has been removed"
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"Error_Msg": "404 not found\nSorry! We can't find the requested id, check again"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
