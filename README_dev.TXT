**Thunderbird Duplicate Email Remover**

Run app_gui.py to run the program

Write pytest to run the tests

TODO:
    More tests
    Hash all the message? Put option to choose that
    Checkboxes for mail folders???
    Update the comments

BUGS:
    Seems to not delete all duplicates. 
        First run:  "Total messages deleted across all mailboxes: 15294"
        Next run:   "Total duplicate messages deleted across all mailboxes: 1"


Logging levels

Level	    When to use
------------------------------------------
DEBUG	    Internal details
INFO	    Normal progress
WARNING	    Something unexpected but safe
ERROR	    Operation failed
CRITICAL	App cannot continue

Start with INFO.


INFORMATION:
    Zip compression level 1: Size: 2.05 GB, Backup duration: 2 minutes and 26.657 seconds
    Zip compression level 9: Size: 1.99 GB, Backup duration: 3 minutes and 33.458 seconds

    A small difference in size for a big difference in time. Keep the level low.