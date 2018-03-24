__apiversion__ = 1


class Trigger:
    def __init__(self):
        self.devices_seen = set()

    def __call__(self, dev_id=None, num_bytes=None, power=None, **kwargs):
        self.devices_seen |= {dev_id}
        print('devices_seen: {}'.format(self.devices_seen))

