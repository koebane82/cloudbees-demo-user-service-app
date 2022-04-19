import json
import logging
from http.server import BaseHTTPRequestHandler
from app_config import AppConfig

config = None

class UserService(BaseHTTPRequestHandler):
    _user_map = {
        "1": {
            "first_name": "Dude",
            "last_name": "Duder",
            "username": "dudeduerson",
            "icon": "default.png"
        },
        "2": {
            "first_name": "Mike",
            "last_name": "Mikerson",
            "username": "reallycoolguy",
            "icon": "default.png"
        },
        "3": {
            "first_name": "Linda",
            "last_name": "Lister",
            "username": "awesomegal",
            "icon": "default.png"
        }
    }

    def _get_user(self, user_id):
        return_val = None

        logging.debug('Searching for User ID %s', user_id)
        if user_id in self._user_map:
            logging.info("User ID %s Found", user_id)
            _user = self._user_map.get(user_id)

            return_val = {
                "username":  _user.get("username"),
            }

            if "user-icon" in config.features:
                return_val['icon'] = _user.get('icon')
        else:
            logging.info("User ID %s not found", user_id)

        return return_val

    def do_GET(self):
        _response_code = 404
        _msg = "path not found"
        _headers = {}

        if self.path.startswith('/user'):
            _user_id = self.path.split('/')[2]
            _user_info = self._get_user(_user_id)

            if _user_info is None:
                _msg = "user not found"
            else:
                _response_code = 200
                _msg = json.dumps(_user_info)

        if _response_code == 200:
            _headers['Content-type'] = "application/json"

        self.send_response(_response_code)

        if len(_headers) > 0:
            for key, value in _headers.items():
                self.send_header(key, value)
            
            self.end_headers()
        
        self.wfile.write(bytes(_msg, "utf-8"))