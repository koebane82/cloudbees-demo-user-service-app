from src.lib.parameters import AWSParameter
from src.lib.parameters import ParameterNotFoundException
from .mock_boto import MockSSM
import unittest

class TestParameterNotFoundException(unittest.TestCase):
    def test_call(self):
        _param_name = "test-parameter"
        _error = ParameterNotFoundException(_param_name)

        self.assertEqual(_param_name, _error.parameter_name)
        
        msg = "Unable to find parameter: {}".format(_param_name)
        self.assertEqual(msg, _error.message)


class TestAWSParameter(unittest.TestCase):
    def setUp(self) -> None:
        self._param1 = "testValue"
        self._param_map = {
            "_param1": self._param1
        }

        _client = MockSSM(self._param_map)

        self._aws_paramter = AWSParameter(_client)

    def test_get_non_existent_param(self):
        with self.assertRaises(ParameterNotFoundException):
            self._aws_paramter.get_value("bad_value")

    def test_get_value(self):
        value = self._aws_paramter.get_value("_param1")
        self.assertEqual(self._param1, value)

    def test_put_parameter(self):
        _name = "test_param"
        _value = "value2"

        self._aws_paramter.put_parameter(_name, _value, 'test_description')

        self.assertEqual(_value, self._param_map.get(_name))