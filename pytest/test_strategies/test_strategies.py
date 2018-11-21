import os
import yaml
from autoremovetorrents.strategy import Strategy

def test_strategies(test_data):
    # Check each case
    base_dir = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'cases')
    print('Base directory: %s' % base_dir)

    for item in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, item)):
            # Enter a directory
            print("Entering directory '%s'..." % item)

            for conf_file in os.listdir(os.path.join(base_dir, item)):
                conf_path = os.path.join(base_dir, item, conf_file)
                if os.path.isfile(conf_path):
                    # Load file
                    print('Loading file: %s' % conf_file)
                    with open(conf_path, encoding='utf-8') as f:
                        conf = yaml.safe_load(f)

                    # Make strategy and run
                    stgy = Strategy(conf_file, conf['test'])
                    stgy.execute(test_data)

                    # Check result
                    if 'remain' in conf and set([x.name for x in stgy.remain_list]) \
                            != set(conf['remain'] if conf['remain'] is not None else []) \
                            or \
                            'remove' in conf and set([x.name for x in stgy.remove_list]) \
                            != set(conf['remove'] if conf['remove'] is not None else []):
                            raise AssertionError()

            # Leave the directory
            print("Leaving directory '%s'..." % item)