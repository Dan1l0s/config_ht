import sys
import zipfile


def cd(files_list, curr_dir, path):
    start_dir = curr_dir
    if (len(path) > 0):
        if path[-1] == '/':
            path = path[0:-1]
    else:
        return curr_dir
    path_str = path.split('/')
    for command in path_str:
        if command == '..':
            index = curr_dir[0:-1].rfind('/')
            if index == -1:
                curr_dir = ''
            else:
                curr_dir = curr_dir[0:index+1]
        elif command == '/root' or command == '~':
            curr_dir = ''
        elif curr_dir + command + '/' in files_list:
            curr_dir += command + '/'
        elif command + '/' in files_list:
            curr_dir = command + '/'
        else:
            print('cd error: "' + path + '" no such directory')
            return start_dir
    return curr_dir


def ls(files_list, curr_dir):
    for path in files_list:
        if path.find(curr_dir) != -1:
            subpath = path[len(curr_dir)::]
            cnt = subpath.count('/')
            if (cnt == 1 and subpath[-1] == '/') or (cnt == 0 and subpath != ''):
                if subpath[-1] == '/':
                    subpath = subpath[0:-1]
                print(subpath, end='\t')
    print()


def pwd(curr_dir):
    if curr_dir == '':
        print('/root')
    else:
        print('/root/' + curr_dir[0:-1])


def cat(files_list, curr_dir, path, zip_name):
    index = path.rfind('/')
    tmp_dir = curr_dir
    if index != -1:
        tmp_dir = cd(files_list, tmp_dir, path[0:index+1])
        path = path[index+1::]
    if (tmp_dir + path) in files_list:
        file = zipfile.ZipFile(zip_name).open(tmp_dir + path, 'r')
        for line in file.readlines():
            cur_line = str(line.strip())[2:-1]
            print(cur_line)
    else:
        print('cat error: "' + tmp_dir + path + '" no such file or directory')


args = sys.argv
if len(args) != 2:
    print('Error, no file system')
    exit()
command_line = ''
zip_name = args[1]
print(args)
files_list = zipfile.ZipFile(zip_name, 'r').namelist()
curr_dir = ''
# curr_dir = cd(files_list, curr_dir, "Archive")
while command_line != 'exit':
    print('[root@localhost ', end='')
    if curr_dir == '':
        print('~]', end='# ')
    else:
        print(curr_dir[('/' + curr_dir[0: -1]).rfind('/'): -1] + ']', end='# ')
    command_line = input()
    command = command_line.split()
    if command[0] == 'cd':
        if len(command) == 2:
            curr_dir = cd(files_list, curr_dir, command[1])
        else:
            print('cd has 1 argument')
    elif command[0] == 'ls':
        if len(command) == 1:
            ls(files_list, curr_dir)
        else:
            print('ls has no arguments')
    elif command[0] == 'pwd':
        if len(command) == 1:
            pwd(curr_dir)
        else:
            print('pwd has no arguments')
    elif command[0] == 'cat':
        if len(command) == 2:
            cat(files_list, curr_dir, command[1], zip_name)
        else:
            print('cat has 1 argument')
    elif command[0] == 'exit':
        break
    else:
        print('error, "' + command[0] + '" command not found')
