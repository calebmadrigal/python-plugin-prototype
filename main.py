"""Handles parsing trigger plugin files and running them.

The plugin file must be a python file which contains either a function called 'trigger'
or a class called 'Trigger'. It's also recommended to specify a '__apiversion__' (which is just an int)
for backward compatibility if api changes are made in the future.

If specifying a 'trigger' function, the trigger can take the args specified by default_trigger, and should
always take a catch-all **kwargs for future compatibility.

Likewise, if specifying a 'Trigger' class, that class must define a '__call__' method, which takes
a subset of the kwargs specified by 'default_trigger', and should always contain a catch-all **kwargs
for future compatibility.

Note that this plugin system is not sandboxed, so if the code in trigger_path brakes something,
the host program will break (unless it is explicitly handling any errors).
"""
import time
import argparse

CURRENT_API_VERSION = 1


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
    """Parse plugin file and return the trigger config."""
    with open(trigger_path, 'r') as f:
        trigger_code = f.read()
    trigger_vars = {}
    exec(trigger_code, trigger_vars)

    api_version = trigger_vars.get('__apiversion__', CURRENT_API_VERSION)
    trigger = trigger_vars.get('trigger', None)
    trigger_class = trigger_vars.get('Trigger', None)

    if trigger_class:
        # Instantiate class. Note that only a trigger function or class can be defined (and class takes priority)
        # Assume the class is called 'Trigger'
        trigger = trigger_class()

    if not trigger:
        raise Exception('Plugin file must specify a "trigger" function or a "Trigger" class')

    return {'trigger': trigger, 'api_version': api_version}


def run_trigger_plugin(trigger, trigger_data):
    if trigger['api_version'] == CURRENT_API_VERSION:
        trigger['trigger'](**trigger_data)
    else:
        raise Exception('Unsupported trigger version')


def run_trigger(trigger):
    for i in range(5):
        trigger_data = {'dev_id': '11:22:33:44:55:'+str(i)*2, 'dev_type': 'mac', 'num_bytes': (i+1)*10, 'window': 30}
        run_trigger_plugin(trigger, trigger_data)
        time.sleep(1)
        

if __name__ == '__main__':
    args = get_arg_parser().parse_args()
    trigger_config = {'trigger': default_trigger, 'api_version': CURRENT_API_VERSION}

    if args.trigger_py:
        trigger_config = parse_trigger(args.trigger_py)

    run_trigger(trigger_config)

