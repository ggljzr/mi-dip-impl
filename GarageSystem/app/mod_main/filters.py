from .models.event import Event
from .models.garage import Garage

class Filters():
    def date_filter(date):
        if date == None:
            return 'Žádné'

        return date

    def garage_doors_filter(doors):
        if doors == Garage.DOORS_OPEN:
            return 'Otevřeno'

        if doors == Garage.DOORS_CLOSED:
            return 'Zavřeno'

        return 'Nedefinováno'

    def garage_state_filter(state):
        if state == Garage.STATE_OK:
            return 'OK'

        if state == Garage.STATE_NOT_RESPONDING:
            return 'Nehlásí se'

        if state == Garage.STATE_SMOKE:
            return 'Detekce kouře'

        if state == Garage.STATE_MOVEMENT:
            return 'Detekce pohybu'

        return 'Nedefinováno'
        
    def event_filter(event):

        if event.type == Event.TYPE_REPORT:
            text = 'Kontrolní hlášení'
        elif event.type == Event.TYPE_DOOR_OPEN:
            text = 'Otevření dveří'
        elif event.type == Event.TYPE_DOOR_CLOSED:
            text = 'Zavření dveří'
        elif event.type == Event.TYPE_MOVEMENT:
            text = 'Detekce pohybu!'
        elif event.type == Event.TYPE_SMOKE:
            text = 'Detekce kouře!'
        else:
            text = 'Nedefinováno'

        ret = '[{}] {}'.format(event.timestamp, text)

        return ret

    def reg_mode_filter(reg_mode):
        if reg_mode:
            return 'Zapnutý'

        return 'Vypnutý'