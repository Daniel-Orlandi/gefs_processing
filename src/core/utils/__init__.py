import re
from pathlib import Path
from unittest import result


def create_folder(path:str)->None:
    try:      
      path = Path(path)
      if (not path.is_dir()):
        path.mkdir(parents=True, exist_ok=True)

    except Exception as error:
      raise error


def filter_list(string_list:str, pattern:str) -> list:
  filtered_list = []

  for each_item in string_list:
    if(re.search(pattern, each_item)):
      filtered_list.append(each_item)

  return filtered_list

