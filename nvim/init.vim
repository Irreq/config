"******************************************************************************
" Irreq Neovim Config File
"******************************************************************************

let vimplug_exists=expand('~/.config/nvim/autoload/plug.vim')

let g:vim_bootstrap_langs = "python"
let g:vim_bootstrap_editor = "nvim"

if !filereadable(vimplug_exists)
  echo "Installing Vim-Plug..."
  echo ""
  silent !\curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  let g:not_finish_vimplug = "yes"

  autocmd VimEnter * PlugInstall
endif

" Required:
call plug#begin(expand('~/.config/nvim/plugged'))


"******************************************************************************
"" Plug install packages
"******************************************************************************

" Templates
Plug 'tibabit/vim-templates'
" Usage: TemplateInit <language>
let g:tmpl_search_paths = ['~/github/config/nvim/templates']
let g:tmpl_author_email = 'irreq@protonmail.com'

"" Tex
"Plug 'lervag/vimtex'
"" Usage:
"" latexmk -pdf -pvc test.tex
"let g:tex_flavor='latex'
"let g:vimtex_view_method='zathura'
"let g:vimtex_quickfix_mode=0

" IDE
Plug 'davidhalter/jedi-vim'
" Usage:
" <leader>d: go to definition
" K: check documentation of class or method
" <leader>n: show the usage of a name in current file
" <leader>r: rename a name
let g:jedi#completions_enabled = 0 " disable, because we use deoplete for completion
let g:jedi#use_splits_not_buffers = "right" " open the go-to function in split

" Code Completion
Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
Plug 'zchee/deoplete-jedi'
let g:deoplete#enable_at_startup = 1

Plug 'deoplete-plugins/deoplete-clang'

" Code Checking Python
Plug 'neomake/neomake'
let g:neomake_python_enabled_makers = ['pylint']

" Auto Pairs
Plug 'jiangmiao/auto-pairs'

" Language Specific Commenting
Plug 'scrooloose/nerdcommenter'
" Usage:
" <leader>cc: comment
" <leader>cu: uncomment

" Code Auto-Format
Plug 'sbdchd/neoformat'
" Usage:
" :Neoformat
let g:neoformat_basic_format_align = 1 " Enable alignment
let g:neoformat_basic_format_retab = 1 " Enable tab to space conversion
let g:neoformat_basic_format_trim = 1 " Enable trimmming of trailing whitespace

" Multiple cursors
Plug 'mg979/vim-visual-multi', {'branch': 'master'}
"    select words with Ctrl-N (like Ctrl-d in Sublime Text/VS Code)
"    create cursors vertically with Ctrl-Down/Ctrl-Up
"    select one character at a time with Shift-Arrows
"    press n/N to get next/previous occurrence
"    press [/] to select next/previous cursor
"    press q to skip current and get next occurrence
"    press Q to remove current cursor/selection
"    start insert mode with i,a,I,A

" Code Snippets
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'


" Trigger configuration. You need to change this to something other than <tab> if you use one of the following:
" - https://github.com/Valloric/YouCompleteMe
" - https://github.com/nvim-lua/completion-nvim
let g:UltiSnipsExpandTrigger="<tab>"
let g:UltiSnipsJumpForwardTrigger="<c-b>"
let g:UltiSnipsJumpBackwardTrigger="<c-z>"

" Code Folding
Plug 'tmhedberg/SimpylFold'
" Usage:
" zo: Open fold in current cursor position
" zO: Open fold and sub-fold in current cursor position recursively
" zc: Close the fold in current cursor position
" zC: Close the fold and sub-fold in current cursor position recursively

" Visible Yank
Plug 'machakann/vim-highlightedyank'
let g:highlightedyank_highlight_duration = 1000 " Highlight 1000 ms

" File Explorer
Plug 'scrooloose/nerdtree'
let NERDTreeShowHidden=1
let NERDTreeQuitOnOpen=1 " Auto Close
nnoremap <C-\> :NERDTreeToggle<CR>

" Theme
Plug 'https://github.com/joshdick/onedark.vim'

" Syntax Highlight
" Plug 'numirias/semshi', { 'do': ':UpdateRemotePlugins' }



" VimTex

Plug 'lervag/vimtex'

" This is necessary for VimTeX to load properly. The "indent" is optional.
" Note that most plugin managers will do this automatically.
filetype plugin indent on

" This enables Vim's and neovim's syntax-related features. Without this, some
" VimTeX features will not work (see ":help vimtex-requirements" for more
" info).
syntax enable

" Viewer options: One may configure the viewer either by specifying a built-in
" viewer method:
let g:vimtex_view_method = 'mupdf'

" Or with a generic interface:
"let g:vimtex_view_general_viewer = 'okular'
"let g:vimtex_view_general_options = '--unique file:@pdf\#src:@line@tex'

" VimTeX uses latexmk as the default compiler backend. If you use it, which is
" strongly recommended, you probably don't need to configure anything. If you
" want another compiler backend, you can change it as follows. The list of
" supported backends and further explanation is provided in the documentation,
" see ":help vimtex-compiler".
let g:vimtex_compiler_method = 'latexrun'

let g:tex_flavor = 'latex'
" Most VimTeX mappings rely on localleader and this can be changed with the
" following line. The default is usually fine and is the symbol "\".
let maplocalleader = ","


" Tex Live Preview

" A Vim Plugin for Lively Previewing LaTeX PDF Output
Plug 'xuhdev/vim-latex-live-preview', { 'for': 'tex' }
" USAGE: :LLPStartPreview 

"let g:livepreview_previewer = 'mupdf'
let g:livepreview_previewer = 'okular'
call plug#end()

"*****************************************************************************
" Basic Setup
"*****************************************************************************

" Encoding
set encoding=utf-8
set fileencoding=utf-8
set fileencodings=utf-8
set bomb
set binary

let mapleader=' ' " Space

" Press i to enter insert mode, and ii to exit insert mode.
:inoremap ii <Esc>

"*****************************************************************************
" Visual Settings
"*****************************************************************************

set ruler
set number
set relativenumber
set showcmd
set statusline=%F%m%r%h%w%=(%{&ff}/%Y)\ \%l/\%L,\%c

syntax enable
colorscheme onedark
set background=dark

"*****************************************************************************
" Plugs
"*****************************************************************************
call neomake#configure#automake('nrwi', 500) " Start Code Checking
