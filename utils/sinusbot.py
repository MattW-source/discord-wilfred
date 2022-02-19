import requests
import json

def time_phaser(seconds):
    output = ""
    print(seconds)
    m, s = divmod(seconds, 60)
    if m > 0:
        output = output + str(int(round(m, 0))) + ":"
    if s > 0:
        output = output + str(int(round(s, 0))) + ""
    return output

def login():
    r = requests.post("http://music.foggyio.uk:8087/api/v1/bot/login", data={"username":"automation", "password":"", "botId":"fb953982-7d4c-4e40-8052-31eca101b3fd"}, timeout=10.0)
    token = json.loads(r.text)["token"]
    return token

def playing():
    try:
        authToken = login()
        headers = {"authorization":"Bearer " + authToken}
        r = requests.get("http://music.foggyio.uk:8087/api/v1/bot/i/2c141bcb-73f0-4332-b93b-545000768cb5/status", headers=headers, timeout=10.0)
        version = json.loads(r.text)["v"]
        try:
            song = json.loads(r.text)["currentTrack"]["tempArtist"] + " - " + json.loads(r.text)["currentTrack"]["tempTitle"]
        except:
            song = json.loads(r.text)["currentTrack"]["artist"] + " - " + json.loads(r.text)["currentTrack"]["title"]
        try:
            duration = time_phaser(json.loads(r.text)["currentTrack"]["duration"]/1000)
        except:
            duration = "0:00"
        if json.loads(r.text)["currentTrack"]["title"] == "One World Radio":
            owr = True
        else:
            owr = False
        return [song, duration, version, owr]
    except: #In the event the music bot is not online or due to other unforeseen errors in which the expected response is not received.
        try:
            try:
                song = json.loads(r.text)["currentTrack"]["temptitle"]
            except:
                song = json.loads(r.text)["currentTrack"]["title"]
            if json.loads(r.text)["currentTrack"]["title"] == "One World Radio":
                owr = True
            else:
                owr = False
            try:
                duration = time_phaser(json.loads(r.text)["currentTrack"]["duration"]/1000)
            except:
                duration = "0:00"
                return [song, duration, version, owr]
        except: #In the event of a completely unexpected error
            return None
