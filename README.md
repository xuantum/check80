# check80
This Python program patrols real estate information websites and checks the latest information on the sale of land with a building coverage ratio of 80% and reports via LINE notify service.

## Requirement
Python3  
LINE notify token  

## Python requirements.txt
>requests==2.25.0  
>beautifulsoup4==4.9.3  

## Setup
Rewrite LINE notify tokens(token).  
Rewrite URL lists(urls_<name>).  
Rewrite Kanji name dictionary(dict_kanji).  
Place <name>_history.txt as empty.  

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
