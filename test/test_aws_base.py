import os
import unittest
from unittest.mock import patch
from .mock_boto import MockBoto, MockGenericClient
from src.libs.aws_base import AWSBase

class TestAWSBase(unittest.TestCase):
    def setUp(self) -> None:
        self._client = MockGenericClient()
        self._aws_base = AWSBase('test', self._client)
        self._access_key_id = '11111111'
        self._secret_access_key = '222222222'
        self._session_token = '3333333'
        self._region = 'no-real-region'

        env_vars = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'AWS_SESSION_TOKEN',
            'AWS_REGION'
        ]

        for env_var in env_vars:
            if env_var in os.environ:
                del(os.environ[env_var])

    def test_initializor_with_arg(self):
        _client = AWSBase("Test3", client=self._client)
        self.assertEqual("Generic", _client._client._client_type)

    @patch("boto3.client", MockBoto.client)
    def test_initializor_without_arg(self):
        _client_type = "test_client"
        _client = AWSBase(_client_type)

        self.assertEqual(_client_type, _client._client._client_type)


    @patch("boto3.client", MockBoto.client)
    def test__generate_client_without_env_vars(self):
        _client_type = "test"

        _new_client = self._aws_base._generate_client(client_type=_client_type)
        self.assertEqual(_client_type, _new_client._client_type)
        self.assertIsNone(_new_client._aws_access_key_id)
        self.assertIsNone(_new_client._aws_secret_access_key)
        self.assertIsNone(_new_client._aws_session_token)
        self.assertIsNone(_new_client._region_name)

    @patch("boto3.client", MockBoto.client)
    def test__generate_client_with_id_and_key(self):
        _client_type = "test1"

        os.environ['AWS_ACCESS_KEY_ID'] = self._access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = self._secret_access_key

        _new_client = self._aws_base._generate_client(client_type=_client_type)
        self.assertEqual(_client_type, _new_client._client_type)
        self.assertEqual(self._access_key_id, _new_client._aws_access_key_id)
        self.assertEqual(self._secret_access_key, _new_client._aws_secret_access_key)
        self.assertIsNone(_new_client._aws_session_token)
        self.assertEqual( 'us-east-1', _new_client._region_name)

    @patch("boto3.client", MockBoto.client)
    def test__generate_client_with_id_key_and_token(self):
        _client_type = "test1"

        os.environ['AWS_ACCESS_KEY_ID'] = self._access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = self._secret_access_key
        os.environ['AWS_SESSION_TOKEN'] = self._session_token

        _new_client = self._aws_base._generate_client(client_type=_client_type)
        self.assertEqual(_client_type, _new_client._client_type)
        self.assertEqual(self._access_key_id, _new_client._aws_access_key_id)
        self.assertEqual(self._secret_access_key, _new_client._aws_secret_access_key)
        self.assertEqual(self._session_token, _new_client._aws_session_token)
        self.assertEqual( 'us-east-1', _new_client._region_name)
    
    @patch("boto3.client", MockBoto.client)
    def test__generate_client_with_id_key_token_and_region(self):
        _client_type = "test1"

        os.environ['AWS_ACCESS_KEY_ID'] = self._access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = self._secret_access_key
        os.environ['AWS_SESSION_TOKEN'] = self._session_token
        os.environ['AWS_REGION'] = self._region

        _new_client = self._aws_base._generate_client(client_type=_client_type)
        self.assertEqual(_client_type, _new_client._client_type)
        self.assertEqual(self._access_key_id, _new_client._aws_access_key_id)
        self.assertEqual(self._secret_access_key, _new_client._aws_secret_access_key)
        self.assertEqual(self._session_token, _new_client._aws_session_token)
        self.assertEqual(self._region, _new_client._region_name)