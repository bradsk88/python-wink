from ..devices.base import WinkDevice

SUPPORTED_BINARY_STATE_FIELDS = ['powered', 'opened']


class WinkBinarySwitch(WinkDevice):
    """
    Represents a Wink binary switch.
    """

    def state(self):
        _field = self.binary_state_name()
        return self._last_reading.get(_field, False)

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        _field = self.binary_state_name()
        values = {"desired_state": {_field: state}}
        response = self.api_interface.local_set_state(self, values, type_override="binary_switche")
        self._update_state_from_response(response)

    def binary_state_name(self):
        """
        Search all of the capabilities of the device and return the supported binary state field.
        Default to returning powered.
        """
        return_field = "powered"
        _capabilities = self.json_state.get('capabilities')
        if _capabilities is not None:
            _fields = _capabilities.get('fields')
            if _fields is not None:
                for field in _fields:
                    if field.get('field') in SUPPORTED_BINARY_STATE_FIELDS:
                        return_field = field.get('field')
        return return_field

    def last_event(self):
        return self._last_reading.get("last_event")

    def update_state(self):
        """
        Update state with latest info from Wink API.
        """
        response = self.api_interface.local_get_state(self, type_override="binary_switche")
        return self._update_state_from_response(response)
