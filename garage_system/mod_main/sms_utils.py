import subprocess
import unicodedata
from sys import stderr

"""
Function wrapping gammu-smsd-inject command, used to send SMS.
Function fails silently when Gammu SMSD is not installed.

If clear_unicode is True, non-ascii characters are replaced
with their closest ascii equivalents, e.g. š -> s.

Returns True if sms was added to SMSD queue, False otherwise.
"""
def send_sms(phone, text, clear_unicode=True, debug_print=False):
    if debug_print:
        print('Sending SMS to: {}'.format(phone))
        print('SMS text: {}'.format(text))

    if phone is None:
        return False

    if phone is '':
        return False

    # try to send sms if gammu daemon is installed
    # recipe to change non ascii chars https://stackoverflow.com/a/2701901
    ascii_txt = text

    if clear_unicode == True:
        ascii_txt = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    
    try:
        subprocess.call(['gammu-smsd-inject', 'TEXT',
                         phone, '-text', ascii_txt])
    except FileNotFoundError:
        print('gammu-smsd-inject was not found', file=stderr)
        return False

    return True