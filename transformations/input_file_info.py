from dataclasses import dataclass

@dataclass
class InputFileItem:
   """This will keep track of a file"""
    name: str
    img_type: str
    is_valid: bool
    time_stamp: str  #change to date/time later
    f_path: str
    is_remote: bool



# export InputFileItem