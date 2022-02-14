import asyncio
from core.gefs.gefs_data_handler import GEFSHandler
from core.utils import filter_list

gefs_handler = GEFSHandler(date='20220210')

gefs_handler.set_hour(00)

hour = gefs_handler.get_hour()

# gefs_handler.get_gefs_aws_data(file_search_pattern=f'gec{hour}.t{hour}',
#                                save_path='/usr/src/app/src/core/gefs')

gefs_handler.get_gefs_aws_data(file_search_pattern=r'gep[0-9]{2}.t[0-9]{2}z.pgrb2b.0p50.f[0-9]{3}$',
                               save_path='/usr/src/app/src/data/gefs/ensemble')



#ver limite de conexões simultãneas
