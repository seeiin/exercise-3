from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.extensions import db
from app.content import contentBp
from app.models.content import Contents

# route GET all contents
@contentBp.route("", methods=['GET'], strict_slashes = False)
@jwt_required(locations=["headers"], optional=True)
def get_all_content():
    """
    Fungsi untuk mendapatkan semua content

    args:
        -

    return
        response (json object): pesan response
    """
    
    # mendapatkan argumen limit
    limit = request.args.get('limit', 10)
    if type(limit) is not int:
        return jsonify({'message': 'invalid parameter'}), 400

    # query untuk mendapatkan data content
    contents = db.session.execute(
        db.select(Contents).limit(limit)
    ).scalars()

    # mengubah object contents menjadi dictionary
    result = []
    for content in contents:
        result.append(content.serialize())

    # membuat response
    response = jsonify(
        success = True,
        data = result
    )
    
    return response, 200
    
# route GET contents/<id>
@contentBp.route("<int:id>", methods=['GET'], strict_slashes = False)
@jwt_required(locations=["headers"])
def get_one_content(id):
    """
    Fungsi untuk mendapatkan content berdasarkan id

    args:
        id (int): id content

    return
        response (json object): pesan response
    """
    
    # mendapatkan content berdasarkan id
    contents = Contents.query.filter_by(content_id=id).first()

    # cek apakah variable hasil query kosong
    if not contents:
        return jsonify({'error': 'content not found'}), 422
    
    # mendapatkan content dalam bentuk dictionary
    content = contents.serialize()

    # membuat response dalam bentuk object json
    response = jsonify(
        success = True,
        data = content)
    
    return response, 200

# route POST /contents
@contentBp.route("", methods=['POST'], strict_slashes = False)
@jwt_required(locations=["headers"])
def create_content():
    """
    Fungsi untuk membuat content baru

    args:
        -

    return
        response (json object): pesan response
    """
    
    # mendapatkan request json dari client
    data = request.get_json()
    caption = data.get("caption", None)
    image_url = data.get("image_url", None)
    user_id = get_jwt_identity()
    created_at = datetime.now()

    # # Validasi input
    # if not ... or not ... or not ...:
    #     return jsonify({'message': 'incomplete data'}),422

    # menambahkan content baru
    new_content = Contents(caption = caption,
                           image_url = image_url,
                           created_at = created_at,
                           user_id = user_id)
    
    # menambahkan data ke database
    db.session.add(new_content)
    db.session.commit()

    # membuat response
    response = jsonify(
        success = True,
        data = new_content.serialize()
    )

    return response, 200

# route DELETE contents/id
@contentBp.route("<int:id>", methods=['DELETE'], strict_slashes = False)
@jwt_required(locations=["headers"])
def delete_content(id):
    """
    Fungsi untuk hapus content berdasarkan id

    args:
        id (int) : id content

    return
        response (json object): pesan response
    """
    # mendapatkan current user yang login
    current_user = get_jwt_identity()

    # mendapatkan user yang create content
    content = Contents.query.filter_by(content_id=id).first()
    
    # cek apakah variable hasil query kosong
    if not content:
        return jsonify({'error': 'content not found'}), 422

    # cek apakah current user sama dengan user yang membuat content
    if current_user != content.user_id :
        return jsonify(
            message = 'You do not have permission to edit this content'
        ), 403

    db.session.delete(content)
    db.session.commit()
    
    # membuat response
    response = jsonify({
        "success" : True,
        "message" : "data delete successfully",
    })

    return response, 200