import argparse
import repl

def start_app():
    parser = argparse.ArgumentParser(description='UNIX-like shell emulator')
    parser.add_argument('--vfs-path', default='.', help='Path to VFS physical location')
    parser.add_argument('--start-script', help='Path to startup script')
    
    args = parser.parse_args()
    
    print("Starting emulator with parameters:")
    print(f"  VFS path: {args.vfs_path}")
    print(f"  Start script: {args.start_script if args.start_script else 'Not specified'}")
    print("-" * 40)
    
    emulator = repl.shell_emulate(args.vfs_path, args.start_script)

    
    if args.start_script:
        emulator.run_script(args.start_script)
        print("-" * 40)
        print("Startup script executed.")
        print("Entering interactive mode...")
        print("-" * 40)

    emulator.repl()