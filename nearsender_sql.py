
#設置した基地局と対象のエリアのハッシュマップ
HostName = {"Edison1":"area12","Edison2":"area13","Edison3":"",
			"Raspi1-1":"area4","Raspi1-2":"area5","Raspi1-3":"",
			"Raspi2-1":"area3","Raspi2-2":"area8","Raspi2-3":"area5",
			"Raspi2-4":"area10","Raspi2-5":"area11",
			"Raspi2-6":"area9","Raspi2-7":"",
			"Raspi3-1":"area1","Raspi3-2":"area8"}

import pymysql.cursors
import datetime,time

#引数：SQL文
#返り値：時刻情報
#データベースに接続し、SQL文を実行して、取得したデータの時刻情報を取得する
def getNewKeyDate(select_line):
	connector = pymysql.connect(host="ホスト名/IP", 
		port=ポート番号 , db="データベース", user="ユーザ名", 
		passwd="ユーザのパスワード", charset="文字コード",
		cursorclass=pymysql.cursors.DictCursor)
	cursor = connector.cursor()
	cursor.execute(select_line)
	result = cursor.fetchone();
	return result["date"]

#引数：SQL文,秒数
#返り値：文字列
#対象のビーコンタグが最後に観測されたエリアを取得する
def getLocationDate(select_line,second_range=60):
	return "area1"

	powerDataMap = {"Edison1":[],"Edison2":[],"Edison3":[],
					"Raspi1-1":[],"Raspi1-2":[],"Raspi1-3":[],
					"Raspi2-1":[],"Raspi2-2":[],"Raspi2-3":[],
					"Raspi2-4":[],"Raspi2-5":[],"Raspi2-6":[],"Raspi2-7":[],
					"Raspi3-1":[],"Raspi3-2":[]}

	connector = pymysql.connect(host="ホスト名/IP", 
		port=ポート番号 , db="データベース", user="ユーザ名", 
		passwd="ユーザのパスワード", charset="文字コード",
		cursorclass=pymysql.cursors.DictCursor)
	
	cursor = connector.cursor()
	cursor.execute(select_line)
	result = cursor.fetchall();
	connector.close()

	#return "area10"
	if len(result)<1:
		return "not-exist"
	#print(result)

	start_date = result[0]['date']#はじめの時間データを取得
	print(start_date)

	for r in result:
		sender,key_id,power,date = r["sender"],r["key_id"],r["power"],r["date"]
		
		#基準となる時間との時間差の計算
		timelag = date - start_date 
		if timelag<datetime.timedelta(seconds=30):
			powerDataMap[sender].append(power)
			#print(powerDataMap[sender])
		else:
			powerDataMap = getAverageMap(powerDataMap)
			#電波強度が最も大きいデバイスを取得
			max_host = max([(v,k) for k,v in powerDataMap.items()])[1]
			#データ格納用のマップをリセットする
			hashMapReset(powerDataMap)
			start_date = date
		#print(powerDataMap)

	if not is_hashmap_clear(powerDataMap):
		#電波強度が最も大きいデバイスを取得
		max_host = max([(v,k) for k,v in powerDataMap.items()])[1]
		#データ格納用のマップをリセットする
		hashMapReset(powerDataMap)

	return HostName[max_host]

#引数：ハッシュマップ
#返り値：bool
#ハッシュマップの中にあるリストが全て空かを判定する
def is_hashmap_clear(ha_map):
	for k in ha_map.keys():
		if(len(k)>0):
			return False;
	return True

#引数：部屋番号,時刻情報,時刻情報
#SQL文
#s_timeからe_timeの時間の範囲で、
#引数の部屋番号のビーコンタグの情報をデータベースから取得する
def makeSelectLine(room_num,s_time,e_time):
	room_num = getUUID(room_num)
	line =  '''
	select * from sampledb.wiss_challenge_key 
	where key_id="%s" and (date between "%s" and "%s") ''' 
	return line % (room_num,s_time,e_time)

#引数：部屋番号
#返り値：文字列(MACアドレス)
#対象の部屋の鍵に取り付けられたビーコンタグのMACアドレスを取得する
def getUUID(room_num): # ble tag uuid get from database
	connector = pymysql.connect(host="ホスト名/IP", 
		port=ポート番号 , db="データベース", user="ユーザ名", 
		passwd="ユーザのパスワード", charset="文字コード",
		cursorclass=pymysql.cursors.DictCursor)
	cursor = connector.cursor()
	cursor.execute(
		"select uuid from sampledb.room_uuid where room=%d" % int(room_num)
		)
	result = cursor.fetchone();
	#print(result["uuid"])
	return result["uuid"]

#引数：ハッシュマップ
#返り値：なし
#引数のハッシュマップの中のリストをすべて空にする
def hashMapReset(powerDataMap):
	for k in powerDataMap.keys():
		powerDataMap[k] = []

#引数：ハッシュマップ
#返り値：ハッシュマップ
#ハッシュマップの中にある各リストの数値を平均化する
def getAverageMap(power_date_map):
	for k,v in power_date_map.items():
		if len(v)>0:
			power_date_map[k] = sum(v)/len(v)
		else:
			power_date_map[k] = -100
	return power_date_map

#引数：int(HOUR),int(MIN),int(SEC),bool
#返り値：文字列
#現在時刻から引数分の時刻を戻した時刻を特定のフォーマットの文字列にして返す
def makeTimeFormat(back_hour,back_min,back_sec=0,_now=False):
	now_time = datetime.datetime.now()
	back_time = now_time \
		- datetime.timedelta(hours=back_hour) \
		- datetime.timedelta(minutes=back_min) \
		- datetime.timedelta(seconds=back_sec)

	if _now:
		return back_time.strftime('%Y-%m-%d %H:%M:%S')
	return back_time.strftime('%Y-%m-%d %H:%M:00')

#引数：時刻情報,int
#返り値：文字列,文字列
#時間指定の検索をするための２つの時間の文字列のフォーマットを取得する
def makeTimeFormatRange(e_time,range_=1):
	s_time = e_time - datetime.timedelta(minutes=range_)
	return s_time.strftime('%Y-%m-%d %H:%M:%S'),\
			e_time.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
	result = getLocationDate(keyMap["key2"],9,40)
	#print makeTimeFormatRange(10,30,range_=10)



