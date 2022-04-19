import logging
import os
from lib.parameters import Parameter, ParameterNotFoundException

APPLICATION_NAME = "test-application"

class AppConfig:
    """AppConfig is a class which stores the configurtion of the application
    Abstract Methods
    ----------------
    get_log_handlers(log_level) - gets log handlers
    """
    # The default log level
    DEFAULT_LOG_LEVEL = "info"
    # An empty variable to store features
    features = []

    def __init__(self, parameter_client:Parameter=None, env_prefix:str=None, debug:bool=False):
        """_summary_

        Args:
            parameter_client (Parameter, optional): A Parameter Client. Defaults to None.
            env_prefix (str, optional): name of a sub-environment. Defaults to None.
            debug (bool, optional): overide log level as debug. Defaults to False.
        """
        self._parameter_client = parameter_client
        self._env_prefix = env_prefix
        # Get the log level
        _log_level = self._get_log_level()

        # override the log level
        if debug:
            _log_level = logging.DEBUG
        
        self.log_level = _log_level
        self.log_handlers = AppConfig.get_log_handlers(_log_level)
        self.features = self._get_features()

    def _get_setting(self, param_name:str, default_value:str, description:str) -> str:
        """Gets a setting based on a priority
           (1) Environment Variable
           (2) Parameter Client
           (3) Default Value

        Args:
            param_name (str): Name of the parameter or setting
            default_value (str): The default value of the setting
            description (str): A description of the setting

        Returns:
            str: _description_
        """
        logging.debug("Getting setting value for %s", param_name)
        # Convert setting/param to an ENV variable
        _env_var = param_name.upper().replace("-", "_").replace(".","_").replace("/", "_")

        logging.debug("Checking for environment variable %s", _env_var)
        _setting_value = os.environ.get(_env_var)

        # Set the base of the parameter name
        _param_name = "/{}".format(APPLICATION_NAME)

        if _setting_value is None:
            logging.debug("Environment variable %s not found", _env_var)
            if self._parameter_client is not None:
                # add prefix to param_name
                if self._env_prefix is not None:
                    _param_name = "{}/{}".format(_param_name, self._env_prefix)
                # generate resulting parameter name
                _param_name = "{}/{}".format(_param_name, param_name)

                try:
                    # Get the setting from the parameter store
                    logging.debug("Getting value of %s from %s", param_name, _param_name)
                    _setting_value = self._parameter_client.get_value(_param_name)
                except ParameterNotFoundException:
                    # if the parameter store does not contain parameter, create it
                    logging.debug("Creating parameter %s with value %s", _param_name, default_value)
                    self._parameter_client.put_parameter(
                        name=_param_name,
                        value=default_value,
                        description=description
                    )
        
        if _setting_value is None:
            # if setting is still none, set the value to default
            logging.debug("Setting value for %s not found, using default: %s", param_name, default_value)
            _setting_value = default_value

        return _setting_value

    def _get_log_level(self, param_prefix:str = None) -> int:
        """Gets the log_level based on the setting

        Args:
            param_prefix (str, optional): A parameter prefix. Defaults to None.

        Raises:
            ValueError: if resulting value isn't debug, info, error, warning, or critical

        Returns:
            int: log_level
        """
        _log_level = None

        # Get the log value
        _log_level_str = self._get_setting(
            param_name="log-level",
            default_value=self.DEFAULT_LOG_LEVEL,
            description="Log Level for {}".format(APPLICATION_NAME),
        ).lower()

        # convert _log_level_str to logging._log_level_
        if _log_level_str == "debug":
            _log_level = logging.DEBUG,
        elif _log_level_str == "info":
            _log_level = logging.INFO
        elif _log_level_str == "error":
            _log_level = logging.ERROR
        elif _log_level_str == "warn" or _log_level_str == "warning":
            _log_level = logging.WARNING
        elif _log_level_str == "critical" or _log_level_str == "crit":
            _log_level = logging.CRITICAL
        else:
            raise ValueError("Unknown log level: {}".format(_log_level_str))
        
        # check the instance of the _log_level
        if isinstance(_log_level, tuple):
            _log_level = _log_level[0]

        return _log_level

    def _get_features(self) -> list:
        """Returns a list of enabled features

        Returns:
            list: a list of features
        """
        # variable to store fetures
        _return_features = []
        # a dict to store feature names and their descriptions
        _features = {'user-icon': "display a user icon"}

        for feature, description in _features.items():
            # check if a feature value is enabled
            _feature_val = self._get_setting(
                param_name='feature/{}'.format(feature),
                default_value="off",
                description=description
            ).lower()

            # if feature value is 'on' added it to the list
            if _feature_val == "on":
                _return_features.append(feature)

        return _return_features

    @staticmethod
    def get_log_handlers(log_level:int) -> list:
        """Returns a list of log_handlers

        Args:
            log_level (int): log_level

        Returns:
            list: a list of handlers
        """
        _handlers = []

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        if log_level == logging.DEBUG:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

        _stream_handler = logging.StreamHandler()
        _stream_handler.setLevel(log_level)
        _stream_handler.setFormatter(formatter)

        _handlers.append(_stream_handler)
        return _handlers