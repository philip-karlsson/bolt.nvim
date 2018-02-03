# ⚡ bolt.nvim

⚡ Filter-as-you-type file manager for Neovim with emphasis on speed and visibility

_"Total Commander inspired file manager for the 21st century"_

## Demo

### Navigation
![Example Highlight](https://imgur.com/iES2mVQ.gif)

The filter is automatically updated as you type , no extra keystrokes needed.

### Searching
![Example Highlight](https://imgur.com/VBUnCBQ.gif)

Quicly perform a search in the active directory using [ripgrep](https://github.com/BurntSushi/ripgrep). If desired, expand the
results to see which lines that matches your pattern. For convenience, simply start
typing to filter your search results.

### Dual-pane
![Example Highlight](https://imgur.com/8uCxpO8.gif)

Unleash the commander using the multi-pane mode.

#### Notice

The development of Bolt.nvim is still in a **very early phase**, so bugs are expected. 
If you find something that needs fixing, please create an issue.

## Installation

**Note:** bolt.nvim requires Neovim(latest is recommended) with Python3 enabled.
See [requirements](#requirements) if you aren't sure whether you have this.

For vim-plug:

```vim

call plug#begin()

Plug 'philip-karlsson/bolt.nvim', { 'do': ':UpdateRemotePlugins' }

call plug#end()
```

## Requirements
bolt.nvim requires Neovim with Python3.
tIf `:echo has("python3")` returns `1`, then you have python 3 support; otherwise, see below.

You can enable the Neovim Python3 interface with pip:

    pip3 install neovim

### TODOs:
- Create proper vim documentation
- Complete the dual-pane mode
- Make it possible navigate archives (TC feature)
- Populate README.md with keybindings

## Self-Promotion
Like bolt.nvim? Make sure to follow the repository and why not leave a star.

## Thanks
Thanks for trying out this plugin, any feedback/contrubution would be much appreciated as
this is my first take on writing plugins for Neovim. Additionally, I would like to express my
cincere gratitude to Per-Åke Bligård and David Johansson for introducing me to the wonderful
world of unorthodox file managers 🍻

## Contributors
- Philip Karlsson
- David Johansson

## License
MIT License

Copyright (c) 2018 Philip Karlsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
