#!/usr/bin/env python3

import sys
import os
import argparse
import configparser
import subprocess
from pathlib import Path
import winreg
import glob
import time
import shutil

__version__ = 2.5

configPath = os.path.join(str(Path.home()), '.config','hoidev')
configFilePath = os.path.join(configPath, 'config')

# default values
defaultHoiGamePath = os.path.join(str(Path.home()), 'Documents', 'Paradox Interactive', 'Hearts of Iron IV')

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

def confirm(message='confirm?'):
    for x in range(0,3):
        confirm = input('{} (Yes/No): '.format(message))
        confirm = confirm.lower()
        if confirm in ['y', 'yes']:
            return True
        if confirm in ['n', 'no']:
            return False
        print('Please type yes or no')
    else:
        return False

def printExit(msg='', exitCode=1):
    print(msg)
    sys.exit(exitCode)


def get_key_HKCU(regKey='', key='path'):
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        keypath = winreg.OpenKey(registry, regKey)
    except:
        pass
    try:
        path = winreg.QueryValueEx(keypath, key)
        return path[0]
    except:
        pass

def get_key_HKLM(regKey='', key='main'):
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        keypath = winreg.OpenKey(registry, regKey)
    except:
        pass
    try:
        path = winreg.QueryValueEx(keypath, key)
        return path[0]
    except:
        pass

defaultLocalFolderPath     = os.path.join(str(Path.home()), 'Documents', 'Paradox Interactive', 'Hearts of Iron IV')

def handle_config():
    config = configparser.ConfigParser()
    if not os.path.exists(configFilePath):
        if not os.path.exists(configPath):
            os.makedirs(configPath)    
        config['Paths'] = {'local': defaultLocalFolderPath}
        config['Project'] = {'current': ""}
        with open(configFilePath, 'w') as configfile:
            config.write(configfile)
    return config

config = handle_config()
config.read(configFilePath)

#Arma3InstallFolder  = get_key_HKLM(os.path.join('Software','wow6432Node','bohemia interactive','arma 3'))
#Arma3WorkshopFolder = os.path.join(Arma3InstallFolder, '!Workshop')
#Arma3AppdataFolder  = os.path.join(os.getenv('LOCALAPPDATA'), 'Arma 3')
#MikeroToolFolder    = get_key_HKCU(os.path.join('Software','Mikero','pboProject'))
#Arma3ToolsFolder    = get_key_HKCU(os.path.join('Software','Bohemia Interactive','Arma 3 Tools'))
#Arma3SampleFolder   = get_key_HKCU(os.path.join('Software','Bohemia Interactive','Arma 3 Tools'), 'path_assetSamples')

HoiLogsFolder       = os.path.join(config.get('Paths','local', fallback=os.path.join(defaultLocalFolderPath, 'logs')), 'logs')
HoiModFolder        = os.path.join(config.get('Paths','local', fallback=os.path.join(defaultLocalFolderPath, 'mod')), 'mod')
currentProject      = config.get('Project','current', fallback="")

# Log Program
def prog_log (args, parser):
    logfiles = glob.glob(os.path.join(HoiLogsFolder, '*.log'))

    def printLogHighlight(text):
        if args.highlight:
            if 'error' in text.lower():
                return print('{}{}{}'.format('\033[91m', text, '\033[0m'), end='')
            if 'not found' in text.lower():
                return print('{}{}{}'.format('\033[31m', text, '\033[0m'), end='')
            elif 'warning' in text.lower():
                return print('{}{}{}'.format('\033[93m', text, '\033[0m'), end='')
            elif 'info' in text.lower():
                return print('{}{}{}'.format('\033[94m', text, '\033[0m'), end='')
            elif 'debug' in text.lower():
                return print('{}{}{}'.format('\033[37m', text, '\033[0m'), end='')
            else:
                return print('{}{}{}'.format('\033[90m', text, '\033[0m'), end='')
        else:
            return print(text, end='')

    def prog_log_watch(arg):
        arg = '' if arg == None else arg
        try:
            latestLogfile = os.path.join(HoiLogsFolder, args.log + ".log")
            logFile = open(latestLogfile, 'r')
        except ValueError:
            print("No logs avalible.")
            sys.exit(1)
        except FileNotFoundError:
            print('"{}" does not exist use --type to find avalible log types.'.format(args.log))
            sys.exit(1)


        os.system("title hoidev log")

        try:
            hoiRunning = process_exists("hoi4.exe")
            if hoiRunning:
                print('Starting monitoring of latest log file', os.path.basename(latestLogfile))
            else:
                print('Showing latest log file', os.path.basename(latestLogfile))
        except:
            hoiRunning = True
            print('WARN: Not possible to determin if HoI4 is running...')
            print('Starting monitoring of latest log file', os.path.basename(latestLogfile))

        if arg:
            os.system("title hoidev log \"{}\"".format(arg))
            print('Filter: {}'.format(arg)) 
        try:
            while True:
                try:
                    where = logFile.tell()
                    line = logFile.readline()
                except UnicodeDecodeError:
                    print("HOIDEV >>> UnicodeDecodeError: 'charmap' codec can't decode")
                if not line:
                    time.sleep(0.25)
                    logFile.seek(where)
                    if not hoiRunning:
                        sys.exit(0)
                else:
                    if arg:
                        if arg in line:
                            printLogHighlight(line)
                    else:
                        printLogHighlight(line)
        except KeyboardInterrupt:
            sys.exit(0)

    def prog_log_list():
        if len(logfiles) <= 1:
            print("No logs avalible.")
            sys.exit(1)

        print("Avalible logs")
        for f in logfiles:
            print(' ', os.path.basename(f))
        sys.exit(0)

    def prog_log_clear():
        for f in logfiles:
            try:
                os.remove(f)
            except:
                print (os.path.basename(f), "seams to be in use.")
        print("Logs have been removed")
        sys.exit(0)

    if args.watch or args.watch == None:
        prog_log_watch(args.watch)

    if args.type:
        prog_log_list()

    if args.clear:
        prog_log_clear()

    # if nothing
    parser.parse_args(['log', '--help'])
    sys.exit(1)

