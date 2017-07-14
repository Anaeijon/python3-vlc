"""
VLC api connector for Python 3.6.

This can make use of vlc 'http' or 'rc' api.
It starts a vlc instance automatically if it doesn't allready exists in a
    specific linux-sceen using the subprocess library.

All of this should work without the need of installing additional libraries.
Requiers Python >=3.6

Written by David Döring (https://github.com/Anaeijon)
    with ideas from a script by Marios Zindilis
    https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html

Some documentation about the vlc api uses:
"There is a set of remote-control commands for VLC over HTTP.
This is probably the most convenient and reliable interface for developers to
    use to control VLC.
The commands ARE listed - but the list is tucked away in a README file, in the
    http subfolder of the little HTTP server under the VLC executables folder."
(VLC-Wiki)
I found it in my local installation at:
    /usr/share/vlc/lua/http/requests/README.txt
It is aviable in a subfolder of the official VLC repository:
    github.com/videolan/vlc/blob/master/share/lua/http/requests/README.txt

All usable commands for the 'RC'-Interface are aviable after running vlc -I rc
    and executing the 'help' command in the RC enviroment:
  +----[ CLI commands ]
  | add XYZ  . . . . . . . . . . . . . . . . . . . . add XYZ to playlist
  | enqueue XYZ  . . . . . . . . . . . . . . . . . queue XYZ to playlist
  | playlist . . . . . . . . . . . . .  show items currently in playlist
  | search [string]  . .  search for items in playlist (or reset search)
  | delete [X] . . . . . . . . . . . . . . . . delete item X in playlist
  | move [X][Y]  . . . . . . . . . . . . move item X in playlist after Y
  | sort key . . . . . . . . . . . . . . . . . . . . . sort the playlist
  | sd [sd]  . . . . . . . . . . . . . show services discovery or toggle
  | play . . . . . . . . . . . . . . . . . . . . . . . . . . play stream
  | stop . . . . . . . . . . . . . . . . . . . . . . . . . . stop stream
  | next . . . . . . . . . . . . . . . . . . . . . .  next playlist item
  | prev . . . . . . . . . . . . . . . . . . . .  previous playlist item
  | goto, gotoitem . . . . . . . . . . . . . . . . .  goto item at index
  | repeat [on|off]  . . . . . . . . . . . . . .  toggle playlist repeat
  | loop [on|off]  . . . . . . . . . . . . . . . .  toggle playlist loop
  | random [on|off]  . . . . . . . . . . . . . .  toggle playlist random
  | clear  . . . . . . . . . . . . . . . . . . . . .  clear the playlist
  | status . . . . . . . . . . . . . . . . . . . current playlist status
  | title [X]  . . . . . . . . . . . . . . set/get title in current item
  | title_n  . . . . . . . . . . . . . . . .  next title in current item
  | title_p  . . . . . . . . . . . . . .  previous title in current item
  | chapter [X]  . . . . . . . . . . . . set/get chapter in current item
  | chapter_n  . . . . . . . . . . . . . .  next chapter in current item
  | chapter_p  . . . . . . . . . . . .  previous chapter in current item
  |
  | seek X . . . . . . . . . . . seek in seconds, for instance `seek 12'
  | pause  . . . . . . . . . . . . . . . . . . . . . . . .  toggle pause
  | fastforward  . . . . . . . . . . . . . . . . . . set to maximum rate
  | rewind . . . . . . . . . . . . . . . . . . . . . set to minimum rate
  | faster . . . . . . . . . . . . . . . . . .  faster playing of stream
  | slower . . . . . . . . . . . . . . . . . .  slower playing of stream
  | normal . . . . . . . . . . . . . . . . . .  normal playing of stream
  | rate [playback rate] . . . . . . . . . .  set playback rate to value
  | frame  . . . . . . . . . . . . . . . . . . . . . play frame by frame
  | fullscreen, f, F [on|off]  . . . . . . . . . . . . toggle fullscreen
  | info . . . . . . . . . . . . .  information about the current stream
  | stats  . . . . . . . . . . . . . . . .  show statistical information
  | get_time . . . . . . . . .  seconds elapsed since stream's beginning
  | is_playing . . . . . . . . . . . .  1 if a stream plays, 0 otherwise
  | get_title  . . . . . . . . . . . . . the title of the current stream
  | get_length . . . . . . . . . . . .  the length of the current stream
  |
  | volume [X] . . . . . . . . . . . . . . . . . .  set/get audio volume
  | volup [X]  . . . . . . . . . . . . . . .  raise audio volume X steps
  | voldown [X]  . . . . . . . . . . . . . .  lower audio volume X steps
  | achan [X]  . . . . . . . . . . . .  set/get stereo audio output mode
  | atrack [X] . . . . . . . . . . . . . . . . . . . set/get audio track
  | vtrack [X] . . . . . . . . . . . . . . . . . . . set/get video track
  | vratio [X] . . . . . . . . . . . . . . .  set/get video aspect ratio
  | vcrop, crop [X]  . . . . . . . . . . . . . . . .  set/get video crop
  | vzoom, zoom [X]  . . . . . . . . . . . . . . . .  set/get video zoom
  | vdeinterlace [X] . . . . . . . . . . . . . set/get video deinterlace
  | vdeinterlace_mode [X]  . . . . . . .  set/get video deinterlace mode
  | snapshot . . . . . . . . . . . . . . . . . . . . take video snapshot
  | strack [X] . . . . . . . . . . . . . . . . .  set/get subtitle track
  |
  | vlm  . . . . . . . . . . . . . . . . . . . . . . . . .  load the VLM
  | description  . . . . . . . . . . . . . . . . .  describe this module
  | help, ? [pattern]  . . . . . . . . . . . . . . . . .  a help message
  | longhelp [pattern] . . . . . . . . . . . . . . a longer help message
  | lock . . . . . . . . . . . . . . . . . . . .  lock the telnet prompt
  | logout . . . . . . . . . . . . . .  exit (if in a socket connection)
  | quit . . . . . . . .  quit VLC (or logout if in a socket connection)
  | shutdown . . . . . . . . . . . . . . . . . . . . . . .  shutdown VLC
  +----[ end of help ]

"""

