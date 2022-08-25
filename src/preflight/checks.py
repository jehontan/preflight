from abc import ABC, abstractmethod
from dataclasses import dataclass
import os

class Context(dict):
    '''Context for checks.'''
    pass

@dataclass
class Result:
    passed:bool
    msg:str

class Check(ABC):
    '''Base class for preflight checks.'''
    def __init__(self, name:str, desc:str='', pass_msg:str='', fail_msg:str=''):
        '''
        Parameters
        ----------
        name : str
            Name of the test.
        desc : str
            Description of the test.
        pass_msg : str
            Message to output if test passes.
        fail_msg : str
            Message to output if test fails.
        '''
        self.name = name
        self.desc = desc
        self.pass_msg = pass_msg
        self.fail_msg = fail_msg

    @abstractmethod
    def run(self, ctx:Context) -> bool:
        pass

class CheckSequence:
    def __init__(self, name:str=''):
        self.name = name
        self.ctx = Context()
        self.checks : list[Check] = []
        self.results : dict[str, Result] = {}

    def add(self, check:Check):
        '''Add a check to the sequence.'''
        self.checks.append(check)

    def run(self) -> bool:
        '''Run the check sequence.
        
        Returns
        -------
        all_passed : bool
            True if all checks passed, False otherwise.
        '''
        self.results = {}
        all_passed = True
        for check in self.checks:
            res = check.run(self.ctx)
            self.results[check.name] = res
            all_passed &= res.passed
            
        return all_passed

##### Concrete checks #####

class PingConnectivityCheck(Check):
    '''Basic connectivity check using ping'''
    def __init__(self, name:str, host:str, timeout:int=1, desc:str='', pass_msg:str='Connected.', fail_msg:str='Not connected.'):
        '''
        Parameters
        ----------
        name : str
            Name of the test.
        host : str
            Host to ping.
        timeout : int
            Timeout in seconds.
        desc : str
            Description of the test.
        pass_msg : str
            Message to output if test passes.
        fail_msg : str
            Message to output if test fails.
        '''
        super().__init__(name, desc, pass_msg, fail_msg)
        self.host = host
        self.timeout = timeout

    def run(self, ctx:Context=None) -> bool:
        res = os.system('ping -c 1 -w {} {} > /dev/null'.format(self.timeout, self.host))
        passed = res == 0
        ctx['{}_connected'.format(self.host)] = passed
        return Result(passed, self.pass_msg if passed else self.fail_msg)