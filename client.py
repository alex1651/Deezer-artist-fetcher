# -*- coding: utf-8
"""
Implements a client class to query the
`Deezer API <http://developers.deezer.com/api>`_
"""

from __future__ import unicode_literals, absolute_import

import requests
from six.moves.urllib.parse import urlencode

# from deezer.resources import Album, Artist, Comment, Genre
# from deezer.resources import Chart, Resource
# from deezer.resources import Playlist, Radio, Track, User


class Client(object):
    """
    A client to retrieve some basic infos about Deezer resourses.
    Create a client instance with the provided options. Options should
    be passed in to the constructor as kwargs.
        # >>> import deezer
        # >>> client = deezer.Client(app_id='foo', app_secret='bar')
    This client provides several method to retrieve the content of most
    sort of Deezer objects, based on their json structure.
    """

    use_ssl = True
    host = "api.deezer.com"

    objects_types = {
        'search': None,

    }

    def __init__(self, **kwargs):
        super(Client, self).__init__()

        self.use_ssl = kwargs.get('use_ssl', self.use_ssl)
        self.host = kwargs.get('host', self.host)
        self.session = requests.Session()
        self.options = kwargs
        self._authorize_url = None

        self.app_id = kwargs.get('app_id')
        self.app_secret = kwargs.get('app_secret')
        self.access_token = kwargs.get('access_token')


    @staticmethod
    def make_str(value):
        """
        Convert value to str in python2 and python3 compatible way
        :returns: str instance
        """
        try:  # pragma: no cover - python 3
            value = str(value)
        except UnicodeEncodeError:  # pragma: no cover - python 2
            value = value.encode('utf-8')
        return value

    @property
    def scheme(self):
        """
        Get the http prefix for the address depending on the use_ssl attribute
        """
        return self.use_ssl and 'https' or 'http'

    def url(self, request=''):
        """Build the url with the appended request if provided."""
        if request.startswith('/'):
            request = request[1:]
        return "{0}://{1}/{2}".format(self.scheme, self.host, request)

    def object_url(self, object_t, object_id=None, relation=None, **kwargs):
        """
        Helper method to build the url to query to access the object
        passed as parameter
        :raises TypeError: if the object type is invalid
        """
        if object_t not in self.objects_types:
            raise TypeError("{0} is not a valid type".format(object_t))
        request_items = (object_t, object_id, relation)
        request_items = (item for item in request_items if item is not None)
        request_items = (str(item) for item in request_items)
        request = '/'.join(request_items)
        base_url = self.url(request)
        if self.access_token is not None:
            kwargs['access_token'] = self.make_str(self.access_token)
        if kwargs:
            for key, value in kwargs.items():
                if not isinstance(value, str):
                    kwargs[key] = self.make_str(value)
            result = '{0}?{1}'.format(base_url, urlencode(kwargs))
        else:
            result = base_url
        return result

    def get_object(self, object_t, object_id=None, relation=None, parent=None,
                   **kwargs):
        """
        Actually query the Deezer API to retrieve the object
        :returns: json dictionary
        """
        # url = self.object_url(object_t, object_id, relation, **kwargs)
        url = "https://api.deezer.com/search?q="+kwargs['q']
        # print(url)
        response = self.session.get(url)
        return response


    def search(self, query, relation=None, **kwargs):
        """
        Search track, album, artist or user
        :returns: a list of :class:`~deezer.resources.Resource` objects.
        """
        return self.get_object("search", relation=relation, q=query, **kwargs)