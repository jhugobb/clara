import argparse, sys

from datParser import datParser
from validateConfig import ValidateConfig

def run():
    try:
        argp = argparse.ArgumentParser(description='AMMM Lab Heuristics')
        argp.add_argument('configFile', help='configuration file path')
        args = argp.parse_args()

        print ('AMMM Project')
        print ('By Ivan Salfati and Hugo Ballesteros')
        print ('--------------------------------------')

        print ('Reading Config file %s...' % args.configFile)
        config = datParser.parse(args.configFile)
        ValidateConfig.validate(config)

    except Exception as e:
        print ()
        print ('Exception:', e)
        print ()
        return(1)    


if __name__ == '__main__':
    sys.exit(run())