import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 6:
    print("This script requires Python version 3.6")
    sys.exit(1)

import socket
import requests
import subprocess
from typing import List, NewType


class MRL:
    """
    MRL (Media Resource Locator) construction class for VLC.

    See: https://wiki.videolan.org/Media_resource_locator/
    [[access][/demux]://]URL[#[title][:chapter][-[title][:chapter]]]
    [:option=value ...]
    """

    AccessType = NewType('AccessType', str)
    CDDA = AccessType('cdda')  # CD Digital Audio
    DIR = AccessType('dir')  # Filesystem-based directory
    DV = AccessType('dv')  # Digital Video/FireWire
    DVD = AccessType('dvd')  # DVD
    FILE = AccessType('file')  # Filesystem-based file
    FTP = AccessType('ftp')  # FTP
    GNOMEVFS = AccessType('gnomevfs')  # GnomeVFS
    HTTP = AccessType('http')  # HTTP
    MMS = AccessType('mms')  # Microsoft Media Server
    PVR = AccessType('pvr')  # PVR
    RTP = AccessType('rtp')  # RTP
    RTSP = AccessType('rtsp')  # RTSP
    SIMPLEDVD = AccessType('simpledvd')  # play DVD-Video, bypassing menu
    SMB = AccessType('smb')  # Server Message Block
    TCP = AccessType('tcp')  # TCP
    UDP = AccessType('udp')  # UDP
    VCDX = AccessType('vcdx')  # Video CD
    VLC = AccessType('vlc')  # commands to VLC itself

    def __init__(self,
                 access: AccessType,
                 url: str,
                 demux: str=None,
                 title: int=None,
                 chapter: int=None,
                 endtitle: int=None,
                 endchapter: int=None,
                 options: List[str]=None) -> None:
        """Construct a Media Source Locator for VLC."""
        self.access = access
        self.url = url
        self.demux = demux
        self.title = title
        self.chapter = chapter
        self.endtitle = endtitle
        self.endchapter = endchapter
        self.options = options

    def __str__(self) -> str:
        """
        MRL to String.

        Turn the gathered information into a MRL-String following the
            VLC-MRL-Specification from:
            https://wiki.videolan.org/Media_resource_locator/

            # !!! mostly untested !!!
        """
        outstr = self.access
        if self.demux is not None:
            outstr += "/" + self.demux
        outstr += "://" + self.url
        if self.title is not None or \
           self.chapter is not None or \
           self.endtitle is not None or \
           self.endchapter is not None:
            outstr += '#'
            if self.title is not None:
                outstr += self.title
            if self.chapter is not None:
                outstr += ":" + self.chapter
            if self.endtitle is not None or \
               self.endchapter is not None:
                outstr += '-'
            if self.endtitle is not None:
                outstr += self.endtitle
            if self.endchapter is not None:
                outstr += ':' + self.endchapter
        if self.options is not None:
            for option in self.options.items():
                outstr += ' :' + option
        return outstr


