from abc import ABCMeta, abstractmethod
from typing import Dict

class NotFoundCommandException(Exception):
    pass

class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass

class CommandList:
    def __init__(self, commands):
        self.__commands = commands
    
    def has_command(self, name: str) -> bool:
        return name in self.__commands
    
    def execute_command(self, name, *args, **kwargs):
        if not self.has_command(name):
            raise NotFoundCommandException
        command = self.__commands.get(name)
        return command.execute(*args, **kwargs)

