//スマホブラウザ専用の関数

//入力画面からマップ画面に遷移させる
function moveMapPage(){
	window.location.href = '#map'; // 繊維
	initCanvas();
}

//ページ遷移、位置情報取得、マップ表示を行う関数
function searchRequestMobile(){
	moveMapPage()
	device_flag = 1;
	searchKeyPosison();
}

//必要な入力情報をブラウザから取得し
//サーバーに位置情報のリクエストをかけ
//取得した位置情報をもとにマップ画面を出力する
function searchKeyPosison(){
	//get select box date
	var key_value_now = getKeyNumber();
	var pass_value_now = getKeyPassword();
	setRoomText(key_value_now);
	var data = new Object();
	data["key_id"] = key_value_now;
	data["password"] = pass_value_now
	$.ajax({
	  type : "GET",
	  url : "/_foo",
	  data: data,
	  contentType: 'application/json;charset=UTF-8',
	  success: function(result) {
	  	searchRequest(result)
	  }
	});

}