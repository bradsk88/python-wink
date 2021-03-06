from ..devices.base import WinkDevice


class WinkPowerStrip(WinkDevice):
    """
    Represents a Wink Powerstrip.
    The state of the power strip is Ture if one outlet is on, and False if both are off.
    Setting the state will set the state of both outlets.
    """

    def state(self):
        outlets = self.json_state.get('outlets')
        state = False
        for outlet in outlets:
            if outlet.get('last_reading').get('powered'):
                state = True
        return state

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        values = {"outlets": [{"desired_state": {"powered": state}}, {"desired_state": {"powered": state}}]}

        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)


class WinkPowerStripOutlet(WinkDevice):
    """
    Represents a Wink Powerstrip outlet.
    """

    def state(self):
        return self._last_reading.get('powered', False)

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self, id_override=self.parent_id(),
                                                       type_override=self.parent_object_type())
        self._update_state_from_response(response)

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        power_strip = response_json.get('data')

        power_strip_reading = power_strip.get('last_reading')
        outlets = power_strip.get('outlets')
        for outlet in outlets:
            if outlet.get('outlet_id') == str(self.object_id()):
                outlet['last_reading']['connection'] = power_strip_reading.get('connection')
                self.json_state = outlet

    def pubnub_update(self, json_response):
        self._update_state_from_response(json_response)

    def index(self):
        return self.json_state.get('outlet_index', None)

    def parent_id(self):
        return self.json_state.get('parent_object_id')

    def parent_object_type(self):
        return self.json_state.get('parent_object_type')

    def set_name(self, name):
        if self.index() == 0:
            values = {"outlets": [{"name": name}, {}]}
        else:
            values = {"outlets": [{}, {"name": name}]}
        response = self.api_interface.set_device_state(self, values, id_override=self.parent_id(),
                                                       type_override="powerstrip")
        self._update_state_from_response(response)

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        if self.index() == 0:
            values = {"outlets": [{"desired_state": {"powered": state}}, {}]}
        else:
            values = {"outlets": [{}, {"desired_state": {"powered": state}}]}

        response = self.api_interface.set_device_state(self, values, id_override=self.parent_id(),
                                                       type_override="powerstrip")
        self._update_state_from_response(response)
