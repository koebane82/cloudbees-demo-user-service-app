import logging
import os
from lib.parameters import Parameter, ParameterNotFoundException

APPLICATION_NAME = "test-application"

class AppConfig:
    DEFAULT_LOG_LEVEL = "info"
    features = []

    def __init__(self, parameter_client:Parameter=None, env_prefix:str=None, debug:bool=False):
        self._parameter_client = parameter_client
        self._env_prefix = env_prefix

        _log_level = self._get_log_level()

        if debug:
            _log_level = logging.DEBUG
        
        self.log_level = _log_level
        self.log_handlers = AppConfig.get_log_handlers(_log_level)
        self.features = self._get_features()

    def _get_setting(self, param_name:str, default_value:str, description:str) -> str:
        logging.debug("Getting setting value for %s", param_name)
        _env_var = param_name.upper().replace("-", "_").replace(".","_").replace("/", "_")

        logging.debug("Checking for environment variable %s", _env_var)
        _setting_value = os.environ.get(_env_var)

        _param_name = "/{}".format(APPLICATION_NAME)

        if _setting_value is None:
            logging.debug("Environment variable %s not found", _env_var)
            if self._parameter_client is not None:
                if self._env_prefix is not None:
                    _param_name = "{}/{}".format(_param_name, self._env_prefix)
                
                _param_name = "{}/{}".format(_param_name, param_name)
                try:
                    logging.debug("Getting value of %s from %s", param_name, _param_name)
                    _setting_value = self._parameter_client.get_value(_param_name)
                except ParameterNotFoundException:
                    logging.debug("Creating parameter %s with value %s", _param_name, default_value)
                    self._parameter_client.put_parameter(
                        name=_param_name,
                        value=default_value,
                        description=description
                    )
        
        if _setting_value is None:
            logging.debug("Setting value for %s not found, using default: %s", param_name, default_value)
            _setting_value = default_value

        return _setting_value

    def _get_log_level(self, param_prefix:str = None):
        _log_level = None

        _log_level_str = self._get_setting(
            param_name="log-level",
            default_value=self.DEFAULT_LOG_LEVEL,
            description="Log Level for {}".format(APPLICATION_NAME),
        ).lower()

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
        
        if isinstance(_log_level, tuple):
            _log_level = _log_level[0]

        return _log_level

    def _get_features(self) -> list:
        _return_features = []
        _features = {'user-icon': "display a user icon"}

        for feature, description in _features.items():
            _feature_val = self._get_setting(
                param_name='feature/{}'.format(feature),
                default_value="off",
                description=description
            ).lower()

            if _feature_val == "on":
                _return_features.append(feature)

        return _return_features

    @staticmethod
    def get_log_handlers(log_level:int) -> list:
        _handlers = []

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        if log_level == logging.DEBUG:
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")

        _stream_handler = logging.StreamHandler()
        _stream_handler.setLevel(log_level)
        _stream_handler.setFormatter(formatter)

        _handlers.append(_stream_handler)
        return _handlers