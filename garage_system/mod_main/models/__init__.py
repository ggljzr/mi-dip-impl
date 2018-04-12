from garage_system import scheduler, db, config_manager
from .garage import Garage

from ..filters import Filters
from ..sms_utils import send_sms

scheduler.add_job(Garage.check_reports, 'interval', minutes=1)

@db.event.listens_for(Garage.state, 'set', named=True)
def send_notification(**kwargs):

    if kwargs['value'] == kwargs['oldvalue']:
        # do nothing since state is unchanged
        return

    # if new state is ok do nothing
    if kwargs['value'] == Garage.STATE_OK:
        return

    # get string representation of garage state
    state = Filters.garage_state_filter(kwargs['value'])

    user_phone = config_manager.read_phone()
    text = 'Změna stavu garáže : {} (id={}), stav: {}'.format(kwargs['target'].tag,
                                                              kwargs['target'].id, state)
    send_sms(user_phone, text)

    garage_phone = kwargs['target'].phone
    text = 'Změna stavu Vaší garáže : {}! Volejte spravce na {}'.format(
        state, user_phone)
    send_sms(garage_phone, text)

