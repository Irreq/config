"*****************************************************************************
"" Irreq NEOVIM
"*****************************************************************************
if has('vim_starting')
  set nocompatible               " Be iMproved
endif

let vimplug_exists=expand('~/.config/nvim/autoload/plug.vim')

let g:vim_bootstrap_langs = "python"
let g:vim_bootstrap_editor = "nvim"				" nvim or vim

if !filereadable(vimplug_exists)
  echo "Installing Vim-Plug..."
  echo ""
  silent !\curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  let g:not_finish_vimplug = "yes"

  autocmd VimEnter * PlugInstall
endif

" Required:
call plug#begin(expand('~/.config/nvim/plugged'))

"*****************************************************************************
"" Plug install packages
"*****************************************************************************
Plug 'tibabit/vim-templates'
" Usage: TemplateInit <language>
let g:tmpl_search_paths = ['~/github/config/nvim/templates']

let g:tmpl_author_email = 'irreq@protonmail.com'

Plug 'lervag/vimtex'
" latexmk -pdf -pvc test.tex
let g:tex_flavor='latex'
let g:vimtex_view_method='zathura'
let g:vimtex_quickfix_mode=0




" For tex completion
Plug 'sirver/ultisnips'
let g:UltiSnipsExpandTrigger = '<tab>'
let g:UltiSnipsJumpForwardTrigger = '<tab>'
let g:UltiSnipsJumpBackwardTrigger = '<s-tab>'





Plug 'Raimondi/delimitMate'

Plug 'davidhalter/jedi-vim'
" disable autocompletion, because we use deoplete for completion
let g:jedi#completions_enabled = 0

" open the go-to function in split, not another buffer
let g:jedi#use_splits_not_buffers = "right"

Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
let g:deoplete#enable_at_startup = 1
Plug 'zchee/deoplete-jedi'

Plug 'scrooloose/nerdcommenter'
" To comment <leader>cc and uncomment <leader>uc

Plug 'iamcco/markdown-preview.nvim', { 'do': { -> mkdp#util#install() }, 'for': ['markdown', 'vim-plug']}


Plug 'sbdchd/neoformat'
" Enable alignment
let g:neoformat_basic_format_align = 1

" Enable tab to space conversion
let g:neoformat_basic_format_retab = 1

" Enable trimmming of trailing whitespace
let g:neoformat_basic_format_trim = 1

autocmd InsertLeave,CompleteDone * if pumvisible() == 0 | pclose | endif
inoremap <expr><tab> pumvisible() ? "\<c-n>" : "\<tab>"


Plug 'neomake/neomake'
let g:neomake_python_enabled_makers = ['pylint']


"Multiple cursors
Plug 'mg979/vim-visual-multi', {'branch': 'master'}

Plug 'machakann/vim-highlightedyank'
" set highlight duration time to 1000 ms, i.e., 1 second
let g:highlightedyank_highlight_duration = 1000

Plug 'tmhedberg/SimpylFold'
"     zo： Open fold in current cursor position
"     zO： Open fold and sub-fold in current cursor position recursively
"     zc： Close the fold in current cursor position
"     zC： Close the fold and sub-fold in current cursor position recursively

Plug 'vim-python/python-syntax'


" python
" vim-python
augroup vimrc-python
  autocmd!
  autocmd FileType python setlocal expandtab shiftwidth=4 tabstop=8 colorcolumn=79
      \ formatoptions+=croq softtabstop=4 smartindent
      \ cinwords=if,elif,else,for,while,try,except,finally,def,class,with
augroup END


call plug#end()


function! Multiple_cursors_before()
    let b:deoplete_disable_auto_complete = 1
endfunction

function! Multiple_cursors_after()
    let b:deoplete_disable_auto_complete = 0
endfunction


call neomake#configure#automake('nrwi', 500)

" syntastic
let g:syntastic_python_checkers=['python', 'flake8']

"*****************************************************************************
"" Basic Setup
"*****************************************************************************"
"" Encoding
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8
set bomb
set binary

"" Map leader to ,
let mapleader=','


"*****************************************************************************
"" Visual Settings
"*****************************************************************************syntax on
set ruler
set number
set relativenumber
set showcmd
set statusline=%F%m%r%h%w%=(%{&ff}/%Y)\ \%l/\%L,\%c

"" Set relive and regular number
"" function to toggle number mode
"function! g:ToggleNuMode()
    "if(&rnu == 1)
        "set number
    "else
        "set relativenumber
    "endif
"endfunc

"" map the above function to F5
"nnoremap <f5> :call g:ToggleNuMode()<cr>

"syntax on
syntax enable
set termguicolors


set background=dark
hi clear

if exists('syntax on')
    syntax reset
endif

let g:colors_name='WhyDoWeNeedAName'
set t_Co=256


" misc

hi ColorColumn      guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Conceal          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Cursor           guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi lCursor          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi CursorIM         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi CursorColumn     guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi CursorLine       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Directory        guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi DiffAdd          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi DiffChange       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi DiffDelete       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi DiffText         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi EndOfBuffer      guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi ErrorMsg         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi VertSplit        guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Folded           guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi FoldColumn       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SignColumn       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi IncSearch        guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi LineNr           guisp=NONE guifg=#555753 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi LineNrAbove      guisp=NONE guifg=#555753 guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi LineNrBelow      guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi CursorLineNr     guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi MatchParen       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi ModeMsg          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi MoreMsg          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi NonText          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Pmenu            guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi PmenuSel         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi PmenuSbar        guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi PmenuThumb       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Question         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi QuickFixLine     guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Search           guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SpecialKey       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SpellBad         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SpellCap         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SpellLocal       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi SpellRare        guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi StatusLine       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi StatusLineNC     guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi StatusLineTerm   guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi StatusLineTermNC guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi TabLine          guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi TabLineFill      guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi TabLineSel       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Terminal         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Title            guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi Visual           guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi VisualNOS        guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi WarningMsg       guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE
hi WildMenu         guisp=NONE guifg=#ffffff guibg=#282828 ctermfg=231 ctermbg=234 gui=NONE cterm=NONE

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
