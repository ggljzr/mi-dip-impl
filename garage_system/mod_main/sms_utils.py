import subprocess

def send_sms(phone, text):
    if phone is not None:
        # try to send sms if gammu daemon is installed
        try:
            subprocess.call(['gammu-smsd-inject', 'TEXT',
                             phone, '-unicode', '-text', text])
        except FileNotFoundError:
            pass
