import subprocess
import unicodedata

def send_sms(phone, text):
    if phone is not None:
        # try to send sms if gammu daemon is installed
        # recipe to change non ascii chars https://stackoverflow.com/a/2701901
        ascii_txt = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        try:
            subprocess.call(['gammu-smsd-inject', 'TEXT',
                             phone, '-text', ascii_txt])
        except FileNotFoundError:
            pass