class VLC:
    """VLC remote controll class."""

    HTTP = 'http'
    RC = 'rc'

    def __init__(self,
                 screen_name='vlc_screen',
                 interfaces=['http'],
                 http_host='localhost',
                 http_port=8080,
                 http_password='pass',
                 rc_host='localhost',
                 rc_port=8888,
                 aout=None,
                 vout=None):
        """
        Create a connection to VLC-Player.

        If VLC-Player is running in a linux-screen with name from <screen_name>
            this Object will establis a connection to VLC.
        If there is no screen <screen_name>, a new screen will be started
            VLC-Player as specified.
        The Interfaces can be specified in the <interfaces>-array. There should
            be either 'http' or 'rc' in the <interfaces>-array to connect to.
        Currently using 'http' is highly recommended.
        """
        # interface http or/and rc allowed
        # http prefered
        self.SCREEN_NAME = screen_name
        self.HTTP_PASSWORD = http_password
        # convert string to list
        # interfaces = list(filter(
        #    lambda x:x!='', interfaces.lower().split(',')))

        if 'http' in interfaces:
            # http is default interface
            interfaces.remove('http')
            self.INTERFACE = self.HTTP
            self.HOST = http_host
            self.PORT = http_port
        elif 'rc' in interfaces:
            interfaces.remove('rc')
            self.INTERFACE = self.RC
            self.HOST = rc_host
            self.PORT = rc_port
        else:
            # use http anyway
            self.INTERFACE = self.HTTP
            self.HOST = http_host
            self.PORT = http_port

        cmd = subprocess.run(
            [
                'screen',
                '-ls',
                self.SCREEN_NAME,
            ], stdout=subprocess.DEVNULL)
        if cmd.returncode:
            self._vlc_log("starting vlc-player with rc interface")
            startup_commands = [
                'screen', '-dmS', self.SCREEN_NAME, 'vlc', '--intf',
                self.INTERFACE, '--extraintf', ','.join(interfaces),
                '--http-host', http_host, '--http-port',
                str(http_port), '--http-password', http_password, '--rc-host',
                '%s:%i' % (rc_host, int(rc_port))
            ]

            if aout is not None:
                startup_commands.append('--aout')
                startup_commands.append(aout)
            if vout is not None:
                startup_commands.append('--vout')
                startup_commands.append(vout)
            subprocess.run(startup_commands)

        # AF_INET --> .connect((HOST, PORT))

        self.SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                # retry connecting
                self.SOCK.connect((self.HOST, self.PORT))
            except ConnectionRefusedError:
                continue
            break
        # self.SOCK.settimeout(2)
        # try:
        #     for i in range(5):
        #         self._vlc_log(self.SOCK.recv(1024).decode('utf-8'))
        # except Exception:
        #     pass
        # self.SOCK.settimeout(1)

    def _rc_get(self, cmd, buffersize=0):
        """Prepare a command and send it to VLC."""
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)
        # allways read at least 2 bytes!
        answer = self.SOCK.recv(buffersize + 2)
        return answer.decode('utf-8').split('\r\n> ')[0]

    def _rc_send(self, cmd):
        """Prepare a command and send it to VLC."""
        if not cmd.endswith('\n'):
            cmd = cmd + '\n'
        cmd = cmd.encode()
        self.SOCK.sendall(cmd)

    def _http_get(self, cmd: str) -> requests.Response:
        get_url = 'http://%s:%i/%s' % (self.HOST, self.PORT, cmd)
        try:
            return requests.get(get_url, auth=('', self.HTTP_PASSWORD))
        except Exception as e:
            print("VLC HTTP interface not running at " + get_url)
            raise e
            return None

    def _http_request(self, cmd: str):
        # TODO: do some checks?
        return self._http_get("requests/status.json?command=%s" % cmd)

    def _vlc_log(self, text):
        print("VLC :  ", text)

    def _select_interface(self, rc_do, http_do, *args, **kwargs):
        if self.INTERFACE is self.RC:
            return rc_do(*args, **kwargs)
        elif self.INTERFACE is self.HTTP:
            return http_do(*args, **kwargs)
        else:
            raise ValueError("Interface not specified.", self.INTERFACE)

