var x=0,y=0,w=0,h=0; //矩形波の座標、形状用の変数
var canvas_w=0,canvas_h=0; //canvasの大きさ用の変数
var device_flag = 0; //スマホかPCのブラウザかを判定するための変数

//canvasの初期化
function initCanvas(){
	var cnvs = document.getElementById('canvas_id');
	cnvs.width = window.innerWidth * 0.95;
	cnvs.height = window.innerHeight * 0.85;
	canvas_w = cnvs.width;
	canvas_h = cnvs.height;
}

//矩形波の形状の情報をセットする
function setBoxInformation(result){
	ss = result.split(",");
	x = parseInt(ss[0]);
	y = parseInt(ss[1]);
	w = parseInt(ss[2]);
	h = parseInt(ss[3]);
}

//矩形波の形状の情報をブラウザの大きさに合わせて変換する
function toDevicePoint(i_w,i_h){
	x = x * (canvas_w/i_w);
	y = y * (canvas_h/i_h);
	w = w * (canvas_w/i_w);
	h = h * (canvas_h/i_h);
}

//カギ番号(ビーコンタングの識別情報)のテキストボックに値セット
function setKeyNumberTextbox(value){
	element = document.getElementsByName("key-number")[0];
	element.value=value;
}

//パスワードのテキストボックスに値をセット
function setKeyPasswordTextbox(value){
	element = document.getElementById("password-box");
	element.innerHTML = '<input type="password" name="key-password" 
				maxlength="30" class="hoge">'
	document.getElementsByName("key-password")[0].focus();
}

//パスワードのテキストボックスに値をセット(スマホブラウザ用)
function setKeyPasswordTextboxMobile(value){
	mobile_html = '<div class="ui-input-text 
				ui-body-inherit ui-corner-all ui-shadow-inset"><input 
				type="password" name="key-password" maxlength="30" 
				class="hoge"></div>'
	element = document.getElementById("password-box");
	element.innerHTML = mobile_html;
	document.getElementsByName("key-password")[0].focus();
}

//時刻情報をブラウザ出力用の変数セットする
function setTimeText(time_){
	element = document.getElementById("timetext");
	element.innerHTML = time_;
}

//部屋番号をブラウザ出力用のセットする
function setRoomText(room_){
	element = document.getElementById("roomtext");
	element.innerHTML = room_;
}



