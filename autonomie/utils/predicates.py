# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import time
from hashlib import md5
import logging


logger = logging.getLogger(__name__)

# 30 minutes tolerance (vms can be late ...)
DEFAULT_TOLERANCE = 60 * 30


class SettingHasValuePredicate(object):
    """
    Custom view predicate allowing to declare views only if a setting is set
    """
    def __init__(self, val, config):
        self.name, self.value = val
        if not isinstance(self.value, bool):
            raise ValueError("Only boolean values supported")

    def text(self):
        return u'if_setting_has_value = {0} == {1}'.format(
            self.name, self.value)

    phash = text

    def __call__(self, context, request):
        settings = request.registry.settings

        isin = self.name in settings
        return isin == self.value


def get_timestamp_from_request(request):
    """
    Retrieve a timestamp in the request's headers

    :param obj request: The Pyramid request object
    :returns: A timestamp
    :rtype: int
    """
    result = None
    if 'timestamp' in request.headers:
        result = request.headers.get('timestamp')
    elif 'Timestamp' in request.headers:
        result = request.headers.get('Timestamp')
    else:
        logger.error("No timestamp header found in the request")
        logger.error(request.headers.items())
        raise KeyError(u"No timestamp header found")

    return result


def check_timestamp(timestamp, tolerance=DEFAULT_TOLERANCE):
    """
    Check that a timestamp is 'actual' it doesn't differ from now too much

    :param str timestamp: A time stamp in string format
    :param int tolerance: The difference we accept between now and the given
    timestamp (request original time)
    :returns: True if the timestamp is close enough
    :rtype: bool
    """
    timestamp = float(timestamp)
    current_second = time.time()
    return abs(timestamp - current_second) < tolerance


def get_clientsecret_from_request(request):
    """
    Retrieve a client secret from the request headers
    Authorization and authorization headers are checked

    :param obj request: The Pyramid request object
    :returns: An encoded client secret
    :rtype: str
    """
    auth = ""
    if 'Authorization' in request.headers:
        auth = request.headers.get('Authorization')
    elif 'authorization' in request.headers:
        auth = request.headers.get('authorization')
    else:
        logger.error('No authorization header found')
        logger.error(request.headers.items())
        raise KeyError(u"No Authorization header found")

    parts = auth.split()
    if len(parts) != 2:
        logger.error(u"Invalid Authorization header")
        logger.error(auth)
        raise KeyError(u"Invalid Authorization header")

    token_type = parts[0].lower()
    if token_type != 'hmac-md5':
        logger.error(u"Invalid token type")
        logger.error(token_type)
        raise ValueError(u"Invalid token format %s" % token_type)
    else:
        client_secret = parts[1]
    return client_secret


def check_secret(client_secret, timestamp, api_key):
    """
    Check the client_secret matches

    :param str client_secret: The client secret sent by the client app
    :param int timestamp: The time stamp provided with the key
    :param str api_key: The configured api_key
    :returns: True/False
    :rtype: bool
    """
    secret = u"{0}-{1}".format(timestamp, api_key)
    encoded = md5(secret).hexdigest()
    if encoded != client_secret:
        return False
    return True


class ApiKeyAuthenticationPredicate(object):
    """
    Custom view predicate validating the api key "key" passed in the headers

    api key can be set in the ini file under autonomie.apikey

    the client app should :

        1- encode the api key with md5 then concatenate it with
    a salt grain and a timestamp then encode the key again
        2- Send the hash in the request header and the timestamp as request.GET
        param


    This predicate check the salt matches the apikey
    It also checks the timestamp is not too far from the current time
    """
    def __init__(self, val, config):
        self.key = val

    def text(self):
        return "Api Key Authentication = {0}".format(self.key)

    phash = text

    def _find_api_key(self, request):
        """
        Try to retrieve the api key from the current registry's settings
        """
        api_key = None
        if self.key in request.registry.settings:
            api_key = request.registry.settings[self.key]
        return api_key

    def __call__(self, context, request):
        """
        1- find the salt key in the headers
        2- check the timestamp
        3- check the salt
        4- True/False
        """
        logger.debug(u"Calling the api key predicate")
        timestamp = get_timestamp_from_request(request)

        if timestamp is None:
            logger.error(u"No timestamp provided in the headers")
            return False

        if not check_timestamp(timestamp):
            logger.error(
                u"Invalid timestamp current time is {0} while "
                u"timestamp is {1}".format(time.time(), timestamp)
            )
            return False

        client_secret = get_clientsecret_from_request(request)

        if client_secret is None:
            logger.error(u"No client secret provided in the headers")
            return False

        api_key = self._find_api_key(request)
        if api_key is None:
            return False

        if not check_secret(client_secret, timestamp, api_key):
            return False

        return True
