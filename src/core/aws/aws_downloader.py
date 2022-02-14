
import os
import asyncio
import functools
import concurrent.futures

import boto3
from botocore import UNSIGNED
from botocore.config import Config

import core.utils as utils
from core.utils.data_logger import Logger


class NoaaAwsDownloader:
  def __init__(self, config=None) -> None:
    self.logger = Logger(logger_name=__name__).get_logger()
    
    if (config):
      self.s3_client = boto3.client('s3',config=config)

    else:
      self.s3_client = boto3.client('s3',config=Config(signature_version=UNSIGNED, 
                                                     retries = {'max_attempts': 5,
                                                                'mode': 'standard'}))       
    self.executor = concurrent.futures.ThreadPoolExecutor() 
  

  @staticmethod
  def get_content(data_list):
    if ('Contents' not in data_list):
       raise FileNotFoundError (f'empty')       
     
    else:
       file_name_list = []

       for item in data_list['Contents']: 
        key = item['Key']        
        #file_name = key.split('/')[-1].split('.')[0]
        file_name_list.append(key)

       return file_name_list
  

  def list_over_1000(self, bucket_name:str, prefix:str, **kwargs) -> list:
    s3_paginator = self.s3_client.get_paginator('list_objects_v2')
    pages = s3_paginator.paginate(Bucket=bucket_name, Prefix=prefix, **kwargs)

    file_list = []
    for page in pages:      
      [file_list.append(obj['Key']) for obj in page['Contents']]
    
    return file_list


  async def list_bucket(self, bucket_name:str, prefix:str, over_1000 = False, **kwargs) -> list:
    try:
      self.logger.info(f'Listing files in bucket: {bucket_name}\n with prefix: {prefix}')
      if(over_1000 == True):
        self.logger.warning(f'over 1000 limit = {over_1000}')
        s3_result = functools.partial(self.list_over_1000, bucket_name=bucket_name, prefix=prefix, **kwargs)
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(self.executor, s3_result)

      else:
        s3_result = functools.partial(self.s3_client.list_objects_v2,Bucket=bucket_name, Prefix=prefix)
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(self.executor, s3_result)
        result = self.get_content(result)          
 
    except Exception as error:
      self.logger.error(error)
    
    else:
      self.logger.info(f'Done.')
      return result
  

  async def download_file(self, bucket_name, file_name:str, save_path:str, **kwargs) -> None:
    try:
      self.logger.info(f'Creating: {save_path} if it does not exists')      

      self.logger.info(f'Downloading:{file_name}/ Saving to:{save_path}')
      s3_result = functools.partial(self.s3_client.download_file,
                                    Bucket=bucket_name,
                                    Key=file_name,
                                    Filename=f'{save_path}/{os.path.basename(file_name)}',
                                    **kwargs)

      loop = asyncio.get_running_loop()
      await loop.run_in_executor(self.executor, s3_result)
    
    except Exception as error:
      self.logger.error(f'Download error:\n {error}')
    
    else:
      self.logger.info(f'Done.')      
  

  async def download_file_list(self, bucket_name:str, file_list:str, save_path:str) -> None:
    self.logger.info(f'Downloading list:\n {file_list}')
    task_list = []
    for file in file_list:
      task = self.download_file(bucket_name=bucket_name, file_name=file, save_path=save_path)
      task_list.append(task)
    
    await asyncio.gather(*task_list)
    self.logger.info(f'Done.')
