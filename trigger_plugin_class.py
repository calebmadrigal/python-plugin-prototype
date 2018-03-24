__apiversion__ = 1


class Trigger:
    def __init__(self):
        self.devices_seen = set()

    def __call__(self, dev_id=None, **kwargs):
        """Note that we can specify any subset of arguments we care about... in this case, just dev_id."""
        self.devices_seen |= {dev_id}
        print('devices_seen: {}'.format(self.devices_seen))