# | add XYZ  . . . . . . . . . . . . . . . . . . . . add XYZ to playlist

    def _rc_add(self, mrl: MRL):
        """
        Add <mrl> to playlist and start playback.

        MRL Fromat see: https://wiki.videolan.org/Media_resource_locator/
        """
        self._rc_send('add %s' % mrl)
        # recache playlist
        self.playlist()

    def _http_add(self, mrl: MRL):
        """Add <mrl> to playlist and start playback."""
        self._http_request("in_play&input=%s" % mrl)
        self.playlist()

    def add(self, mrl: MRL):
        """Add <mrl> to playlist and start playback."""
        self._select_interface(self._rc_add, self._http_add, mrl)

# | enqueue XYZ  . . . . . . . . . . . . . . . . . queue XYZ to playlist
# def _rc_enqueue_path(self, path: str):
#     for file in iglob(path + '/**/*.mp3', recursive=True):
#         self._rc_enqueue(file)
#     self.playlist()

# for fast enqueueing:

    def _rc_enqueue(self, mrl: MRL):
        self._rc_send('enqueue %s' % MRL)
        # recache playlist
        self.playlist()

    def _http_enqueue(self, mrl: MRL):
        """Add <mrl> to playlist."""
        self._http_request("in_enqueue&input=%s" % mrl)
        self.playlist()

    def enqueue(self, mrl: MRL):
        """Add <mrl> to playlist."""
        self._select_interface(self._rc_enqueue, self._http_enqueue, mrl)

