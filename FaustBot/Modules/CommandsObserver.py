from FaustBot.Communication import Connection
from FaustBot.Model.Commands import CommandsProvider
from FaustBot.Modules import UserList
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class CommandsObserver(PrivMsgObserverPrototype):
    def __init__(self, user_list: UserList):
        super().__init__()
        self.userList = user_list

    @staticmethod
    def cmd():
        return ['.command']

    @staticmethod
    def help():
        return '.command <Command> <Reaktion> - Speichert einen benutzerdefinierten Command ein'

    def update_on_priv_msg(self, data, connection: Connection):

        if data['message'].startswith('.command help'):
            connection.send_back('Hilfe schreiben', data)
            return
        
        message = data['message']
        messageSplit = data['message'].split(" ", 3)
        requester = data['nick']
        try:
            command = messageSplit[1]
        except IndexError:
            print('IndexError')
            command = None
        command_prov = CommandsProvider()
        laenge = len(messageSplit)

        messageCase = data['messageCaseSensitive']
        messageSplitCase = messageCase.split(' ', 3)
        try:
            reaction = messageSplitCase[3]
        except IndexError:
            print('indexError')
            reaction = None

        print(message)
        print(command)
        print(reaction)
        print(laenge)

        if message.startswith('.command'):
            connection.send_back('erstes if geschafft', data)

            if laenge == 2 and '-' in message:
                command_prov.delete_command(command)
                connection.send_back(f'Der Command: {command} wurde gelöscht.', data)
                return

            elif laenge == 4 and not reaction is None and not command is None:
                connection.send_back("Drittes if", data)
                command_prov.save_or_replace(command, reaction)
                connection.send_back("Command gespeichert", data)
                connection.send_back(f'{command} {reaction}', data)












