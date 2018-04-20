from .models.event import Event
from .models.garage import Garage


class Filters():
    def date_filter(date):
        if date is None:
            return 'Žádné'

        return date

    def garage_doors_filter(doors):
        if doors == Garage.DOORS_OPEN:
            return 'Otevřeno'

        if doors == Garage.DOORS_CLOSE:
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
            return '[{}] Kontrolní hlášení'.format(event.timestamp)
        
        if event.type == Event.TYPE_DOOR_OPEN:
            return '[{}] Otevření dveří'.format(event.timestamp)

        if event.type == Event.TYPE_DOOR_CLOSE:
            return '[{}] Zavření dveří'.format(event.timestamp)
        
        if event.type == Event.TYPE_MOVEMENT:
            return '[{}] Detekce pohybu!'.format(event.timestamp)

        if event.type == Event.TYPE_SMOKE:
            return '[{}] Detekce kouře!'.format(event.timestamp)

        if event.type == Event.TYPE_DEVICE_ERROR:
            return '[{}] Chyba podřízeného systému'.format(event.timestamp)

        return '[{}] Nedefinováno'.format(event.timestamp, text)

    def reg_mode_filter(reg_mode):
        if reg_mode:
            return 'Zapnutý'

        return 'Vypnutý'
