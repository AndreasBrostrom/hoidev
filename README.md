# armadev
Arma dev is a one script stop shop for arma development. The tool alow you monitor clear rpt logs, setup your p drive enviroment mount, unmount it and even switch its location. The tool also allow for you to run a project build and make scripts.


## Requirements
- [Python 3](https://www.python.org/downloads/)
- [Arma 3 Tools](https://store.steampowered.com/app/233800/Arma_3_Tools/)
- [Miklos Tools](https://mikero.bytex.digital/Downloads)

## Help outputs
```
usage: armadev [-h] {rpt,proj,p,addon,tools} ...

armadev a developer, scripting and modding helper tool for ARMA 3.

positional arguments:
  {rpt,proj,p,addon,tools}
    rpt                 RPT log handler allow monitoring and clearing of logs
    proj                Arma 3 project handler (This script require a git project intorder to function propperly)
    p                   Arma 3 P-drive handler (Path: "D:\Arma3\", Mounted: No)
    addon               Arma 3 Addon unpacker
    tools               List all avalible tools you have installed

optional arguments:
  -h, --help            show this help message and exit
```

### RPT
```
usage: armadev rpt [-h] [--watch [<nothing>|filter]] [--list] [--clear]

armadev a developer, scripting and modding helper tool for ARMA 3.

optional arguments:
  -h, --help            show this help message and exit
  --watch [<nothing>|filter], -w [<nothing>|filter]
                        watch the latest rpt file (Optional parameter for filter)
  --list, -l            list all avalible rpt logs
  --clear, -D           remove all rpt log files
```

### Project
```
usage: armadev proj [-h] [--check] [--make [<nothing>|arguments]] [--build [<nothing>|arguments]]

Arma 3 project handler

optional arguments:
  -h, --help            show this help message and exit
  --check, -c           check what type of project
  --make [<nothing>|arguments], -m [<nothing>|arguments]
                        run make script
  --build [<nothing>|arguments], -b [<nothing>|arguments]
                        run build script
```

### P-drive
```
usage: armadev p [-h] [--mount] [--umount] [--set PATH] [--open]

Arma 3 P-drive handler (Path: "D:\Arma3\", Mounted: No)

optional arguments:
  -h, --help    show this help message and exit
  --mount, -m   mount the arma 3 P-drive
  --umount, -u  unmount the arma 3 P-drive
  --set PATH    Set P-drive location
  --open, -o    Open p dive path in explorer
```

### Addon 
```
usage: armadev addon [-h] [--unpack MODNAME] [--force] [--list] [--browse]

Arma 3 Addon unpacker

optional arguments:
  -h, --help            show this help message and exit
  --unpack MODNAME, -u MODNAME
                        Unpack a mods pbos and debinirize the configs
  --force, -F           Force unpacking by removing and replacing already exisint
  --list, -l            List all workshop mods
  --browse, -b          Opens the !Workshop directory
```