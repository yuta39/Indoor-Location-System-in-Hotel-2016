import pymysql.cursors

connector = pymysql.connect(host="localhost", port=33333 , db="sampledb", user="wiss_challenge", passwd="wiss_challenge_2016", charset="utf8",cursorclass=pymysql.cursors.DictCursor)
#connector = pymysql.connect(host="localhost", port=33333 , db="sampledb", user="root",passwd="root", charset="utf8",cursorclass=pymysql.cursors.DictCursor)
cursor = connector.cursor()


f = open("/Users/wiss_charange/Wiss/flask/room_mac.txt")
line1 = f.readlines()
for l in line1:
	ss=l[:-1].split("\t")
	room = ss[0]
	mac = ss[1]
	insert_line = 'insert into sampledb.room_uuid values(%d,"%s")' % (int(room),mac)
	print(cursor.execute(insert_line))

connector.commit()