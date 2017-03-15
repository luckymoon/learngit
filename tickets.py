#coding:utf-8
"""Train tickets query via command-line.


Usage:
	tickets [-gdtkz] <from> <to> <date>

Options:
	-h,--help		显示帮助菜单
	-g			高铁
	-d			动车
	-t			特快
	-k			快速
	-z			直达

Example:
	tickets -dg 南京 北京 2016-07-01
"""

from docopt import docopt
from id import stations
import json
import requests	
from prettytable import PrettyTable
from termcolor import colored, cprint
import time
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
def _get_duration(row):
	duration = row.get('lishi').replace(':', '小时') + '分钟'
	# take 0 hour , only show minites
	if duration.startswith('00'):
	    return duration[4:]
	# take <10 hours, show 1 bit
	if duration.startswith('0'):
	    return duration[1:]
	return duration

def _get_selecttrain(row):
	m=re.match(r"\w",row.get('station_train_code'))
	print m.group(0)

def cli():
	arguments=docopt(__doc__)
	from_station = stations.get(arguments['<from>'].decode('utf-8'))
	to_station = stations.get(arguments['<to>'].decode('utf-8'))
	date = arguments['<date>']
	#print from_station,to_station,date
	url='https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate='+date+'&from_station='+from_station+'&to_station='+to_station
	r=requests.get(url,verify=False)
	rows=r.json()['data']['datas']
	headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
	pt=PrettyTable()
	pt._set_field_names(headers)
	
	options=sys.argv[1]
	optionlst=None
	if options.startswith('-'):
		optionlst= [x.upper()  for x in options if x in 'dgktz']

	for row in rows:
		train_no=row.get('station_train_code')
		initial = train_no[0]
		if not optionlst  or initial in optionlst:
			train = [
			    # Column: '车次'
			    row.get('station_train_code'),
			    # Column: '车站'
			    '\n'.join([
				colored(row.get('from_station_name'),'green',attrs=['bold']),
				#row.get('from_station_name'),
				colored(row.get('to_station_name'),"red",attrs=['bold'])
			    ]),
			    # Column: '时间'
			    '\n'.join([
				colored(row.get('start_time'),"green",attrs=['bold']),
				colored(row.get('arrive_time'),"red",attrs=['bold'])
			    ]),
			    # Column: '历时'
			    #self._get_duration(row),
			    _get_duration(row),
			    # Column: '商务'
			    row.get('swz_num'),
			    # Column: '一等'
			    row.get('zy_num'),
			    # Column: '二等'
			    row.get('ze_num'),
			    # Column: '软卧'
			    row.get('rw_num'),
			    # Column: '硬卧'
			    row.get('yw_num'),
			    # Column: '软座'
			    row.get('rz_num'),
			    # Column: '硬座'
			    row.get('yz_num'),
			    # Column: '无座'
			    row.get('wz_num')
			]
			pt.add_row(train)
	print(pt)
if __name__=='__main__':
	cli()
	"""
	'\n'.join([
	colored.green(row.get('from_station_name')),
	colored.red(row.get('to_station_name')),
	]),
	# Column: '时间'
	'\n'.join([
	colored.green(row.get('start_time')),
	colored.red(row.get('arrive_time')),
	]),
	"""
