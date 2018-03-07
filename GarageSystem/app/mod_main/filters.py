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
        ret = '[{}]'.format(event.timestamp)

        if event.type == Event.TYPE_REPORT:
            ret = ret + ' Kontrolní událost'
        elif event.type == Event.TYPE_DOOR_OPEN:
            ret = ret + ' Otevření dveří'
        elif event.type == Event.TYPE_DOOR_CLOSED:
            ret = ret + ' Zavření dveří'
        elif event.type == Event.TYPE_MOVEMENT:
            ret = ret + ' Detekce pohybu!'
        elif event.type == Event.TYPE_SMOKE:
            ret = ret + ' Detekce kouře!'
        else:
            ret = ret + 'Nedefinováno'

        return ret

    def reg_mode_filter(reg_mode):
        if reg_mode:
            return 'Zapnutý'

        return 'Vypnutý'