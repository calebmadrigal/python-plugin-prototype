__apiversion__ = '1.0.0'


def trigger(dev_id=None, num_bytes=None, power=None, **kwargs):
    if num_bytes:
        print('Threshold reached for {} - {} bytes'.format(dev_id, num_bytes))
    else:
        print('Saw {} at power level {}'.format(dev_id, power))

