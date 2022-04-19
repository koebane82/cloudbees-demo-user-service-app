import boto3
import os

class AWSBase:
    """
    AWSBase is a class intended to be be a base class to build 
    functionality for all AWS classes
    """
    # The default AWS Region
    _default_region = "us-east-1"
    _client = None

    def __init__(self, client_type: str, client:object=None) -> None:
        if client is None:
            client = self._generate_client(client_type)

        self._client = client        

    def _generate_client(self, client_type: str) -> object:
        """
        _generate_client creates a AWS client based on environment
        Args
        ----
        client_type (str) - the type of AWS client to return
        Returns
        -------
        object - an AWS client
        """

        # Attempt to get AWS Variables from the environment
        _access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        _secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        _session_token = os.getenv('AWS_SESSION_TOKEN')
        _region = os.getenv('AWS_REGION')

        # if AWS region is non, set it to default region
        if _region is None:
            _region = self._default_region

        # Create an empty variable for the client
        client = None

        if _access_key_id is None:
            # if auth variables are not present, attempt to get a client with out
            client = boto3.client(client_type)
        elif _session_token is None:
            client = boto3.client(client_type,
                aws_access_key_id = _access_key_id,
                aws_secret_access_key = _secret_access_key,
                region_name = _region
            )
        else:
            client = boto3.client(client_type,
                aws_access_key_id = _access_key_id,
                aws_secret_access_key = _secret_access_key,
                aws_session_token = _session_token,
                region_name = _region
            )

        return client