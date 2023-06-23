from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.profile import profileBp
from app.extensions import db
from app.models.profile import Profiles
from app.models.user import Users

# route GET all user
@profileBp.route("", methods=['GET'], strict_slashes = False)
# @jwt_required(locations=["headers"])
def get_all_user():
    """
    Fungsi untuk mendapatkan semua user

    args:
        -

    return
        response (json object): pesan response
    """
    
    # mendapatkan argumen limit
    limit = request.args.get('limit', 10)
    if type(limit) is not int:
        return jsonify({'message': 'invalid parameter'}), 400

    # query untuk mendapatkan data user
    users = db.session.execute(
        db.select(Users).limit(limit)
    ).scalars()

    # mengubah object hasil query menjadi dictionary
    result = []
    for user in users:
        result.append(user.serialize())

    # membuat response
    response = jsonify(
        success = True,
        data = result
    )

    return response, 200

@profileBp.route("<int:id>", methods=['GET'], strict_slashes = False)
# @jwt_required(locations=["headers"])
def get_one_user(id):
    """
    Fungsi untuk mendapatkan profile user

    args:
        id (int): id user profile

    return
        response (json object): pesan response
    """
    
    # mendapatkan task berdasarkan id
    profiles = Profiles.query.filter_by(profile_id=id).first()

    # cek apakah variable hasil query kosong
    if not profiles:
        return jsonify({'error': 'User Profile not found'}), 422
    
    # mendapatkan task dalam bentuk dictionary
    profile = profiles.serialize()
    user = profiles.user.serialize()

    user.update(profile)

    # membuat response dalam bentuk object json
    response = jsonify(
        success = True,
        data = user)
    
    return response, 200