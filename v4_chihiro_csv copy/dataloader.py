#!/usr/bin/env python

import MySQLdb
import bisect



class DataLoader(object):
	def __init__(self, mysql_user = "root", mysql_password = "", mysql_db = "andrew", mysql_host = "localhost", filename = "~/Documents/CMU/2013-course/18697_Ole/smartspace/train_data/smartspacedatan/v4_chihiro_csv/cal.joined/110_readings.cal.csv"):
		self.mysql_user = "root"
		self.mysql_password = ""
		self.mysql_db = "andrew"
		self.mysql_host = "localhost"
		self.filename = filename
		print "Processing file", filename
		f = open(filename, "r")
		self.file_content = [x.split(',') for x in f.readlines()]
		f.close()
		self.processed_file = []
		self.timestamps = []
		for line in self.file_content:
			reading = self.process_one_reading(line)
			self.processed_file.append(reading)
			self.timestamps.append(reading["timestamp"])
		print "File processed"
		#print self.processed_file
		
	
	def process_one_reading(self, reading):
		res = {}
		#h, m = map(int, reading[0][8:].split(':'))
		#t = 3600*h + 60*m
		#res["timestamp"] = t
		res["timestamp"] = int(reading[1])
		res["temp"] = float(reading[2])
		res["light"] = float(reading[4])
		res["pressure"] = float(reading[6])
		res["audio_p2p"] = float(reading[8])
		res["people"] = float(reading[9])
		#print "Raw reading:", reading
		#print "Processed:", res
		return res
		
	
		
	def get_min_max_timestamps(self):
		_min = self.processed_file[0]["timestamp"]
		_max = self.processed_file[-1]["timestamp"]
		return _min, _max
	
	def fetch_all_macs(self):
		query = "SELECT mac FROM sensors"
		db = MySQLdb.connect(host = self.mysql_host, user = self.mysql_user, db = self.mysql_db, passwd = self.mysql_password)
		c = db.cursor()
		c.execute(query)
		res = [x[0] for x in c.fetchall()]
		c.close()
		db.close()
		return res
	
	def load_data_bundle(self, start, stop, device_mac = "aaa", norm_coeffs = "aaa"):
		count = 0
		res = []
		i_start = bisect.bisect_left(self.timestamps, start)
		i_stop = bisect.bisect_left(self.timestamps, stop)
		if self.timestamps[i_stop] != stop:
			i_stop -= 1
		if i_stop - i_start < 3:
			return 0, []
		for i in xrange(i_start, i_stop+1):
			reading = self.processed_file[i]
			#print reading
			tmp = []
			timestamp = reading['timestamp']
			if start <= timestamp <= stop:
				#print "start,timestamp,stop:",start,timestamp,stop
				people = reading['people']
				for key in [x for x in reading.keys() if x not in ['timestamp', 'people']]:
					tmp.append(reading[key])
				res.append( ([timestamp] + tmp, people) )
				count += 1
		if count < 3:
			count = 0
			res = []
		#print "count,res: ",count, res
		return count, res

	
def main():
	dl = DataLoader()
 #   for line in dl.processed_file:
 #	   print line
	print dl.get_min_max_timestamps()
	data = dl.load_data_bundle(0, 120)
	for l in data[1]:
		print l
		
if __name__ == "__main__":
	main()
