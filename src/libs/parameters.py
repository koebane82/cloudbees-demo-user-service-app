from .aws_base import AWSBase
from abc import ABC

class ParameterNotFoundException(Exception):
    """Exception raised when a parameter can't be found
    Attributes:
        parameter_name -- the name of the parameter looked for
        message -- explination of the error
    """
    def __init__(self, parameter_name: str) -> None:
        self.parameter_name = parameter_name
        self.message = "Unable to find parameter: {}".format(parameter_name)
        super().__init__(self.message)
    
    def __str__(self):
        return self.message


class Parameter(ABC):
    """Parameter is an abstract class used to which
        dictates the outline of Parameter classes

    Methods
    -------
        get_value(name:str) - gets the value of a prameter
        put_parameter(name:str, value:str, description:str) - puts a parameter
    """
    def get_value(self, name:str) -> str:
        """ The is ment to get the value of a paramter"""

    def put_parameter(self, name:str, value:str, description: str) -> None:
        """ Set's or create a parameter"""


class AWSParameter(Parameter, AWSBase):
    """AWSParameter is a class used to interact with aws parameter stores"""
    def __init__(self, ssm_client=None):
        super().__init__("ssm", ssm_client)

    def get_value(self, name:str) -> str:
        try:
            _param = self._client.get_parameter(Name=name)
        except Exception as e:
            error_code = e.response.get('Error').get('Code')

            if error_code == 'ParameterNotFound':
                raise ParameterNotFoundException(name)
            else:
                raise e
        
        _value = _param.get('Parameter').get('Value')
        return _value

    def put_parameter(self, name: str, value: str, description: str) -> None:
        self._client.put_parameter(
            Name = name,
            Value = value,
            Description = description,
            Type = 'String',
            Tier = 'Standard'
        )