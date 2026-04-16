from sys import stdout, stderr

class Logger:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def input(self, message=''):
        return input(f'{message}')
    
    def print(self, message='', file=stdout):
        print(message, file=file)
    
    def log(self, message='', file=stdout):
        if self.verbose:
            print(f'[+] {message}', file=file)
    
    def warn(self, message='', file=stderr):
        print(f'[!] {message}', file=file)
    
    def err(self, message='', file=stderr):
        print(f'[-] {message}', file=file)
    
    def debug(self, message='', file=stdout):
        print(f'[DEBUG] {message}', file=file)
    
    def set_verbose(self, verbose):
        self.verbose = verbose

console = Logger()