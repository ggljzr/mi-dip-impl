import subprocess

def send_sms(phone, text):
    if phone is not None:
        # try to send sms if gammu daemon is installed
        uni = text.encode('utf-8')
        try:
            subprocess.call(['gammu-smsd-inject', 'TEXT',
                             phone, '-unicode', '-text', uni])
        except FileNotFoundError:
            pass
