import os
import json
import hashlib
import base64

class shell_emulate():
    def __init__(self, vfs_path, start_script=None):
        self.vfs_path = vfs_path
        self.start_script = start_script
        self.vfs_name = os.path.basename(os.path.normpath(vfs_path))
        self.vfs_data = None
        self.vfs_hash = None
        self.load_vfs()

    def repl(self):
        while True:
            try:
                user_input = input(f'{self.vfs_name}> ').strip()
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
        elif command == "vfs-info":
            self.vfs_info()
        else:
            print(f'{command}: command not found')

        return True
    
    def load_vfs(self):
        """Загрузка VFS из JSON файла"""
        try:
            if not os.path.exists(self.vfs_path):
                print(f"Error: VFS file '{self.vfs_path}' not found.")
                return
            
            with open(self.vfs_path, 'r', encoding='utf-8') as f:
                vfs_content = f.read()
                self.vfs_data = json.loads(vfs_content)
                
            # Вычисление SHA-256 хеша
            with open(self.vfs_path, 'rb') as f:
                file_content = f.read()
                self.vfs_hash = hashlib.sha256(file_content).hexdigest()
                
            print(f"VFS loaded successfully from '{self.vfs_path}'")
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid VFS JSON format - {e}")
            self.vfs_data = None
            self.vfs_hash = None
        except Exception as e:
            print(f"Error loading VFS: {e}")
            self.vfs_data = None
            self.vfs_hash = None

    def vfs_info(self):
        """Вывод информации о загруженной VFS"""
        if self.vfs_data is None:
            print("vfs-info: No VFS loaded")
            return
        
        vfs_name = os.path.basename(self.vfs_path)
        print(f"VFS name: {vfs_name}")
        print(f"SHA-256: {self.vfs_hash}")
        print(f"VFS structure loaded: {self.vfs_data is not None}")

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