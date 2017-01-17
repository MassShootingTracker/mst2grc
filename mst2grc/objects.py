import json
import platform
import csv
from io import StringIO
import os
import requests
import datetime


class Config(object):

    def __init__(self, cfg_file):

        # Package information
        here = os.path.abspath(os.path.dirname(__file__))
        namespace = {}
        with open(os.path.join(here, os.path.pardir, 'package.py')) as f:
            exec(f.read(), namespace)
        self.author = namespace['__author__']
        self.name = namespace['APPNAME']
        self.version = namespace['__version__']

        # load configuration json file.
        with open(cfg_file) as f:
            jcfg = json.load(f)

        # Script variables.
        self.subreddit = jcfg['app']['subreddit']

        #login credentials
        self.client_id = jcfg['authentication']['client_id']
        self.client_secret = jcfg['authentication']['client_secret']
        self.refresh_token = jcfg['authentication']['refresh_token']
        self.redirect_uri = jcfg['authentication']['redirect_uri']
        self.scope = jcfg['authentication']['scope']

        #praw settings
        self.api_request_delay = jcfg['praw']['api_request_delay']
        self.useragent = "{}:{}:{} by {}".format(platform.system(), self.name, self.version, self.author)

        # data locations
        self.google_docs = jcfg['google_docs']
        self.wiki_pages = jcfg['wiki_pages']

        # Patterns for finding sidebar stat locations
        self.total_pattern = jcfg['sidebar']['total_pattern']
        self.current_year_pattern = jcfg['sidebar']['current_year_pattern']
        self.days_since_pattern = jcfg['sidebar']['days_since_pattern']

        # format strings
        self.title_md = jcfg['formatting']['title_md']
        self.url_md = jcfg['formatting']['url_md']


class Shooting(object):

    def __init__(self, rec):
        self.date = rec['date']
        self.shooters = ", ".join([x.strip() for x in rec['name_semicolon_delimited'].split(';')])
        self.killed = rec['killed']
        self.wounded = rec['wounded']
        self.city = rec['city']
        self.state = rec['state']
        self.sources = [x.strip() for x in rec['sources_semicolon_delimited'].split(';') if x.strip() != ""]


class MSTYear(object):

    title_md = None
    url_md = None

    def __init__(self, year, url):

        self.year = year
        self.url = url

        res = requests.get(url)
        f = StringIO(res.text)
        reader = csv.DictReader(f)
        self.shootings = []
        for row in reader:
            self.shootings.append(Shooting(row))

        self.list_md = self.__str__()

        self.total = len(self.shootings)
        self.days_since_last = self.days_since_most_recent()

    def days_since_most_recent(self):
        ret = None
        today = datetime.date.today()
        for shooting in self.shootings:
            d = datetime.datetime.strptime(shooting.date, "%m/%d/%Y").date()
            delta = today - d
            if ret is None or delta.days < ret:
                ret = delta.days
        return ret

    @classmethod
    def set_fmts(cls, title_template=None, url_template=None):
        cls.title_md = title_template
        cls.url_md = url_template

    def __iter__(self):
        for item in self.shootings:
            yield item

    def __str__(self):
        md = []
        for i, rec in enumerate(self.shootings):
            md.append(self.title_md.format(number=i + 1,
                                           date=rec.date,
                                           shooters=rec.shooters,
                                           killed=rec.killed,
                                           wounded=rec.wounded,
                                           city=rec.city,
                                           state=rec.state))
            for source in rec.sources:
                md.append(self.url_md.format(url=source))

            md.append('\n')

        return "".join(md)

    def __len__(self):
        return len(self.shootings)


class WikiYear(object):

    BEGINLIST = "[](#BEGINLIST)"
    ENDLIST = "[](#ENDLIST)"

    def __init__(self, content_md, list_md=None):
        self.content_md = content_md
        if list_md is not None:
            self.update(list_md)

    def update(self, new_list):
            new_content = []
            marker_found = False
            for line in self.content_md.split('\n'):
                if not marker_found:
                    new_content.append(line)
                if self.BEGINLIST in line:
                    marker_found = True
                    new_content.append('\n')
                    new_content.append(new_list)
                if self.ENDLIST in line:
                    new_content.append(self.ENDLIST)
                    marker_found = False
            new_content = "".join(new_content)
            self.content_md = new_content

    @classmethod
    def set_markers(cls, begin_marker, end_marker):
        cls.BEGINLIST = begin_marker
        cls.ENDLIST = end_marker

    def __str__(self):
        return self.content_md

