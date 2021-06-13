"""" Enable Vundle: vim plugin manager

" required before Vundle initialization
" set nocompatible        " disable compatibility mode with vi
" filetype off            " disable filetype detection (but re-enable later, see below)

" set the runtime path to include Vundle, and initialize
" set rtp+=~/.vim/bundle/Vundle.vim
" call vundle#begin()
" Plugin 'VundleVim/Vundle.vim'
" Plugin 'wting/rust.vim' " enable syntax highlighting for rust
" call vundle#end()


"""" Basic Behavior

set number              " show line numbers
set wrap                " wrap lines
set encoding=utf-8      " set encoding to UTF-8 (default was "latin1")
set mouse=a             " enable mouse support (might not work well on Mac OS X)
set wildmenu            " visual autocomplete for command menu
set lazyredraw          " redraw screen only when we need to
set showmatch           " highlight matching parentheses / brackets [{()}]
set laststatus=2        " always show statusline (even with only single window)
set ruler               " show line and column number of the cursor on right side of statusline
set visualbell          " blink cursor on error, instead of beeping


"""" Key Bindings

" move vertically by visual line (don't skip wrapped lines)
nmap j gj
nmap k gk


"""" Vim Appearance

" use filetype-based syntax highlighting, ftplugins, and indentation
syntax enable
filetype plugin indent on

set statusline=%F%m%r%h%w%=(%{&ff}/%Y)\ (%l\,%c\)

"""" Tab settings

set tabstop=4           " width that a <TAB> character displays as
set expandtab           " convert <TAB> key-presses to spaces
set shiftwidth=4        " number of spaces to use for each step of (auto)indent
set softtabstop=4       " backspace after pressing <TAB> will remove up to this many spaces

set autoindent          " copy indent from current line when starting a new line
set smartindent         " even better autoindent (e.g. add indent after '{')


"""" Search settings

set incsearch           " search as characters are entered
set hlsearch            " highlight matches

" turn off search highlighting with <CR> (carriage-return)
nnoremap <CR> :nohlsearch<CR><CR>

"set autoread           " autoreload the file in Vim if it has been changed outside of Vim

set background=dark
hi clear

if exists('syntax on')
    syntax reset
endif

let g:colors_name='WhyDoWeNeedAName'
set t_Co=256

" major
hi Normal           guifg=#ffffff
hi Comment          guifg=#555753
hi Constant         guifg=#ffe70d
hi Identifier       guifg=#1d1de0
hi Statement        guifg=#fd55ff
hi PreProc          guifg=#3b41ff
hi Type             guifg=#37e637
hi Special          guifg=#00eeff
hi Underlined       guifg=#ff9c12
hi Ignore           guifg=#ff1919
hi Error            guifg=#ff0000
hi Todo             guifg=#a39393

" minor
hi String           guifg=#22d81c
hi Character        guifg=#ff0000
hi Number           guifg=#fc8414
hi Boolean          guifg=#fc8414
hi Float            guifg=#fc8414
hi Function         guifg=#32afff
hi Conditional      guifg=#fd55ff
hi Repeat           guifg=#fd55ff
hi Label            guifg=#0000ff
hi Operator         guifg=#ff0000
hi Keyword          guifg=#0000ff
hi Exception        guifg=#ff0000
hi Include          guifg=#fd55ff
hi Define           guifg=#34e2e2
hi Macro            guifg=#123456
hi PreCondit        guifg=#123456
hi StorageClass     guifg=#ff0000
hi Structure        guifg=#ffe70d
hi Typedef          guifg=#bfff00
hi SpecialChar      guifg=#0000ff
hi Tag              guifg=#0000ff
hi Delimeter        guifg=#0000ff
hi SpecialComment   guifg=#ffe70d
hi Debug            guifg=#00ff00


" major

