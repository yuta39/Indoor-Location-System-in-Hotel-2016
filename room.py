from werkzeug.security 
	import generate_password_hash, check_password_hash
import pymysql.cursors

#新たな部屋番号とパスワードを記録・管理するためのクラス
class Room(object):
	#引数：部屋番号
	#入力された部屋番号とハッシュ化されたパスワードを
	#データベースに記録する
	def __init__(self,room_num,password):
		self.room_num = room_num
		self.set_password(password)

	#引数：パスワード
	#部屋番号とパスワードをハッシュ化しデータベースに記録する
	def set_password(self,password):
		self.pw_hash = generate_password_hash(password)
		self.insert_database()

	#データベースに接続し部屋番号とハッシュ化されたパスワードを記録する
	def insert_database(self):
		connector = pymysql.connect(
			host="ホスト名/IP", 
			port=ポート番号 , db="データベース", user="ユーザ名", 
			passwd="ユーザのパスワード", charset="文字コード",
			cursorclass=pymysql.cursors.DictCursor)
		cursor = connector.cursor()
		sql_line = 'insert into sampledb.room_pass 
					values(%d,"%s");' % (int(self.room_num),self.pw_hash)
		cursor.execute(sql_line)
		connector.commit()
		connector.close()

#引数：部屋番号,パスワード
#返り値：bool
#部屋番号とパスワードが一致するかを判定する
def check_password(room_num,password):
	connector = pymysql.connect(
			host="ホスト名/IP", 
			port=ポート番号 , db="データベース", user="ユーザ名", 
			passwd="ユーザのパスワード", charset="文字コード",
			cursorclass=pymysql.cursors.DictCursor)
	cursor = connector.cursor()
	sql_line = 'select password from 
			sampledb.room_pass where room=%s;' % room_num
	cursor.execute(sql_line)
	result = cursor.fetchone();
	if(result == None):
		return False
	#print(result)
	return check_password_hash(result['password'],password)

if __name__=="__main__":
	Room(999,"aaaaa")
