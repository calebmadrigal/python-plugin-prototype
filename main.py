import time
import argparse

CURRENT_API_VERSION = '1.0.0'


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--triggerpy', type=str, dest='trigger_py',
                        help='Path to python script that adheres to trigger api')
    return parser


def default_trigger(dev_id=None, dev_type=None, num_bytes=None, power=None, window=None, **kwargs):
    if num_bytes:
        print('{time} detected {dev_type} {dev_id} - {num_bytes} bytes in {window} second window'
              .format(time=int(time.time()), dev_type=dev_type, dev_id=dev_id, num_bytes=num_bytes, window=window))
    else:
        print('{time} detected {dev_type} {dev_id} - power = {power}'
              .format(time=int(time.time()), dev_type=dev_type, dev_id=dev_id, power=power))


def parse_trigger(trigger_path):
    with open(trigger_path, 'r') as f:
        trigger_code = f.read()
    trigger_vars = {}
    exec(trigger_code, trigger_vars)

    apiversion = trigger_vars.get('__apiversion__', CURRENT_API_VERSION)

    try:
        trigger = trigger_vars['trigger']
    except KeyError:
        raise Exception('Trigger plugin must specify a python function named "trigger"')

    return {'trigger': trigger, 'apiversion': apiversion}


def run_trigger(trigger, trigger_data):
    if trigger['apiversion'] == '1.0.0':
        trigger['trigger'](**trigger_data)
    else:
        raise Exception('Unsupported trigger version')


def run(trigger):
    for i in range(9):
        trigger_data = {'dev_id': '11:22:33:44:55:'+str(i)*2, 'dev_type': 'mac', 'num_bytes': (i+1)*10, 'window': 30}
        run_trigger(trigger, trigger_data)
        time.sleep(1)
        

if __name__ == '__main__':
    args = get_arg_parser().parse_args()
    trigger_data = {'trigger': default_trigger, 'apiversion': CURRENT_API_VERSION}

    if args.trigger_py:
        trigger_data = parse_trigger(args.trigger_py)

    run(trigger_data)

