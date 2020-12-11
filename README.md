# check80
(This is for Japanese users)
This Python program patrols real estate company's websites and checks the latest sales information of lands with a building coverage ratio of 80% and reports via LINE notify service.

## Requirement
Python3  
LINE notify token  

## Python requirements.txt
>requests==2.25.0  
>beautifulsoup4==4.9.3  

## Setup
Rewrite LINE notify tokens(token).  
Rewrite URL lists(urls_xxxx).  
Rewrite Kanji name dictionary(dict_kanji).  
Place xxxx_history.txt as empty.  

## Usage
python check80.py

## Maintenance
When the history file grows larger, clear the contents.

## License
This software is released under the MIT License, see LICENSE.
https://opensource.org/licenses/mit-license.php

## Author
xuantum
https://github.com/xuantum