# | playlist . . . . . . . . . . . . .  show items currently in playlist

    def _rc_playlist(self):
        plist = list()
        self._rc_clean_buffer()
        bufs = 67108864
        playlist_read = self._rc_get('playlist', buffersize=bufs).split('\r\n')
        startindex = 2
        endindex = -2
        for i in range(len(playlist_read)):
            if "| 2 -" in playlist_read[i]:
                startindex = i + 1
            elif "| 3 -" in playlist_read[i]:
                endindex = i
                break
        for entry in playlist_read[startindex:endindex]:
            # parsing output form:
            # |   14 - Titel (00:00:33) [played 1 time]
            splitted = entry.split(' ')
            if splitted[-3] == "[played":
                if (splitted[-4][0] != '(' or splitted[-4][-1] != ')' or
                        splitted[-4][3] != ':' or splitted[-4][6] != ':'):
                    try:
                        self._vlc_log("FOUND CORRUPTED ENTRY: %s" % entry)
                        self._vlc_log("DELETING")
                        self.delete(int(splitted[3]))
                        continue
                    except Exception:
                        self._vlc_log("PLAYLIST_READ: %s" % playlist_read)
                        self._vlc_log("PLAYLIST SERIOUSLY CORRUPTED!")
                        self._vlc_log("CLEARING PLAYLIST NOW!")
                        self._rc_clean_buffer()
                        self._rc_clean_buffer()
                        return None
                etime = [int(sp) for sp in splitted[-4][1:-1].split(':')]
                new_e = {
                    'id': int(splitted[3]),
                    'title': ' '.join(splitted[5:-4]),
                    'length': (etime[0] * 60 + etime[1]) * 60 + etime[2],
                    'played': int(splitted[-2])
                }
                plist.append(new_e)
            else:
                if (splitted[-1][0] != '(' or splitted[-1][-1] != ')' or
                        splitted[-1][3] != ':' or splitted[-1][6] != ':'):
                    try:
                        self._vlc_log("FOUND CORRUPTED ENTRY: %s" % entry)
                        self._vlc_log("DELETING")
                        self.delete(int(splitted[3]))
                        continue
                    except Exception:
                        self._vlc_log("PLAYLIST_READ: %s" % playlist_read)
                        self._vlc_log("PLAYLIST SERIOUSLY CORRUPTED!")
                        self._vlc_log("CLEARING PLAYLIST NOW!")
                        self._rc_clean_buffer()
                        self._rc_clean_buffer()
                        return None
                etime = [int(sp) for sp in splitted[-1][1:-1].split(':')]
                new_e = {
                    'id': int(splitted[3]),
                    'title': ' '.join(splitted[5:-1]),
                    'length': (etime[0] * 60 + etime[1]) * 60 + etime[2],
                    'played': 0
                }
                plist.append(new_e)
        self.cached_playlist = plist
        return plist

    def _http_full_playlist(self):
        return self._http_get("requests/playlist.json").json()

    def _http_playlist(self):
        full_pl = self._http_full_playlist()
        self.cached_playlist = full_pl['children'][0]['children']
        return self.cached_playlist

    def playlist(self):
        """Get the playlist."""
        return self._select_interface(self._rc_playlist, self._http_playlist)

    def get_cached_playlist(self):
        """
        Get the cached playlist.

        The playlist is cached every time it changes.
        This method returns the cached playlist or caches it, if there is no
         cached playlist available.
        """
        if self.cached_playlist is None:
            self.playlist()
        return self.cached_playlist

# | search [string]  . .  search for items in playlist (or reset search)

    def _rc_search(self, query):
        return self._rc_get('search %s' % query, buffersize=67108864)

# | delete [X] . . . . . . . . . . . . . . . . delete item X in playlist

    def _rc_delete(self, id: int):
        self._rc_send('delete %i' % id, buffersize=4096)
        # recache playlist
        self.playlist()

    def _http_delete(self, id: int):
        """
        Delete <id> form Playlist.

        Might not work as expected.
        HTTP README says:
         "NOTA BENE: pl_delete is completly UNSUPPORTED"
        But it seems to work for me for now.
        """
        self._http_request("pl_delete&id=%i" % id)
        self.playlist()

    def delete(self, id: int):
        """Delete item <id> from playlist."""
        self._select_interface(self._rc_delete, self._http_delete, id)

# | move [X][Y]  . . . . . . . . . . . . move item X in playlist after Y
# | sort key . . . . . . . . . . . . . . . . . . . . . sort the playlist

#   KEY: id, title, artist, genre, random, duration, album

    def _rc_sort(self, key: str):
        self._rc_send('delete %s' % key, buffersize=64)
        return self.playlist()

    def _http_sort(self, key: str):
        self._http_request("pl_sort&val=%s" % key)
        return self.playlist()

    def sort(self, key: str):
        """Sort playlist by sort mode <key>."""
        return self._select_interface(self._rc_sort, self._http_sort, key)

    def sort_id(self):
        """Sort playlist by id."""
        return self.sort('id')

    def sort_title(self):
        """Sort playlist by title."""
        return self.sort('title')

    def sort_artist(self):
        """Sort playlist by artist."""
        return self.sort('artist')

    def sort_genre(self):
        """Sort playlist by genre."""
        return self.sort('genre')

    def sort_random(self):
        """Randomize playlist order."""
        return self.sort('random')

    random_playlist = sort_random

    def sort_duration(self):
        """Sort playlist by duration."""
        self.sort('duration')

    def sort_album(self):
        """Sort playlist by album."""
        self.sort('album')

