from ..devices.base import WinkDevice


class WinkRemote(WinkDevice):
    """
    Represents a Wink/Lutron connected bulb remote.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkRemote, self).__init__(device_state_as_json, api_interface)
        self._unit = None
        self._cap = 'opened'
        self._available = True

    def unit(self):
        # Remote has no unit
        return self._unit

    def capability(self):
        # Remote has no capability.
        return self._cap

    def state(self):
        return bool(self.button_on_pressed() or self.button_off_pressed() or
                    self.button_up_pressed() or self.button_down_pressed())

    def button_on_pressed(self):
        return self._last_reading.get("button_on_pressed") or False

    def button_off_pressed(self):
        return self._last_reading.get("button_off_pressed") or False

    def button_down_pressed(self):
        return self._last_reading.get("button_down_pressed") or False

    def button_up_pressed(self):
        return self._last_reading.get("button_up_pressed") or False
