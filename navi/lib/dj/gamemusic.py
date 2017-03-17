import psycopg2
from random import randint
import pdb

SQL_ENTRY_EXISTS = """
    SELECT
      1
    FROM
      gamemusic
    WHERE
      title=%s;
"""

SQL_ADD_ENTRY = """
    INSERT INTO
      gamemusic (title, url)
    VALUES
      (%s, %s);
"""

SQL_GET_RANDOM = """
    SELECT
      *
    FROM
      gamemusic;
"""

class DJ:
    try:
        navi_conn = psycopg2.connect(
            database='navidb',
            user='navidb',
            host='127.0.0.1',
            password='navidb'
        )
        navi_cur = navi_conn.cursor()
    except:
        print("Could not connect to db")

    def connected(self):
        if self.navi_conn and self.navi_curr:
            return True
        else:
            return False

    def close(self):
        self.navi_cur.close()
        self.navi_conn.commit()
        self.navi_conn.close()

    def entry_exists(self, url):
        if self.connected:
            self.navi_cur.execute(SQL_ENTRY_EXISTS, (url,))
            res = self.navi_cur.fetchone()
        return res

    def add_entry(self, options):
        j = 0
        title = ""
        while j < len(options)-1:
            if j < len(options)-2:
                title += options[j] + " "
            else:
                title += options[j]
            j += 1
        url = str(options[-1])
        if self.connected and not self.entry_exists(url):
            self.navi_cur.execute(SQL_ADD_ENTRY, (title, url))
            if self.navi_cur.statusmessage == "INSERT 0 1":
                return ("{title} is now part of the music list").format(title=title)
            else:
                return "Failure"
        else:
            return "Failure"

    def get_random(self):
        if self.connected:
            self.navi_cur.execute(SQL_GET_RANDOM)
            res = self.navi_cur.fetchall()

            if res:
                index = randint(0,len(res)+1) % len(res)
            else:
                return "I don't know anything about that.\nAdd a song by inserting a title and a url\n Example \t\t!gamemusic title url"

        return ("{title}  -  {url}").format(title=res[index][0], url=res[index][1])
