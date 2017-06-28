#!coding:utf8

from tornado.options import options, define

__all__ = ['init_app_settings', 'get_app_settings']

define('redis_host', default='172.16.1.21', help='redis server ip.', type=str)
define('redis_port', default=6379, help='redis server port.', type=int)
define('config',default=None,help="config file path",type=str)
_app_settings = {}
_cron_settings = {}


def init_app_settings():
    global _app_settings
    if _app_settings:
        return _app_settings
    options.parse_command_line(final=False)
    config_file_path = options.config
    if config_file_path:
        options.parse_config_file(config_file_path, final=False)
    options.parse_command_line(final=False)
    options.run_parse_callbacks()
    _app_settings = options.as_dict()
    return _app_settings


def get_app_settings():
    global _app_settings
    if not _app_settings:
        _app_settings = init_app_settings()
    return _app_settings

if __name__ == "__main__":
    print init_app_settings()