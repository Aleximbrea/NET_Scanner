# Network Scanner
## Requirements
- Python 3
- Windows 10 / 11

## Get started

1. Check Python installation `python --version`
2. Clone this repository
3. Navigate to the directory with a terminal. **The terminal must have administrator privileges**
4. Install packages ``pip install -r requirements.txt``
5. Execute the script `python main.py`
   
   


## Important
  - ***The script only works with English or Italian system languages***
    
      To check for active connections i use the `netsh interface show interface` command which returns an output based on the system language
      To filter the resaults i use the following statement:
      ```python
        if status == 'Connessione' or status == 'Connected':
      ```
      So if you are using another language it wont find active interfaces