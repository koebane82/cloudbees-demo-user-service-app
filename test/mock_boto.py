
class MockAWSException(Exception):
    def __init__(self, _error_code):
        self.response = {
            'Error': {
                'Code': _error_code
            }
        }


class MockGenericClient:
    def __init__(self, client_type="Generic", 
                 aws_access_key_id=None,
                 aws_secret_access_key=None, 
                 aws_session_token=None,
                 region_name=None):
        self._client_type = client_type
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_session_token = aws_session_token
        self._region_name = region_name


class MockSSM:
    def __init__(self, value_map:dict = None):
        self._value_map = value_map

    def get_parameter(self, Name:str) -> dict:
        if Name not in self._value_map:
            raise MockAWSException('ParameterNotFound')

        _ret_value = {
            "Parameter": {
                "Value": self._value_map.get(Name)
            }
        }

        return _ret_value

    def put_parameter(self, Name:str, Value:str, **kwargs):
        self._value_map[Name] = Value


class MockBoto:
    @staticmethod
    def client(*args, **kwargs):
        client_type = args[0]
        _aws_access_key_id = kwargs.get('aws_access_key_id')
        _secret_access_key = kwargs.get('aws_secret_access_key')
        _aws_session_token = kwargs.get('aws_session_token')
        _region_name = kwargs.get('region_name')

        if client_type == "None":
            return None
        else:
            return MockGenericClient(client_type=client_type,
                                     aws_access_key_id=_aws_access_key_id,
                                     aws_secret_access_key=_secret_access_key,
                                     aws_session_token=_aws_session_token,
                                     region_name=_region_name)