hi Normal     guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Comment    guisp=NONE guifg=#555753 guibg=#282828 ctermfg=240 ctermbg=234 gui=NONE cterm=NONE
hi Constant   guisp=NONE guifg=#ffe70d guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Identifier guisp=NONE guifg=#1d1de0 guibg=#282828 ctermfg=20  ctermbg=234 gui=NONE cterm=NONE
hi Statement  guisp=NONE guifg=#fd55ff guibg=#282828 ctermfg=200 ctermbg=234 gui=NONE cterm=NONE
hi PreProc    guisp=NONE guifg=#3b41ff guibg=#282828 ctermfg=63  ctermbg=234 gui=NONE cterm=NONE
hi Type       guisp=NONE guifg=#37e637 guibg=#282828 ctermfg=77  ctermbg=234 gui=NONE cterm=NONE
hi Special    guisp=NONE guifg=#00eeff guibg=#282828 ctermfg=51  ctermbg=234 gui=NONE cterm=NONE
hi Underlined guisp=NONE guifg=#ff9c12 guibg=#282828 ctermfg=214 ctermbg=234 gui=NONE cterm=NONE
hi Ignore     guisp=NONE guifg=#ff1919 guibg=#282828 ctermfg=196 ctermbg=234 gui=NONE cterm=NONE
hi Error      guisp=NONE guifg=#ff0000 guibg=#282828 ctermfg=196 ctermbg=234 gui=NONE cterm=NONE
hi Todo       guisp=NONE guifg=#a39393 guibg=#282828 ctermfg=246 ctermbg=234 gui=NONE cterm=NONE

" minor
""source $MYVIMRC
hi String         guisp=NONE guifg=#22d81c guibg=#282828 ctermfg=40  ctermbg=234 gui=NONE cterm=NONE
hi Character      guisp=NONE guifg=#ff0000 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Number         guisp=NONE guifg=#fc8414 guibg=#282828 ctermfg=208 ctermbg=234 gui=NONE cterm=NONE
hi Boolean        guisp=NONE guifg=#fc8414 guibg=#282828 ctermfg=208 ctermbg=234 gui=NONE cterm=NONE
hi Float          guisp=NONE guifg=#fc8414 guibg=#282828 ctermfg=208 ctermbg=234 gui=NONE cterm=NONE
hi Function       guisp=NONE guifg=#32afff guibg=#282828 ctermfg=75  ctermbg=234 gui=NONE cterm=NONE
hi Conditional    guisp=NONE guifg=#fd55ff guibg=#282828 ctermfg=30  ctermbg=234 gui=NONE cterm=NONE
hi Repeat         guisp=NONE guifg=#fd55ff guibg=#282828 ctermfg=207 ctermbg=234 gui=NONE cterm=NONE
hi Label          guisp=NONE guifg=#0000ff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Operator       guisp=NONE guifg=#ff0000 guibg=#282828 ctermfg=196 ctermbg=234 gui=NONE cterm=NONE
hi Keyword        guisp=NONE guifg=#0000ff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Exception      guisp=NONE guifg=#ff0000 guibg=#282828 ctermfg=196 ctermbg=234 gui=NONE cterm=NONE
hi Include        guisp=NONE guifg=#fd55ff guibg=#282828 ctermfg=207 ctermbg=234 gui=NONE cterm=NONE
hi Define         guisp=NONE guifg=#34e2e2 guibg=#282828 ctermfg=80  ctermbg=234 gui=NONE cterm=NONE
hi Macro          guisp=NONE guifg=#123456 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi PreCondit      guisp=NONE guifg=#123456 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi StorageClass   guisp=NONE guifg=#ff0000 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Structure      guisp=NONE guifg=#ffe70d guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Typedef        guisp=NONE guifg=#bfff00 guibg=#282828 ctermfg=154 ctermbg=234 gui=NONE cterm=NONE
hi SpecialChar    guisp=NONE guifg=#0000ff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Tag            guisp=NONE guifg=#0000ff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Delimiter      guisp=NONE guifg=#0000ff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SpecialComment guisp=NONE guifg=#ffe70d guibg=#282828 ctermfg=220 ctermbg=234 gui=NONE cterm=NONE
hi Debug          guisp=NONE guifg=#00ff00 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
