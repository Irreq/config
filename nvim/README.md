# Information

This is the help file for many of the commands in the neovim file


## Keybinds

<super>

Comment

	<leader>cc: comment
	<leader>cu: uncomment


IDE

    <leader>d: go to definition
    K: check documentation of class or method
    <leader>n: show the usage of a name in current file
    <leader>r: rename a name


## What's included

Files and folders for NeoVim

```text
nvim/
└── templates/
│   ├── py.template
│   ├── README.md.template
│   └── tex.template
├── init.vim
├── install.sh
└── README.md
```

# TemplateInit Placeholders


The Following placeholders are currently supported by this plugin
Date & Time

    DAY : Day of the week in short form (Mon, Tue, Wed, etc,)
    DAY_FULL : Day of the week in full (Monday, Tueseday, etc.)
    DATE : Date of the month (01 to 31)
    MONTH: Month of the year (01 to 12)
    MONTH_SHORT : Short name of the month (Jan, Feb, Mar, etc.)
    MONTH_FULL : Full month name (January, February, etc.)
    YEAR : current year (2016)
    TODAY: Todays date in dd/mm/yyyy format
    TIME : Current time in 24 our format
    TIME_12 : Current time in 12 hour format
    TIMESTAMP : Current Timestamp, e.g.: Sunday Nov 27, 2016 15:33:33 IST

Authoring

    NAME : Name of the author, g:tmpl_author_name, default : $USER
    HOSTNAME : Name of the host machine, g:tmpl_author_hostname, default : $HOSTNAME
    EMAIL : Email of the author, g:tmpl_author_email, default : $USER@$HOSTNAME

File name

    FILE : Basename of the file filename.ext -> filename
    FILEE : Filename with extension filename.ext -> filename.ext
    FILEF : Absolute path of the file /path/to/directory/filename.ext
    FILER : Filepath relative to the current directory (pwd)/relative/to/filename.ext
    FILED : Absolute path of the file's parent directory /path/to/directory
    FILEP : The file's parent directory /path/to/directory -> directory
    FILERD : Directory relative to the current directory (pwd)/relative/to/

License and Copyright

    LICENSE : License of the project, g:tmpl_license, default : MIT
    LICENSE_FILE : Reads lincese from license file onto the next line, g:tmpl_license_file. If no file path is provided then file is read in following order-
        LICENSE
        LICENSE.txt
        LICENSE.md
        license.txt
        license.md
    COPYRIGHT : Copyright message, g:tmpl_copyright, default : Copyright (c) g:tmpl_company

Others

    PROJECT : Name of the project, g:tmpl_project, default: not expanded
    COMPANY : Name of the company, g:tmpl_company, default: not expanded
    MACRO_GUARD : Macro guard for use in c/c++ files. filename.h -> FILENAME_H. All dots(.) and dashes (-) present in filename are converted into underscores (_).
    MACRO_GUARD_FULL : Same as MACRO_GUARD, except relative path is used in place of file name. e.g. relative/to/filename.h -> RELATIVE_TO_FILENAME_H
    CLASS : class name, same as FILE
    CAMEL_CLASS : class name converted to camel case long_file_name.txt -> LongFileName
    SNAKE_CLASS : class name converted to snake case LongFileName.txt -> long_file_name
    CURSOR : This is a spacial placeholder, it does not expand into anything but the cursor is placed at this location after the template expansion
