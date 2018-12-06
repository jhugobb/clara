import argparse, sys
from datParser import datParser
from validateConfig import validateConfig
from instanceGenerator import instanceGenerator

def run():
    argp = argparse.ArgumentParser(description='Project Instance Generator')
    argp.add_argument('configFile', help='configuration file path')
    args = argp.parse_args()
    
    print ('AMMM Instance Generator')
    print ('-----------------------')
    
    print ('Reading Config file %s...' % args.configFile)
    config = datParser.parse(args.configFile)
    for parameter in config.__dict__:
        print(parameter)

    validateConfig.validate(config)
    '''
    print ('Creating Instances...')
    instGen = instanceGenerator(config)
    instGen.generate()
    '''
    print ('Done')

    return(0)

if __name__ == '__main__':
    sys.exit(run())
