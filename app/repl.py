def repl():
    welcome_name = 'vfs'
    while True:
        try:
            user_input = input(f'{welcome_name}> ').strip()
            if not user_input:
                continue

            parts = user_input.split(' ')
            command = parts[0]
            args = parts[1:]

            if command == 'exit':
                if args:
                    print('exit: too many arguments')
                else:
                    break
            elif command == 'ls':
                print(f'ls: arguments:', ", ".join(args))
            elif command == 'cd':
                if len(args) > 1:
                    print('cd: too many arguments')
                else:
                    print(f'cd: arguments {args}')
            
            else:
                print(f'{command}: command not found')
                
        except EOFError:
            print() 
            break
        except KeyboardInterrupt:
            print()  
            break