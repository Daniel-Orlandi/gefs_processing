from asyncio.log import logger
import datetime
import asyncio

from core.aws.aws_downloader import NoaaAwsDownloader
from core.utils.data_logger import Logger 
from core.utils import filter_list, create_folder


class GEFSHandler:
  def __init__(self, date:str = None) -> None:
    self.logger = Logger(logger_name=__name__).get_logger()

    if(not date):
      self.date = datetime.datetime.today()
    
    else:
      self.date = datetime.datetime.strptime(date,'%Y%m%d')
      
    self.aws_gefs_bucket = 'noaa-gefs-pds'
    self.aws_gefs_prefix = f'gefs.{self.date.strftime("%Y%m%d")}/{self.date.strftime("%H")}/atmos/pgrb2b'
    self.aws_gefs_prefix_secondary = f'gefs.{self.date}/{self.date.strftime("%H")}/atmos/pgrb2b'
    self.file_list = None
    self.noaa_downloader = NoaaAwsDownloader()


  def set_hour(self, hour:int) -> None:    
    self.date = self.date.replace(hour=hour)
    logger.info(f'Hour set to: {self.date}')
  
  def get_hour(self) -> str:
    return self.date.strftime('%H')


  def get_gefs_aws_data(self, file_search_pattern:str, save_path:str):
    logger.info(f'Downloading files: {file_search_pattern}')
    create_folder(save_path)

    file_list = asyncio.run(self.noaa_downloader.list_bucket(bucket_name=self.aws_gefs_bucket,
                                                             prefix=self.aws_gefs_prefix,
                                                             over_1000=True))
    logger.info(f'filtering initial file list') 
    self.file_list = filter_list(file_list, file_search_pattern)

    asyncio.run(self.noaa_downloader.download_file_list(file_list=self.file_list,
                                                        bucket_name=self.aws_gefs_bucket,
                                                        save_path=save_path))

    logger.info(f'Done.') 


      
