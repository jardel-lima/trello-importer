# Trello Importer

If you use Trello to keep track of your tasks, you can use this script to easily create your Board, List and 
Cards on your Trello account using a CSV file. All you need to do is to create a CSV file and execute this script.

## The CSV file

The CSV must have the following structure:

|Board Name | <board_name> |               |        |
|-----------|------------- |-------------- |--------|
|**List**   |**Card**      |**Description**|**Time**|
|\<lista A\>|<card 1>      |<description 1>|1       |
|           |<card 2>      |               |2       |
|           |<card 3>      |               |1       |
|\<lista B\>|<card 4>      |<description 2>|1       |
|           |<card 5>      |               |2       |

In this structure ```<board_name>``` is the board's name that you want to create or it can be the board's id if you want
to add lists and cards to an existing board. In the **List** column you must insert the name of the List you want to create, in the **Card** column
you must insert the name of the Card you want to create. The **Description** column is used to set a description to the card you 
are creating. In the **Time** column you must put the amount of estimated time 
 to complete the task associated to the card. If you use the web browser extension _*Scrum for Trello*_ 
([_Firefox_](https://addons.mozilla.org/pt-BR/firefox/addon/scrum-for-trello/),
[_Chrome_](https://chrome.google.com/webstore/detail/scrum-for-trello/jdbcdblgjdpmfninkoogcfpnkjmndgje)), this time will
be used as a storypoint. 

**This file must be saved with ``UTF-8`` encoding and ``TAB`` (``'\t'``) as column separator.**

## The config file

This script has a config file called ``trello_importer.config`` in the ``conf`` folder, it has just two variables:

````buildoutcfg
API_KEY=<\api_key\>
ORGANIZATION_ID=<\organization_id\>
````  

The ``API_KEY`` is your Trello API key and it is mandatory to execute this script, you can get this key
 [here](https://developers.trello.com/). The ``ORGANIZATION_ID`` is the organization id of your organization on _Trello_, 
 it is used to set the board as a organization board. The ``ORGANIZATION_ID`` is optional.
 
 ## Requirements
 
 To run this script you need to install python 2.7 and install the library ``requests``. To install the library 
 ``requests`` run the following command  after you install python:
 
 ````buildoutcfg
pip install requests
````

## Running the script

To run this script set your Trello API Key on the ``trello_importer.config`` file, create the CSV file as explained on 
the section **_The CSV file_** and save it on the same folder of the script as ``file.csv`` and execute the script with
the command:
````buildoutcfg
python trello_importer.py
````
 You can also save the CSV file with whatever name you want and whatever place you wish, but you will have to inform the
 file's location to the script, as example:
 
 ````buildoutcfg
python trello_importer.py ../path/to/file/my_csv.csv
````

This will open the Trello's authentication page, accept, copy the generated token, past it on the terminal and hit ``Enter``, the script 
will proceed.

## Author

Jardel Ribeiro de Lima 
- [_Linkdin_](https://br.linkedin.com/in/jardelribeirolima)
- [_GitHub_](https://github.com/jardel-lima)


 
