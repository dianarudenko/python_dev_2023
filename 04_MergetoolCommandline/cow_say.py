import cmd
import cowsay
import shlex
import re

class CommandLine(cmd.Cmd):
    intro = '''Welcome to the cowsay-cmd! Please, enter your command.
Type `quit` to quit the program.'''
    prompt = '>>> '


    def bad_params(self, func_name):
        print(f'Bad parameters! Type `help {func_name}` to get more info.')


    def do_list_cows(self, args: str):
        '''
        List all available cows.

        Syntax:
            list_cows [-f cow_path] 

        Parameters:
            -f cow_path: Look for cow file names in the <cow_path> directory. \
If not specified default directory is used.'''
        if args:
            parsed_args = shlex.split(args)
            print(parsed_args)
            if len(parsed_args) == 2 and parsed_args[0] == '-f':
                print(*cowsay.list_cows(cowpath=parsed_args[1]))
            else:
                self.bad_params('list_cows')
        else:
            print(*cowsay.list_cows(), sep=', ')


    def do_make_bubble(self, args: str):
        '''
        Make a bubble around your text.
        
        Syntax:
            make_bubble message [-b brackets] [-w width] [-n]
        
        Parameters:
            message: A message to put in the bubble. If it consists of several \
words it should be wrapped in quotes.
            -b brackets: Specifies which type of brackets to use. There are \
2 possible options: `say` and `think`. Default value is `say`.
            -w width: Specifies width (int) of the bubble. Default value is 40.
            -n: If specified then the message won't be wrapped.'''
        if args:
            parsed_args = shlex.split(args)
            params = {}
            message = None
            i = 0
            args_len = len(parsed_args)
            while i < args_len:
                if parsed_args[i] == '-b':
                    i += 1
                    if i == args_len:
                        self.bad_params('make_bubble')
                        return
                    if parsed_args[i] not in ('say', 'think'):
                        self.bad_params('make_bubble')
                        return
                    if parsed_args[i] == 'say':
                        params['brackets'] = cowsay.THOUGHT_OPTIONS['cowsay']
                    else:
                        params['brackets'] = cowsay.THOUGHT_OPTIONS['cowthink']
                elif parsed_args[i] == '-w':
                    i += 1
                    if i == args_len:
                        self.bad_params('make_bubble')
                        return
                    try:
                        params['width'] = int(parsed_args[i])
                    except:
                        self.bad_params('make_bubble')
                        return
                elif parsed_args[i] == '-n':
                    params['wrap_text'] = False
                elif message is None:
                    message = parsed_args[i]
                else:
                    self.bad_params('make_bubble')
                    return
                i += 1
            print(cowsay.make_bubble(message, **params))
        else:
            self.bad_params('make_bubble')


    def cowdo(self, args, func, func_name):
        if args:
            parsed_args = shlex.split(args)
            params = {}
            message = None
            i = 0
            args_len = len(parsed_args)
            while i < args_len:
                if parsed_args[i] == '-c':
                    i += 1
                    if i == args_len:
                        self.bad_params(func_name)
                        return
                    params['cow'] = parsed_args[i]
                elif parsed_args[i] == '-e':
                    i += 1
                    if i == args_len:
                        self.bad_params(func_name)
                        return
                    params['eyes'] = parsed_args[i]
                elif parsed_args[i] == '-t':
                    i += 1
                    if i == args_len:
                        self.bad_params(func_name)
                        return
                    params['tongue'] = parsed_args[i]
                elif message == None:
                    message = parsed_args[i]
                else:
                    self.bad_params(func_name)
                    return
                i += 1
            if message is None:
                self.bad_params(func_name)
                return
            print(func(message, **params))
        else:
            self.bad_params(func_name)

        
    def do_cowsay(self, args: str):
        '''
        Make a cow say your message.

        Syntax:
            cowsay message [-c cow] [-e eyes] [-t tongue]

        Parameters:
            message: A message for cow to say.  If it consists of several \
words it should be wrapped in quotes.
            -c cow: A cowfile with a cow picture to use. If not specified \
default cow is used.
            -e eyes: Specifies the eyes pattern to use. Dafault value is `oo`.
            -t tongue: Spesifies the tongue pattern to use. Default value is `  `.'''
        self.cowdo(args, cowsay.cowsay, 'cowsay')


    def do_cowthink(self, args: str):
        '''
        Make a cow think of your message.

        Syntax:
            cowthink message [-c cow] [-e eyes] [-t tongue]

        Parameters:
            message: A message for cow to think of.  If it consists of several \
words it should be wrapped in quotes.
            -c cow: A cowfile with a cow picture to use. If not specified \
default cow is used.
            -e eyes: Specifies the eyes pattern to use. Dafault value is `oo`.
            -t tongue: Spesifies the tongue pattern to use. Default value is `  `.'''
        self.cowdo(args, cowsay.cowthink, 'cowthink')


    def complete_list_cows(self, text, line, begidx, endidx):
        if re.fullmatch(r'list_cows\s+-', line[:endidx]):
            return ['f']
        return []


    def complete_make_bubble(self, text, line, begidx, endidx):
        if re.fullmatch(r'make_bubble\s+-', line[:endidx]):
            return ['b', 'w', 'n']
        elif re.fullmatch(r'.+?\s+-b\s+\S*', line[:begidx]):
            match = re.match(r'.+?\s+-b\s+', line[:begidx])
            real_text = line[match.end():endidx]
            return [mode for mode in ('say', 'think') if mode.startswith(real_text)]
        return []

    
    def cowdo_complete(self, text, line, begidx, endidx, func_name):
        if re.fullmatch(func_name + r'\s+-', line[:endidx]):
            return ['c', 'e', 't']
        elif re.fullmatch(r'.+?\s+-c\s+\S*', line[:begidx]):
            match = re.match(r'.+?\s+-c\s+', line[:begidx])
            real_text = line[match.end():endidx]
            if real_text:
                return [cow for cow in cowsay.list_cows() if cow.startswith(real_text)]
            else:
                # there are too many options so show just few of them
                return ['default', 'cat', 'owl', '...']
        elif re.fullmatch(r'.+?\s+-e\s+\S*', line[:begidx]):
            match = re.match(r'.+?\s+-e\s+', line[:begidx])
            real_text = line[match.end():endidx]
            options = ('oo', '==', 'XX', '$$', '@@', '**', '--', 'OO', '..')
            return [eyes for eyes in options if eyes.startswith(real_text)]
        elif re.fullmatch(r'.+?\s+-t\s+\S*', line[:begidx]):
            options = ('lJ', 'll', 'LJ', 'II', 'U ')
            return [tongue for tongue in options if tongue.startswith(text)]
        return []


    def complete_cowsay(self, text, line, begidx, endidx):
        return self.cowdo_complete(text, line, begidx, endidx, 'cowsay')
    

    def complete_cowthink(self, text, line, begidx, endidx):
        return self.cowdo_complete(text, line, begidx, endidx, 'cowthink')
        

    def do_quit(self, args):
        '''Quit the program'''
        return 1

if __name__ == '__main__':
    cmdline = CommandLine()
    cmdline.cmdloop()