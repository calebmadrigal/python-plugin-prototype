# python-plugin-prototype

python plugin prototype

## Usage

Example of running with a `trigger` function:

    $ python3 main.py --triggerpy trigger_plugin_func.py
    Threshold reached for 11:22:33:44:55:00 - 10 bytes
    Threshold reached for 11:22:33:44:55:11 - 20 bytes
    Threshold reached for 11:22:33:44:55:22 - 30 bytes
    Threshold reached for 11:22:33:44:55:33 - 40 bytes
    Threshold reached for 11:22:33:44:55:44 - 50 bytes

Example of running with a `Trigger` class:

    $ python3 main.py --triggerpy trigger_plugin_class.py
    devices_seen: {'11:22:33:44:55:00'}
    devices_seen: {'11:22:33:44:55:00', '11:22:33:44:55:11'}
    devices_seen: {'11:22:33:44:55:00', '11:22:33:44:55:11', '11:22:33:44:55:22'}
    devices_seen: {'11:22:33:44:55:33', '11:22:33:44:55:00', '11:22:33:44:55:11', '11:22:33:44:55:22'}
    devices_seen: {'11:22:33:44:55:00', '11:22:33:44:55:22', '11:22:33:44:55:33', '11:22:33:44:55:44', '11:22:33:44:55:11'}

Note: the advantage of using a class is that it can keep track of memory between trigger calls, whereas the function
has no memory between calls.