# | sd [sd]  . . . . . . . . . . . . . show services discovery or toggle
# | play . . . . . . . . . . . . . . . . . . . . . . . . . . play stream

    def _rc_play(self):
        self._rc_send('play')

    def _http_play(self):
        self._http_request('pl_play')

    def play(self):
        """Play last active item."""
        self._select_interface(self._rc_play, self._http_play)

# | stop . . . . . . . . . . . . . . . . . . . . . . . . . . stop stream

    def _rc_stop(self):
        self._rc_send('stop')

    def _http_stop(self):
        self._http_request('pl_stop')

    def stop(self):
        """Stop playback."""
        self._select_interface(self._rc_stop, self._http_stop)

# | next . . . . . . . . . . . . . . . . . . . . . .  next playlist item

    def _rc_next(self):
        self._rc_send('next')

    def _http_next(self):
        self._http_request('pl_next')

    def next(self):
        """Jump to next item in playlist."""
        self._select_interface(self._rc_next, self._http_next)

# | prev . . . . . . . . . . . . . . . . . . . .  previous playlist item

    def _rc_previous(self):
        self._rc_send('prev')

    def _http_previous(self):
        self._http_request('pl_previous')

    def previous(self):
        """Jump to previous item in playlist."""
        self._select_interface(self._rc_previous, self._http_previous)

# | goto, gotoitem . . . . . . . . . . . . . . . . .  goto item at index

    def _rc_goto(self, index):
        self._rc_send('goto %i' % (index, ))

# | repeat [on|off]  . . . . . . . . . . . . . .  toggle playlist repeat

    def _rc_repeat(self, repeat: bool):
        self._rc_send("repeat %s" % ("on" if repeat else "off"))

    def _http_repeat(self, repeat: bool):
        if self.status()['repeat'] ^ repeat:
            # toggle if current status and desired status differ
            self._http_request('pl_repeat')

    def repeat(self, repeat: bool):
        """Activate/Deactivate repeating."""
        self._select_interface(self._rc_repeat, self._http_repeat, repeat)

# | loop [on|off]  . . . . . . . . . . . . . . . .  toggle playlist loop

    def _rc_loop(self, loop: bool):
        self._rc_send("loop %s" % ("on" if loop else "off"))

    def _http_loop(self, loop: bool):
        if self.status()['loop'] ^ loop:
            # toggle if current status and desired status differ
            self._http_request('pl_loop')

    def loop(self, loop: bool):
        """Activate/Deactivate looping."""
        self._select_interface(self._rc_loop, self._http_loop, loop)

# | random [on|off]  . . . . . . . . . . . . . .  toggle playlist random

    def _rc_random(self, random: bool):
        self._rc_send("random %s" % ("on" if random else "off"))

    def _http_random(self, random: bool):
        if self.status()['random'] ^ random:
            # toggle if current status and desired status differ
            self._http_request('pl_random')

    def random(self, random: bool):
        """Activate/Deactivate random playback."""
        self._select_interface(self._rc_random, self._http_random, random)

# | clear  . . . . . . . . . . . . . . . . . . . . .  clear the playlist

    def _rc_clear(self):
        self._rc_send('clear')
        # recache playlist
        self.playlist()

    def _http_empty(self):
        self._http_request('pl_empty')
        self.playlist()

    def clear(self):
        """Empty the playlist."""
        self._select_interface(self._rc_clear, self._http_empty)

    # empty and clear do exactly the same!
    empty = clear

    # | status . . . . . . . . . . . . . . . . . . . current playlist status

    def _rc_status(self):
        return self._rc_get('status', buffersize=4096)

    def _http_status(self):
        return self._http_request("").json()

    def status(self):
        """Get vlc status information."""
        return self._select_interface(self._rc_status, self._http_status)

