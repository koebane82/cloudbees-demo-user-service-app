import json
import logging
from http.server import BaseHTTPRequestHandler
from app_config import AppConfig

config = None

class UserService(BaseHTTPRequestHandler):
    """The UserService Class provides a HTTP Handler for the User Service

    Methods
    -------
    do_Get() - Handles GET requests

    """
    # _user_map handles user data until replaced with future functionality
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

    def _get_user(self, user_id: str) -> dict:
        """_get_user returns user info based on the user_id

        Args
        ----
        user_id (str): id of the user requested

        Returns
        -------
        dict: a dict of user infomration
        """
        # empty return variable
        return_val = None

        logging.debug('Searching for User ID %s', user_id)

        # get user if user id is in map
        if user_id in self._user_map:
            logging.info("User ID %s Found", user_id)
            _user = self._user_map.get(user_id)

            return_val = {
                "username":  _user.get("username"),
            }

            # if user-icon feature is enabled, add icon location to return value
            if "user-icon" in config.features:
                return_val['icon'] = _user.get('icon')
        else:
            logging.info("User ID %s not found", user_id)

        return return_val

    def do_GET(self):
        """ do_get handles GET HTTP request"""
        # Set default response code
        _response_code = 404
        # Set default message
        _msg = "path not found"
        # empty variable for headers
        _headers = {}

        # check for user path
        if self.path.startswith('/user'):
            # get the user id from path
            _user_id = self.path.split('/')[2]
            # get the information about the user
            _user_info = self._get_user(_user_id)

            # if user doesn't exist, return user not found
            if _user_info is None:
                _msg = "user not found"
            else:
                _response_code = 200
                _msg = json.dumps(_user_info)

        # add content-type header if returing data
        if _response_code == 200:
            _headers['Content-type'] = "application/json"

        # Send response Code
        self.send_response(_response_code)

        # send headers if there are headers
        if len(_headers) > 0:
            for key, value in _headers.items():
                self.send_header(key, value)
            
            self.end_headers()
        # send data
        self.wfile.write(bytes(_msg, "utf-8"))