# Project Program
def prog_project (args, parser):
    modList     = glob.glob(os.path.join(HoiModFolder, '*'))

    def prog_project_set(arg):
        if args.set == None:
            printExit('No mod project defined for set...'.format(arg), 1)
        if not os.path.exists(os.path.join(HoiModFolder, arg)):
            printExit('Mod "{}" does not exist...'.format(arg), 1)
        if currentProject == arg:
            printExit('Your project is already set to "{}"'.format(arg), 1)
        if not currentProject == "":
            setNewProject = confirm('Do you want to change path from "{}" to "{}"'.format(currentProject, arg))
        else:
            setNewProject = True
        if setNewProject:
            config.set('Project', 'current', args.set)
            with open(configFilePath, 'w') as configfile:
                config.write(configfile)
        else: 
            sys.exit(1)
        sys.exit(0)

    def prog_project_list():
        print("Avalible mods")
        for f in modList:
            if os.path.isdir(f):
                print(' ', os.path.basename(f))
        sys.exit(0)

    if args.set or args.set == None:
        prog_project_set(args.set)

    if args.list:
        prog_project_list()

    # if nothing
    parser.parse_args(['project', '--help'])
    sys.exit(1)


def prog_nudget (args, parser):
    nudgetAllDirectories = os.listdir(defaultLocalFolderPath)
    validNudgetFiles = ['history', 'states', 'localisation']
    nudgetDirectories = []
    for d in nudgetAllDirectories:
        if d in validNudgetFiles:
            nudgetDirectories.append(d)

    def prig_nudget_check():
        if len(nudgetDirectories) >= 1:
            print('Unsaved changed in your profile directory...')
            for d in nudgetDirectories:
                print(' ', d)
        else:
            print('No unsaved changed in your profile directory...')
        sys.exit(0)

    def prig_nudget_save(arg):
        arg = 'all' if arg == None else arg
        if not currentProject:
            print('No project defined')
            sys.exit(1)
        if len(nudgetDirectories) <= 0:
            print('No unsaved changed in your profile directory. Nothing to save!')
            sys.exit(1)

        if arg == 'all':
            for file in nudgetDirectories:
                src  = os.path.join(defaultLocalFolderPath,file)
                dest = os.path.join(HoiModFolder,currentProject,file)                
                print('Moveing', file, 'to your project directory...')
                shutil.copytree(src, dest, dirs_exist_ok=True)
                shutil.rmtree(src)
        sys.exit(0)

    if args.check:
        prig_nudget_check()

    if args.save or args.save == None:
        prig_nudget_save(args.save)

    # if nothing
    parser.parse_args(['nudge', '--help'])
    sys.exit(1)
    
def main():
    os.system("title hoidev")

    program_description="hoidev a developer, scripting and modding helper tool for Hearts of Iron 4."
    parser = argparse.ArgumentParser(
        prog='hoidev',
        description=program_description,
        epilog=''
    )
    subparsers = parser.add_subparsers()

    prog_parser_log = subparsers.add_parser('log',
        help='Log handler allow monitoring and clearing of logs',
        description=program_description)
    prog_parser_log.add_argument('--watch', '-w', nargs='?', metavar='<nothing>|filter', default=False,
        help='watch the latest log file (Optional parameter for filter)')
    prog_parser_log.add_argument('--log', '-l', nargs='?', metavar='log', default='game',
        help='watch a specific logfile (default; game) Use type to see other log names')
    prog_parser_log.add_argument('--highlight', '-i', action='store_true',
        help='highlight errors, warning, info and debug messages')
    prog_parser_log.add_argument('--type', '-t', action='store_true',
        help='list all avalible log types')
    prog_parser_log.add_argument('--clear', '-D', action='store_true',
        help='remove all log files')
    prog_parser_log.set_defaults(func=prog_log)

    prog_parser_project = subparsers.add_parser('project',
        help='project manager (Currect project: {})'.format(currentProject),
        description=program_description)
    prog_parser_project.add_argument('--list', '-l', action='store_true',
        help='list all avalible mods that can me defined as projects')
    prog_parser_project.add_argument('--set', nargs='?', metavar='MOD', default="",
        help='allow you to set a project based on folders in the mod directory (Current project: {})'.format(currentProject))
    prog_parser_project.set_defaults(func=prog_project)

    prog_parser_nudget = subparsers.add_parser('nudge',
        help='project nudge helper',
        description=program_description)
    prog_parser_nudget.add_argument('--check', '-c', action='store_true',
        help='check if there are unsaved changes')
    prog_parser_nudget.add_argument('--save', '-s', nargs='?', metavar='FILE', default="",
        help='allow to save nudget files to active project folder'.format(currentProject))
    prog_parser_nudget.set_defaults(func=prog_nudget)

    args = parser.parse_args()

    try: 
        args.func(args, parser)
    except AttributeError:
        parser.parse_args(['--help'])

if __name__ == "__main__":
    sys.exit(main())
