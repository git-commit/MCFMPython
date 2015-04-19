import socket
import getpass
import os
import os.path
import re


def main():
    header()

    fileprompt()
    fileloc = input("File path: ")

    if (os.path.isfile(fileloc)) != 1:
        print("File does not exist. Creating.")
        open(fileloc, 'w+')

    NICK = input("Enter your username: ")

    CHANNEL = "#" + input("Enter the channnel you would like to join (eg. Monstercat): ")

    print("Right click and paste your oauth key beginning with \"oath:\""),
    PASSWORD = getpass.getpass('(hidden):')

    HOST = "irc.twitch.tv"
    PORT = 6667
    IDENT = NICK
    REALNAME = NICK

    print("Connecting...")
    s = socket.socket()
    s.connect((HOST, PORT))
    sendIRC("PASS %s\r\n" % PASSWORD, s)
    sendIRC("NICK %s\r\n" % NICK, s)
    sendIRC("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), s)
    sendIRC("JOIN %s\r\n" % CHANNEL, s)

    substring = ":monstercat!monstercat@monstercat.tmi.twitch.tv PRIVMSG " + \
        CHANNEL + " :Now Playing:"

    styleprompt()

    instyle = input("Style: ")
    style = int(instyle)
    caps = input("All caps? (y/n): ")
    uppercase_output = caps is "y"

    belowline()
    sendIRC("PRIVMSG " + CHANNEL + " :!song\r\n", s)
    currentsongartist = ""

    while 1:
        readbuffer = (s.recv(1024)).decode("utf-8")
        if readbuffer.find(substring) != -1:
            song, artist = re.search(
                'Now Playing: (.*) by (.*) - Listen', readbuffer).groups()

            songartist = get_styled_output(style, song, artist, uppercase_output)

            if currentsongartist != songartist:
                print(songartist)
                with open(fileloc, 'r+') as f:
                    f.seek(0)
                    f.write(songartist)
                    f.truncate()
                currentsongartist = songartist


def header():
    print("       __  ___                 __                       __      ________  ___   ", end='')
    print("      /  \/  /___  ____  _____/ /____  ______________ _/ /_    / ____/  \/  /   ", end='')
    print("     / /\_/ / __ \/ __ \/ ___/ __/ _ \/ ___/ ___/ __ `/ __/   / /_  / /\_/ /    ", end='')
    print("    / /  / / /_/ / / / (__  ) /_/  __/ /  / /__/ /_/ / /_    / __/ / /  / /     ", end='')
    print("   /_/  /_/\____/_/ /_/____/\__/\___/_/   \___/\__,_/\__/   /_/   /_/  /_/      ", end='\n')
    print("Created by thinkaliker                                  [http://thinkaliker.com]", end='')
    print("       and rhoCode                                          [http://rhocode.com]", end='')
    print("Source available on GitHub            [http://github.com/thinkaliker/MCFMPython]", end='')
    print("////////////////////////////////////////////////////////////////////////////////")


def belowline():
    print("Songs will appear below.")
    print("================================================================================")


def styleprompt():
    print("Text output styles")
    print("----------------------")
    print(" [1]  Artist // Song")
    print(" [2]  Song // Artist")
    print(" [3]  Artist - Song")
    print(" [4]  Song - Artist")


def fileprompt():
    print(
        "Enter your text file output location (Somewhere on C:\ recommended)")


def get_styled_output(style, song, artist, uppercase):
    if uppercase:
        song = song.upper()
        artist = artist.upper()

    styles = {
        1: (" %s // %s " % (artist, song)),
        2: (" %s // %s " % (song, artist)),
        3: (" %s - %s " % (artist, song)),
        4: (" %s - %s " % (song, artist)),
    }
    return styles[style]


def sendIRC(stuff, t):
    t.send(stuff.encode('utf-8'))


if __name__ == '__main__':
    main()
