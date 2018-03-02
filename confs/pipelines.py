# -*- coding: utf-8 -*-

import sqlite3
import os
from confs.items import Session, Speaker

INIT_DB = '''
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    edition TEXT,
    title TEXT,
    summary TEXT,
    scheduled_at TIMESTAMP,
    location TEXT,
    level TEXT
);

CREATE TABLE speakers (
    id TEXT PRIMARY KEY,
    fullname TEXT,
    bio TEXT,
    country TEXT,
    personal_url TEXT,
    facebook TEXT,
    twitter TEXT,
    flickr TEXT
);

CREATE TABLE session_tags (
    session TEXT,
    tag TEXT,
    PRIMARY KEY (session, tag),
    FOREIGN KEY(session) REFERENCES sessions(id)
);

CREATE TABLE session_speakers (
    session TEXT,
    speaker TEXT,
    PRIMARY KEY (session, speaker),
    FOREIGN KEY(session) REFERENCES sessions(id)
);
'''


INSERT_SESSION = '''
INSERT OR REPLACE INTO sessions(
    id, edition, title, summary, scheduled_at, location, level
) VALUES (?, ?, ?, ?, ?, ?, ?)
'''

INSERT_SPEAKER = '''
INSERT OR REPLACE INTO speakers(
    id, fullname, bio, country, personal_url, facebook, twitter, flickr
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
'''

INSERT_SESSION_TAG = '''
INSERT OR REPLACE INTO session_tags(session, tag)
VALUES (?, ?)
'''

INSERT_SESSION_SPEAKER = '''
INSERT OR REPLACE INTO session_speakers(session, speaker)
VALUES (?, ?)
'''


class ConfsPipeline(object):

    def open_spider(self, spider):
        do_create = not os.path.isfile('./confs.db')
        self.db = sqlite3.connect('./confs.db')
        if do_create:
            self.db.executescript(INIT_DB)

    def process_item(self, item, spider):
        with self.db:
            if isinstance(item, Session):
                self.process_session(item)
            elif isinstance(item, Speaker):
                self.process_speaker(item)
        return item

    def process_session(self, item):
        self.db.execute(INSERT_SESSION, (
            item['id'],
            item['edition'],
            item['title'],
            item['summary'],
            item['scheduled_at'],
            item['location'],
            item['level'],
        ))

        for tag in item['tags']:
            self.db.execute(INSERT_SESSION_TAG, (item['id'], tag))
        for speaker in item['speakers']:
            self.db.execute(INSERT_SESSION_SPEAKER, (item['id'], speaker))

    def process_speaker(self, item):
        self.db.execute(INSERT_SPEAKER, (
            item['id'],
            item['fullname'],
            item['bio'],
            item['country'],
            item['personal_url'],
            item.get('facebook'),
            item.get('twitter'),
            item.get('flickr'),
        ))
