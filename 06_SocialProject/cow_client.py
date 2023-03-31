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

    def recv(self):
        while True:
            msg = self.sock.recv(1024).decode()
            try:
                while True:
                    buf = self.sock.recv(1024, socket.MSG_DONTWAIT).decode()
                    if buf:
                        msg += buf
                    else:
                        break
            except:
                pass
            if msg == "":
                break
            print(f"\n{msg}\n{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)
        

if __name__ == '__main__':
    cmdline = CowClient()
    timer = threading.Thread(target=cmdline.recv)
    timer.start()
    cmdline.cmdloop()