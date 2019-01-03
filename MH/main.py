import argparse, sys

from datParser import datParser
from validateConfig import ValidateConfig
from validateInputBus import ValidateInputBus
from problem import Problem
from solver import Solver
from solution import Solution

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

        print ('Reading Input Data file %s...' % config.inputDataFile)
        inputData = datParser.parse(config.inputDataFile)
        ValidateInputBus.validate(inputData)

        print ('Creating Problem...')
        problem = Problem(inputData)

        if(problem.checkInstance()):
            print ('Solving Problem...')
            solver = Solver()
            solution = solver.solve(config, problem)
                
            solution.saveToFile(config.solutionFile)
        else:
            print ('Instance is unfeasible.')
            solution = Solution.createEmptySolution(config, problem)
            solution.makeInfeasible()
            solution.saveToFile(config.solutionFile)
            
        return(0)
    except Exception as e:
        print ()
        print ('Exception:', e)
        print ()
        return(1)   


if __name__ == '__main__':
    sys.exit(run())