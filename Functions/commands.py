def help_cmd():
    msg = ("```"
           "===Thank you for choosing Aiko, property of Helios==="
           "\nCheck number of people Online/Idle/Offline  :   server report"
           "\nJoin VC   :   join"
           "\nLeave VC  :   leave"
           "\nText to Speech    :   tts"
           "\nList Music Queue  :   queue"
           "\nClear Music Queue     :   clear"
           "```")
    return msg


def server_report_cmd(online, idle, offline, server):
    msg = (f"```"
           f"Online: {online} \n"
           f"Idle/Busy: {idle} \n"
           f"Offline: {offline} \n"
           f"Members: {server.member_count}"
           f"```")
    return msg


class TextToSpeech:
    def __init__(self, msg):
        from gtts import gTTS
        self.language = 'ja'
        self.text = msg
        self.tts = gTTS(''.join(self.text[1:]), lang=self.language)

    def save(self, fname):
        self.tts.save(fname)


class Music:
    def __init__(self, music_queue, music_name, ydl_opts):
        self.music_queue = music_queue
        self.music_name = music_name
        self.ydl_opts = ydl_opts

    def play(self, content):
        import yt_dlp
        self.link = content[1]
        self.music_queue.append(self.link)
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.link, download=False)
            video_title = info_dict.get('title', None)
            self.music_name[self.link] = video_title

    def queue(self):
        queue = '\n'.join(self.music_name.values())
        if len(self.music_queue) > 0:
            msg = ("```"
                   "====Your music queue====\n" + queue + "\n========================"
                   "```")
            return msg
        else:
            msg = "Sorry, there is nothing in the queue at the moment"
            return msg


class HandleExceptions:
    #Error A_1 : Server Error
    #Error B_1 : Client Error
    #Error E_1A : Experimental Error

    class ServerError:
        def default_unknown_error(error):
            msg = "Error A_1, Server Error. Sorry something must have happened, try again later"
            return msg

    class ClientError:
        def vc_error(error):
            msg = "Error B_1, Client Error. You have to be in a VC for me to join"
            return msg

    class experimental_error:
        def default_unknown_error(error):
            msg = "Error E-1A, Experimental Error. Please Retry."
            return msg

