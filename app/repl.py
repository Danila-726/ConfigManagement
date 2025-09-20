import os

class shell_emulate():
    def __init__(self, vfs_path, start_script=None):
        self.vfs_path = vfs_path
        self.start_script = start_script
        self.vfs_name = os.path.basename(os.path.normpath(vfs_path))

    def repl(self):
        while True:
            try:
                user_input = input(f'{self.vfs_path}> ').strip()
                if not user_input:
                    continue
            except EOFError:
                print() 
                break
            except KeyboardInterrupt:
                print()  
                break

            should_continue = self.run_command(user_input)
            if not should_continue:
                break

    def run_command(self, user_input):
        if not user_input:
            return True

        parts = user_input.split(' ')
        command = parts[0]
        args = parts[1:]

        if command == 'exit':
            if args:
                print('exit: too many arguments')
                return True
            return False
        elif command == 'ls':
            print(f'ls: arguments:', ", ".join(args))
        elif command == 'cd':
            if len(args) > 1:
                print('cd: too many arguments')
            else:
                print(f'cd: arguments {args}')
        elif command == "conf-dump":
            print("Configuration:")
            print(f"  VFS path: {self.vfs_path}")
            print(f"  Start script: {self.start_script if self.start_script else 'Not specified'}")
        else:
            print(f'{command}: command not found')

        return True
    
    def run_script(self, script_path):
        try:
            with open(f"{script_path}", 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    continue
                
                print(f"{self.vfs_name}> {stripped_line}")

                should_continue = self.run_command(stripped_line)
                if not should_continue:
                    break
                    
        except FileNotFoundError:
            print(f"Error: Script '{script_path}' not found.")
            return False
        except Exception as e:
            print(f"Error executing script: {e}")
            return False
            
        return True