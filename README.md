# Instagram_Unfollower

Unfollows Instagram accounts that don't follow you back

## System Requirements
Name           | Terminal Command
---            | ---
Homebrew       | `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
Python 3       | `brew install python`
Firefox        | `brew cask install firefox`
Selenium       | `pip3 install selenium`

## Instructions
- open Terminal
- `cd` into `Instagram_Unfollower` directory
- type `python3 ig_unfollower.py 'USERNAME' 'PASSWORD'` in Terminal
    - For example, `python3 ig_unfollower.py 'lebronjames' 'imisskyrie'`
    - If your username and/or password contain spaces, '&', '[', '\', or any other special characters that throw off command line arguments, put single (or double) quotes around your username and/or password
    - Else, you don't have to :)
- list of unfollowers unfollowed is capped at 100
- feel free to update your whitelist in `python3 ig_unfollower.py` line 24 as needed

Fork or clone this repo and mod it any way you'd like :)
