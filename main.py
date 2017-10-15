from flask import Flask, render_template
from flask import request, redirect, url_for,request
import room as room
import nearsender_sql as ns

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)


#各エリアに矩形波を描くための座標とサイズの情報
point_to_map1F = {
			"area1":"207,302,90,60",
			"area2":"250,430,80,110",
			"area3":"420,320,50,50",
			"area4":"700,350,220,120"
			}
point_to_map2F = {
			"area6":"178,312,160,80",
			"area7":"177,210,150,100",
			"area8":"177,122,160,200",
			"area9":"386,235,80,60",
            "area10":"772,202,120,200",
            "area12":"160,430,170,100",
            "area13":"329,445,150,80"}
point_to_map8F = {"area11":"0,0,0,0"}
point_to_map5F = {"area5":"0,0,0,0"}

#引数：リクエストしてきた端末の情報
#返り値：端末のデバイス名
#リクエストしてきたユーザの端末の種類(iPhoneやChrome、Safariなど)を返す
def getDevice(user_agent):
    start_index = user_agent.find('(')
    end_index = user_agent.find(';')
    device = user_agent[start_index+1:end_index]
    return device

#引数：エリアの文字列
#返り値：描画情報と階情報の文字列
#引数のエリアをブラウザに描画するための
#矩形波の描画情報と階情報を、連結して文字列で返す
def getlocationPoint(area):
	if area in point_to_map1F:
		return point_to_map1F[area] + ":1F"
	elif area in point_to_map2F:
		return point_to_map2F[area] + ":2F"
	elif area in point_to_map5F:
		return point_to_map5F[area] + ":5F"
	elif area in point_to_map8F:
		return point_to_map8F[area] + ":8F"
	else:
		return None


#引数：リクエストした端末の情報
#返り値：モバイル端末であれTrue それ以外ならFalse
#リクエストしてきたユーザの端末がモバイル端末かどうかを判定する
def is_mobile(user_agent):
    if user_agent is None:
        return False

    device = getDevice(user_agent)

    #iPhone,iPod,iPad,Androidであればmobileデバイスだと解釈する
    if device=='iPhone' or device=='iPod' or device=='iPad' or device=='Android':
        return True
    else:
        return False

#引数：部屋番号
#返り値：時刻情報
#対象のビーコンタグが観測された最後の時間を取得する
def get_new_key_date(room_num):
	sql_line = 'select date from sampledb.wiss_challenge_key where key_id="%s" order by date desc limit 1;' % ns.getUUID(room_num)
	return ns.getNewKeyDate(sql_line)

#引数：部屋番号
#返り値：SQL文,時刻情報
#情報を取得するためのSQL文と最後にビーコンタグが最後に観測された時刻を取得する
def makeSQLline(room_num):
	e_time = get_new_key_date(room_num)
	s_time,e_time = ns.makeTimeFormatRange(e_time,1)
	return ns.makeSelectLine(room_num,s_time,e_time),e_time

#引数：部屋番号
#返り値：文字列,時刻情報
#SQL文を元にビーコンタグの現在の位置情報を取得し
#その位置情報とビーコンタグが最後に観測された時刻を取得する
def request_about_key(room_num):
	sql_line,_time = makeSQLline(room_num)
	area = getlocationPoint(ns.getLocationDate(sql_line))
	return area,_time

#引数：部屋番号
#返り値：文字列
#連結された文字列を取得する
def where_and_when(room_num):
	now_key_val = room_num
	now_min_val="0"
	now_hour_val="0"
	try:
		area,e_time = request_about_key(now_key_val)
	except TypeError as e:
		return "no-exist"
	else:
		return area + '@' + e_time[:-3] 
	finally:
		pass
	
#引数：部屋番号
#返り値：bool
#入力された部屋番号がデータベースに登録されているかを判定する
def is_admin_room_number(room_num):
	try:
		ns.getUUID(room_num)
	except TypeError as e:
		return False
	else:
		return True
	finally:
		pass




#情報入力画面の出力する
@app.route('/main')
def main():
    title = '情報を送ります'
    if is_mobile(request.user_agent.string):
        return render_template('top_sp.html',title=title)
    else:
        return render_template('top.html',title=title)
       
#GET通信で受け取った情報を元に
#ブラウザ描画するための情報を返す
@app.route('/_foo',methods=['GET','POST'])
def foo():
    if request.method == 'GET':
        now_key_val = request.args.get("key_id")
        now_pass_val = request.args.get("password")
        if not is_admin_room_number(now_key_val):
        	return "no-room"
        if room.check_password(int(now_key_val),now_pass_val):
        	response_msg = where_and_when(now_key_val)
        	print(response_msg)
        	return response_msg
        else:
        	return "password-apo"

    return "no-exist"

#マップ画面を出力する
@app.route('/map',methods=['GET','POST'])
def map():
	title = 'マップを出力します'
	if is_mobile(request.user_agent.string):
		return render_template("top_sp.html",title=title,room_num=room_num)
	else:
	    room_num = request.form["key-number"]
	    password = request.form["key-password"]

	    if not is_admin_room_number(room_num):
	    	return render_template('top.html',
	    		title=title,error_msg="扱っていない部屋番号です")

	    if room.check_password(int(room_num),password):
	    	response_msg = where_and_when(room_num)
	    	print(response_msg)
	    	return render_template('map.html',
	    		title=title,room_num=room_num,response_msg=response_msg)
	    else:
	    	return render_template('top.html',
	    		title=title,error_msg="パスワードが違います")



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')