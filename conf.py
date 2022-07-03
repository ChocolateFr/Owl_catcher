from configparser import ConfigParser

def read_config():
    parser = ConfigParser()
    parser.read('bot.conf')
    class data:
        api_id = parser.get('base', 'api_id')
        api_hash = parser.get('base', 'api_hash')
        token = parser.get('base', 'token')
    return data