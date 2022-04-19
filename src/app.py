import logging
import argparse

from app_config import AppConfig
import user_service
from lib.parameters import AWSParameter
from http.server import HTTPServer

def get_arguments():
    parser = argparse.ArgumentParser(description="A test application for cloudbee's demo")
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Display debug messages')
    parser.add_argument('--aws',
                        action='store_true',
                        help="Application is running in AWS")
    parser.add_argument('-p', '--port',
                        action="store",
                        default="8080",
                        help="TCP Port for application to listen")
    parser.add_argument('-l', '--listen-addr',
                        action="store",
                        default="0.0.0.0",
                        help="Listening Address")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_arguments()

    initial_log_level = logging.INFO
    if args.debug:
        initial_log_level = logging.DEBUG

    #logging.basicConfig(format=AppConfig.get_log_format(initial_log_level),
    #                    level=initial_log_level)

    _handlers = AppConfig.get_log_handlers(initial_log_level)
    logging.basicConfig(level=initial_log_level,
                        handlers=_handlers)
    logging.info("LogLevel set to %s", initial_log_level)
    parameter_client = None

    if args.aws:
        logging.info("Application is running in AWS")
        logging.debug("Generating AWS Parameter Client")
        parameter_client = AWSParameter()

    logging.debug("Generating Application configuration")
    _config = AppConfig(parameter_client=parameter_client,
                        debug=args.debug)

    logging.info("Setting log level to %s", _config.log_level)
    logging.basicConfig(level=_config.log_level, handlers=_config.log_handlers)
    logging.info("Starting HTTP Server on %s", args.port)

    user_service.config = _config
    webserver = HTTPServer((args.listen_addr, int(args.port)), user_service.UserService)

    try:
        webserver.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webserver.server_close()
    logging.info("Exiting")