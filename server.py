import subprocess


class ServerInstance:
    def __init__(self, server_path, jarfile='server.jar'):
        self.server_path = server_path
        self.process = None
        self.jarfile = jarfile
        self.output = []

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


server_path = 'server/'

server_instance = ServerInstance(server_path)
server_instance.start_server()

while True:
    command = input('Enter command: ')
    if command == 'output':
        output = server_instance.read_output()
        print(output)
    elif command == 'tail':
        print('how many lines to read?')
        lines = int(input())
        output = server_instance.read_tail(lines)
        print(output)
    elif command == 'stop':
        server_instance.stop_server()
        break
    else:
        server_instance.execute_command(command)
