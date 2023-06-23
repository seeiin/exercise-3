from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.extensions import db, jwt
from app.auth import authBp
from app.models.user import Users
from app.models.profile import Profiles
from app.models.blacklist_token import BlacklistToken

@authBp.route("/register", methods=['POST'], strict_slashes =False)
def registration():
    """
    Fungsi untuk registrasi user baru

    args:
        -

    return
        response (json object): pesan response
    """
    # get data from request json
    data = request.get_json()
    
    # get data json
    username = data.get('username', None)
    email = data.get('email', None)
    password = generate_password_hash(data.get('password', None))
    biography = data.get('biography', None)
    profile_image_url = data.get('profile_image_url', None)
    website = data.get('website', None)
    location = data.get('location', None)
    
    # validasi input
    if not username or not email or not password:
        return jsonify(
            message = "Username or Email or Password is required"
        ), 400
 
    try:
        # menambahkan user dan profile ke db
        user = Users(username=username, 
                     email=email, 
                     password=password)
        db.session.add(user)
        db.session.commit()
        
        profile = Profiles(biography=biography,
                           profile_image_url=profile_image_url,
                           website=website,
                           location=location,
                           user_id = user.user_id)     
        db.session.add(profile)
        db.session.commit()
    except IntegrityError:
        # jika user duplikat
        return jsonify(
            message = f"User {username} is already registered."
        ), 422
      
    return jsonify({
        "message": "Registration user is completed"
    }), 200
       

@authBp.route("/login", methods=['POST'], strict_slashes = False)
def login():
    """
    Fungsi untuk login

    args:
        -

    return
        response (json object): pesan response
    """
    # get data from request json
    data = request.get_json()
    
    # get name password from json
    username = data.get('username', None)
    password = data.get('password', None)

    # validasi input
    if not username or not password:
        return jsonify(
            message = "Username or Password is required"
        ), 400
    
    # query record user dari database dengan name request
    user = Users.query.filter_by(username=username).first()

    # cek apakah user ada pada databse atau tidak
    if not user or not check_password_hash(user.password, password):
        return jsonify(
            message = "Username or Password is invalid"
        ), 422
    else:
        # buat akses dan refresh token
        access_token = create_access_token(identity=user.user_id)
        refresh_token = create_refresh_token(identity=user.user_id)

    # jika berhasil berikan message berhasil login
    return jsonify({
        "message":"Berhasil Login",
        "access_token" : access_token,
        "refresh_token" : refresh_token}), 200

@authBp.route('/refresh', methods=['POST'])
@jwt_required(refresh = True)
def refresh():
    """
    Fungsi untuk perbarui access token jika sudah kadaluarsa dengan refresh token.

    args:
        -

    return
        response (json object): pesan response
    """
    current_user = get_jwt_identity()
    access_token = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(access_token), 200

@authBp.route("/logout", methods=['POST'], strict_slashes = False)
@jwt_required(locations=["headers"])
def logout():
    """
    Fungsi untuk logout

    args:
        -

    return
        response (json object): pesan response
    """
    # mendapatkan token jwt
    raw_jwt = get_jwt()

    # menambahkan token jwt ke blacklist
    # mencabut JWT dan menolak akses ke permintaan di masa mendatang
    jti = raw_jwt.get('jti')
    token = BlacklistToken(jti = jti)
    
    db.session.add(token)
    db.session.commit()
    return jsonify(message = "logout successfully")

# callback untuk memeriksa apakah JWT ada di daftar blokir atau tidak
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    """
    Fungsi untuk cek apakah token ada di database atau tidak

    args:
        -

    return
        token (str): None jika token tidak ada pada databse
    """
    jti = jwt_payload["jti"]
    token = BlacklistToken.query.filter_by(jti=jti).first()
    return token is not None