# | title [X]  . . . . . . . . . . . . . . set/get title in current item

    def _rc_set_title(self, title):
        return self.x('title %s' % (title, ), buffersize=4096)

# | title_n  . . . . . . . . . . . . . . . .  next title in current item
# | title_p  . . . . . . . . . . . . . .  previous title in current item
# | chapter [X]  . . . . . . . . . . . . set/get chapter in current item
# | chapter_n  . . . . . . . . . . . . . .  next chapter in current item
# | chapter_p  . . . . . . . . . . . .  previous chapter in current item
# |
# | seek X . . . . . . . . . . . seek in seconds, for instance `seek 12'

    def _rc_seek(self, time: int):
        self._rc_send('title %i' % int(time))

    def _http_seek(self, time: int):
        self._http_request('seek&val=%i' % int(time))

    def seek(self, time: int):
        """Seek in seconds (jump to position)."""
        self._select_interface(self._rc_seek, self._http_seek, time)

# | pause  . . . . . . . . . . . . . . . . . . . . . . . .  toggle pause

    def _rc_pause(self):
        self.x('pause')

    def _http_pause(self):
        self._http_request('pl_pause')

    def pause(self):
        """Pause playing title."""
        self._select_interface(self._rc_pause, self._http_pause)

# | fastforward  . . . . . . . . . . . . . . . . . . set to maximum rate
# | rewind . . . . . . . . . . . . . . . . . . . . . set to minimum rate
# | faster . . . . . . . . . . . . . . . . . .  faster playing of stream
# | slower . . . . . . . . . . . . . . . . . .  slower playing of stream
# | normal . . . . . . . . . . . . . . . . . .  normal playing of stream
# | frame  . . . . . . . . . . . . . . . . . . . . . play frame by frame
# | fullscreen, f, F [on|off]  . . . . . . . . . . . . toggle fullscreen
# | info . . . . . . . . . . . . .  information about the current stream
# | stats  . . . . . . . . . . . . . . . .  show statistical information
# | rate [playback rate] . . . . . . . . . .  set playback rate to value
# | get_time . . . . . . . . .  seconds elapsed since stream's beginning

    def _rc_get_time(self) -> int:
        return int(self._rc_get('get_time', buffersize=128))

    def _http_get_time(self) -> int:
        status = self._http_status()
        title_length = int(status['length'])
        position = float(status['position'])
        return int(title_length * position)

    def get_time(self) -> int:
        """Get seconds elapsed since stream's beginning."""
        return self._select_interface(self._rc_get_time, self._http_get_time)

    time = get_time

    def _rc_get_position(self) -> float:
        raise NotImplementedError("_rc_get_position is not implemented. " +
                                  "Use _rc_get_time or http instead.")
        # TODO: implement

    def _http_get_position(self) -> float:
        """Get position in current stream (between 0..1)."""
        return float(self._http_status()['position'])

    def get_position(self) -> float:
        """Get position in current stream (between 0..1)."""
        return self._select_interface(self._rc_get_position,
                                      self._http_get_position)

    position = get_position

    # | is_playing . . . . . . . . . . . .  1 if a stream plays, 0 otherwise
    # | get_title  . . . . . . . . . . . . . the title of the current stream

    def _rc_get_title(self):
        return self._rc_get('get_title', buffersize=1024)

    def _http_get_title_by_id(self, id) -> dict:
        """Search playlist for <id> and return corresponding title."""
        if int(id) == -1:
            # there is no title
            return None
        playl = self._http_playlist()
        return [title for title in playl if int(title['id']) == int(id)][0]

    def _http_get_current_id(self):
        """Get the it of currently playing title."""
        return self._http_request('').json()['currentplid']

    def _http_get_title(self) -> dict:
        return self._http_get_title_by_id(self._http_get_current_id())

    def get_title(self):
        """Return currently playing title."""
        return self._select_interface(self._rc_get_title, self._http_get_title)

