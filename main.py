import cmd
import os
import subprocess
import shutil
import platform
import readline

if platform.system() != "Linux":
    print("Sorry, this program is only supported on Linux NOOB!!! You must have downloaded the wrong version. Please note that only Linux and Windows versions are available for this software.")
    exit(1)

print("\033]0;TRASH TERMINAL\007")


class Trash(cmd.Cmd):
    intro = "Trash Terminal. ver. 1.4.3 Type 'help' to see available commands."
    prompt = "Trash >>> "
    print(intro)

    def __init__(self):
        super().__init__()
        self.starting_directory = os.path.expanduser("~")
        os.chdir(self.starting_directory)
        self.default_prompt = "Trash >>> "
        self.update_prompt()



    def update_prompt(self):
        self.prompt = f"Trash [{os.getcwd()}] >>> "

    def cmdloop(self):
        while True:
            try:
                line = input(self.prompt)
                commands = [cmd.strip() for cmd in line.split("&&")]
                for cmd in commands:
                    if cmd == "quit":
                        return True
                    if cmd == "nigga":
                        print("kys you worthless peace of shit")
                    self.onecmd(cmd)
            except KeyboardInterrupt:
                print("^C")
            except Exception as e:
                print(e)

    def preloop(self):
        readline.set_pre_input_hook(self.pre_input_hook)

    def pre_input_hook(self):
        readline.insert_text(self.prompt + "".join(self.cmdqueue))
        readline.redisplay()
        self.update_prompt()

    def postcmd(self, stop, line):
        print("\033[0m", end="")
        return stop

    def emptyline(self):
        self.cmdqueue.append("")

    def precmd(self, line):
        """Called before executing each command."""
        if self.cmdqueue:
            self.cmdqueue.pop(0)
        parts = line.strip().split()
        if parts:
            cmd_name = parts[0]
            if cmd_name in self.aliases:
                line = self.aliases[cmd_name] + " " + " ".join(parts[1:])
        return line


    def do_cd(self, arg):
        try:
            os.chdir(arg)
            self.update_prompt()
        except FileNotFoundError:
            print("Directory not found:", arg)
        except Exception as e:
            print("An error occurred:", e)

    def do_ls(self, arg):
        """Lists files and directories in the current directory."""
        try:
            files = os.listdir()
            for file in files:
                if os.path.isdir(file):
                    print(f"\033[34m{file}\033[0m")  # Blue for directories
                elif os.access(file, os.X_OK):
                    print(f"\033[32m{file}\033[0m")  # Green for executables
                else:
                    print(file)  # Default color for normal files
        except Exception as e:
            print(f"An error occurred: {e}")


    def do_print(self, arg):
        print(arg)

    def do_redir(self, arg):
        """Resets the current working directory to the starting directory."""
        try:
            os.chdir(self.starting_directory)
            self.update_prompt()
            print("Directory reset to:", self.starting_directory)
        except Exception as e:
            print("An error occurred:", e)


    def do_crdir(self, arg):
        try:
            os.mkdir(arg)
            print("Directory created:", arg)
        except FileExistsError:
            print("Directory already exists:", arg)
        except Exception as e:
            print("An error occurred:", e)

    def do_touch(self, arg):
        try:
            with open(arg, 'a'):
                os.utime(arg, None)
            print("File created:", arg)
        except FileExistsError:
            print("File already exists:", arg)
        except Exception as e:
            print("An error occurred:", e)

    def do_del(self, arg):
        try:
            if os.path.isdir(arg):
                shutil.rmtree(arg)
                print("Directory removed:", arg)
            else:
                os.remove(arg)
                print("File removed:", arg)
        except FileNotFoundError:
            print("File or directory not found:", arg)
        except Exception as e:
            print("An error occurred:", e)

    def do_cp(self, arg):
        try:
            source, destination = arg.split()
            shutil.copy(source, destination)
            print("Copied:", source, "to", destination)
        except Exception as e:
            print("An error occurred:", e)

    def do_move(self, arg):
        try:
            source, destination = arg.split()
            shutil.move(source, destination)
            print("Moved:", source, "to", destination)
        except Exception as e:
            print("An error occurred:", e)

    def do_netinfo(self, arg):
        """Displays network interface configuration."""
        try:
            result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print("An error occurred:", e)

    def do_sysinfo(self, arg):
        """Displays system information."""
        try:
            print("Operating System:", platform.system())
            print("Operating System Version:", platform.version())
            print("Machine Type:", platform.machine())
            print("Processor:", platform.processor())
            print("Network Hostname:", platform.node())

            print("\nMemory Information:")
            subprocess.run(["free", "-h"])

            print("\nDisk Usage:")
            subprocess.run(["df", "-h"])

            print("\nRunning Processes:")
            subprocess.run(["ps", "aux"])
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def do_clear(self, arg):
        """Clears the terminal screen."""
        try:
            subprocess.run(["clear"])
        except Exception as e:
            print("An error occurred:", e)


    def do_rn(self, arg):
        try:
            old_name, new_name = arg.split()
            os.rename(old_name, new_name)
            print(f"Successfully renamed '{old_name}' to '{new_name}'.")
        except ValueError:
            print("Usage: rename <old_name> <new_name>")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def do_grep(self, arg):
        try:
            file_name, pattern = arg.split()
            with open(file_name, 'r') as file:
                for line in file:
                    if pattern in line:
                        print(line, end='')
        except ValueError:
            print("Usage: grep <file_name> <pattern>")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def do_cat(self, arg):
        try:
            with open(arg, 'r') as file:
                print(file.read())
        except FileNotFoundError as e:
            print(f"Error: {e}")

    def do_dano(self, arg):
        """Edit a file directly in the terminal with Dano editor.
           Usage: dano <file_name>"""
        if not arg:
            print("Usage: dano <file_name>")
            return

        file_path = arg.strip()

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    lines = file.readlines()
            else:
                print(f"Creating new file: {file_path}")
                lines = []

            print("Entering editing mode. Type ':w' to save and exit, ':q' to quit without saving.")
            print("Current file content:")
            for index, line in enumerate(lines):
                print(f"{index + 1}: {line.strip()}")

            new_content = lines[:]
            while True:
                user_input = input("> ")
                if user_input == ":w":
                    with open(file_path, 'w') as file:
                        file.writelines(new_content)
                    print(f"File '{file_path}' saved.")
                    break
                elif user_input == ":q":
                    print("Exiting without saving.")
                    break
                elif user_input.startswith(":"):
                    print(f"Unknown command: {user_input}")
                else:
                    new_content.append(user_input + "\n")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred while editing the file: {e}")

    def default(self, line):
        parts = line.strip().split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
            try:
                subprocess.run([cmd] + args)
            except Exception as e:
                print(f"Error executing file: {e}")
            return

        if os.path.isfile(cmd):
            if cmd.endswith(".py"):
                try:
                    subprocess.run(["python3", cmd] + args)
                except Exception as e:
                    print(f"Error running Python script: {e}")
                return
            elif cmd.endswith(".sh"):
                try:
                    subprocess.run(["bash", cmd] + args)
                except Exception as e:
                    print(f"Error running shell script: {e}")
                return
                
        print("\033[33m", end="")
        super().default(line)
        print("\033[0m", end="")

    def do_quit(self, arg):
        print("Exiting Trash.")
        return True

if __name__ == "__main__":
    Trash().cmdloop()
