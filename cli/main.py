import sys
import traceback

from cli.parser import parse_args

# Project commands
from cli.commands.project.init import run as init_cmd
from cli.commands.project.info import run as info_cmd
from cli.commands.project.doctor import run as doctor_cmd

# Dependency commands
from cli.commands.dependency.add import run as add_cmd
from cli.commands.dependency.remove import run as remove_cmd
from cli.commands.dependency.show import run as show_cmd

# Resolution commands
from cli.commands.resolution.resolve import run as resolve_cmd
from cli.commands.resolution.explain import run as explain_cmd
from cli.commands.resolution.conflicts import run as conflicts_cmd

# Environment commands
from cli.commands.environment.install import run as install_cmd
from cli.commands.environment.sync import run as sync_cmd
from cli.commands.environment.clean import run as clean_cmd

# Debug commands
from cli.commands.debug.graph import run as graph_cmd
from cli.commands.debug.trace import run as trace_cmd
from cli.commands.debug.dump import run as dump_cmd


class CommandDispatcher:
    def __init__(self):
        self.commands = {
            # project
            "init": init_cmd,
            "info": info_cmd,
            "doctor": doctor_cmd,

            # dependency
            "add": add_cmd,
            "remove": remove_cmd,
            "show": show_cmd,

            # resolution
            "resolve": resolve_cmd,
            "explain": explain_cmd,
            "conflicts": conflicts_cmd,

            # environment
            "install": install_cmd,
            "sync": sync_cmd,
            "clean": clean_cmd,

            # debug
            "graph": graph_cmd,
            "trace": trace_cmd,
            "dump": dump_cmd,
        }

    def dispatch(self, args):
        command = args.command

        if command not in self.commands:
            print(f"[ERROR] Unknown command: {command}")
            return 1

        handler = self.commands[command]
        return handler(args)


def main():
    try:
        args = parse_args()

        if not args.command:
            print("No command provided. Use --help.")
            return 1

        dispatcher = CommandDispatcher()
        return dispatcher.dispatch(args)

    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
        return 1

    except Exception as e:
        print("[ERROR] Something went wrong:")
        print(f"  {str(e)}")

        
        print("\n--- TRACEBACK ---")
        traceback.print_exc()

        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)