# | get_length . . . . . . . . . . . .  the length of the current stream

    def _rc_get_length(self):
        return int(self._rc_get('get_title', buffersize=1024))

    def _http_get_length(self):
        return self._http_request('').json()['length']

    def length(self):
        """Get the length of playing title in seconds."""
        return self._select_interface(self._rc_get_length,
                                      self._http_get_length)

# | volume [X] . . . . . . . . . . . . . . . . . .  set/get audio volume

    def _rc_get_volume(self) -> int:
        return int(self._rc_get('volume', buffersize=4096))

    def _http_get_volume(self) -> int:
        return int(self._http_request('').json()['volume'])

    def get_volume(self) -> int:
        """Get the volume."""
        return self._select_interface(self._rc_get_volume,
                                      self._http_get_volume)

    def _rc_set_volume(self, volume) -> int:
        return int(self._rc_get('volume %i' % int(volume), buffersize=4096))

    def _http_set_volume(self, volume) -> int:
        self._http_request('volume&val=%i' % int(volume))
        # need to redo the request, because first request returns volume
        #  before change
        return self._http_get_volume()

    def set_volume(self, volume) -> int:
        """Set the volume."""
        return self._select_interface(self._rc_set_volume,
                                      self._http_set_volume, volume)

# | volup [X]  . . . . . . . . . . . . . . .  raise audio volume X steps

    def _rc_volup(self, x) -> int:
        return int(self._rc_get('volup %i' % (x), buffersize=1024))

    def _http_volup(self, x) -> int:
        self._http_request('volume&val=+%i' % int(x))
        return self._http_get_volume()

    def volup(self, x) -> int:
        """Increase the volume by x."""
        return self._select_interface(self._rc_volup, self._http_volup, x)

# | voldown [X]  . . . . . . . . . . . . . .  lower audio volume X steps

    def _rc_voldown(self, x) -> int:
        return int(self._rc_get('voldown %i' % (x), buffersize=1024))

    def _http_voldown(self, x) -> int:
        self._http_request('volume&val=-%i' % int(x))
        return self._http_get_volume()

    def voldown(self, x) -> int:
        """Decrease the volume by x."""
        return self._select_interface(self._rc_voldown, self._http_voldown, x)

# | achan [X]  . . . . . . . . . . . .  set/get stereo audio output mode
# | atrack [X] . . . . . . . . . . . . . . . . . . . set/get audio track
# | vtrack [X] . . . . . . . . . . . . . . . . . . . set/get video track
# | vratio [X] . . . . . . . . . . . . . . .  set/get video aspect ratio
# | vcrop, crop [X]  . . . . . . . . . . . . . . . .  set/get video crop
# | vzoom, zoom [X]  . . . . . . . . . . . . . . . .  set/get video zoom
# | vdeinterlace [X] . . . . . . . . . . . . . set/get video deinterlace
# | vdeinterlace_mode [X]  . . . . . . .  set/get video deinterlace mode
# | snapshot . . . . . . . . . . . . . . . . . . . . take video snapshot
# | strack [X] . . . . . . . . . . . . . . . . .  set/get subtitle track
# |
# | vlm  . . . . . . . . . . . . . . . . . . . . . . . . .  load the VLM
# | description  . . . . . . . . . . . . . . . . .  describe this module
# | help, ? [pattern]  . . . . . . . . . . . . . . . . .  a help message
# | longhelp [pattern] . . . . . . . . . . . . . . a longer help message
# | lock . . . . . . . . . . . . . . . . . . . .  lock the telnet prompt
# | logout . . . . . . . . . . . . . .  exit (if in a socket connection)
# | quit . . . . . . . .  quit VLC (or logout if in a socket connection)
# | shutdown . . . . . . . . . . . . . . . . . . . . . . .  shutdown VLC

    def _rc_shutdown(self):
        return ('Shutdown' in self.x('shutdown', buffersize=128))

# | clean - - - empty the recv buffer

    def _rc_clean_buffer(self):
        while True:
            try:
                self._vlc_log(" clean : " +
                              self.SOCK.recv(4096).decode('utf-8'))
            except Exception:
                break
