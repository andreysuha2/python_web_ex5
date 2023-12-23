from ex_5.commands import commands_list
from ex_5.core.commands import NotFoundCommandException, CommandList
import sys

class App:
    def __init__(self, commands_list: CommandList) -> None:
        self.commands = commands_list
    
    def parse_args(self, args):
        return  (args[0], args[1:])
    
    def start(self, args_str):
        command_name, args = self.parse_args(args_str)
        try:
            result = self.commands.execute_command(command_name, *args)
            print("result:", result)
        except NotFoundCommandException:
            print(f"Command: {command_name} not found")
            
def main():
    app = App(commands_list=commands_list)
    app.start(sys.argv[1:])
    
if __name__ == "__main__":
    main()