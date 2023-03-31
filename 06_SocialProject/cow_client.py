import cmd
import threading
import time
import readline
import socket


class CowClient(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 1337))
        self.prompt = '> '
        self.response = ''
        self.inner = False
        self.wait = True

    def do_cows(self, args):
        '''
        List all available cownames'''
        if args:
            print('Bad request\n')
            return
        self.sock.send("cows\n".encode())

    def do_who(self, args):
        '''
        List all logged in users'''
        if args:
            print('Bad request\n')
            return
        self.sock.send("who\n".encode())

    def do_quit(self, args):
        '''
        Quit the chat'''
        if args:
            print('Bad request\n')
            return
        self.sock.send("quit\n".encode())
        return 1

    def do_login(self, args):
        '''
        Log in with the specified cownames
        
        Syntax:
            login cowname 

        Parameters:
            cowname: user name to login with'''
        self.sock.send(("login " + args + '\n').encode())

    def do_say(self, args):
        '''
        Send a message to the specified user
        
        Syntax:
            say username msg 

        Parameters:
            username: username of the adresser
            msg: a message to send'''
        self.sock.send(("say " + args + '\n').encode())

    def do_yield(self, args):
        '''
        Send a message to all users
        
        Syntax:
            yield msg 

        Parameters:
            msg: a message to send'''
        self.sock.send(("yield " + args + '\n').encode())
    
    def complete_login(self, text, line, begidx, endidx):
        self.inner = True
        self.sock.send("cows\n".encode())
        while self.wait:
            pass
        self.wait = True
        self.inner = False
        cows = (self.response).split('\n')[1:]
        return [cow for cow in cows if cow.startswith(text)]
    
    def complete_say(self, text, line, begidx, endidx):
        self.inner = True
        self.sock.send("who\n".encode())
        while self.wait:
            pass
        self.wait = True
        self.inner = False
        users = (self.response).split('\n')[1:]
        return [user for user in users if user.startswith(text)]

    def recv(self):
        while True:
            msg = self.sock.recv(1024).decode().strip()
            if msg == "":
                break
            if self.inner:
                self.response = msg
                self.wait = False
            else:
                print(f"\n{msg}\n{cmdline.prompt}{readline.get_line_buffer()}",
                      end="",
                      flush=True)
        

if __name__ == '__main__':
    cmdline = CowClient()
    timer = threading.Thread(target=cmdline.recv)
    timer.start()
    cmdline.cmdloop()