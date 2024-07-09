from src.MinecaftServerManager import MinecraftServerInstance

server_path = 'server/'

server_instance = MinecraftServerInstance(server_path)
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
    elif command == 'restart':
        server_instance.restart_server()
    elif command == 'recreate world':
        server_instance.recreate_world()
    else:
        server_instance.execute_command(command)
