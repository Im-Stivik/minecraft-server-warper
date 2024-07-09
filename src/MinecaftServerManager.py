import subprocess
import os
import shutil
import datetime


class MinecraftServerInstance:
    def __init__(self, server_path, jarfile='server.jar'):
        self.server_path = server_path
        self.process = None
        self.jarfile = jarfile
        self.output = []
        self.world_name = 'world'

    def start_server(self):
        # Start the Minecraft server process
        self.process = subprocess.Popen(
            ['java', '-Xmx1024M', '-Xms1024M', '-jar', self.jarfile, 'nogui'],
            cwd=self.server_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Start a thread to read server output
        self._start_output_reader()

    def _create_custom_log_massage(self, message):
        # get current time
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return f'[{current_time}] [Warper]: {message}'

    def append_to_output(self, message):
        self.output.append(self._create_custom_log_massage(message))

    def _start_output_reader(self):
        # Read server output in a separate thread
        def output_reader():
            for line in iter(self.process.stdout.readline, b''):
                self.output.append(line.decode('utf-8').strip())
            self.process.stdout.close()

        import threading
        threading.Thread(target=output_reader, daemon=True).start()

    def execute_command(self, command):
        # Send a command to the Minecraft server process
        if self.process:
            self.process.stdin.write(command.encode('utf-8') + b'\n')
            self.process.stdin.flush()

    def read_output(self):
        # Return all collected output and clear the buffer
        output = '\n'.join(self.output)
        return output

    def read_tail(self, lines=1):
        # Return the last n lines
        return '\n'.join(self.output[-lines:])

    def stop_server(self):
        # Stop the Minecraft server process
        if self.process:
            self.process.stdin.write('stop\n'.encode('utf-8'))
            self.process.stdin.flush()
            self.process.wait()
            self.process = None

    def restart_server(self):
        self.stop_server()
        self.start_server()

    def recreate_world(self):
        # Delete the world folder and restart the server
        self.append_to_output('Recreating world...')
        self.append_to_output('Stopping server...')
        self.stop_server()
        self.append_to_output('Deleting world folder...')
        self._delete_world_folder()
        self.append_to_output('World folder deleted. starting server...')
        self.start_server()

    def _delete_world_folder(self):
        world_path = os.path.join(self.server_path, self.world_name)
        shutil.rmtree(world_path, ignore_errors=True)
