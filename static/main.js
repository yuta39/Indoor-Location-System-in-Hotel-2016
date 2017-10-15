
var img_name = "";

//サーバー側に現在の現在の位置情報のリクエストをかけ、受け取る
function searchRequest(result){
	//result = getResponseText();
	if(result === "no-exist"){
		alert("位置情報が確認できません。担当の者のところまでお持ちください。");
		window.location.href = "/main";
	}else if(result === "password-apo"){
		alert("パスワードに誤りがあります。");
		window.location.href = "/main";
	}else if(result === "no-room"){
		alert("扱っていない部屋番号です。");
		window.location.href = "/main";
	}
	claerCanvas();//画像のクリア
	ss0 = result.split("@");
	setTimeText(ss0[1]);
	ss1 = ss0[0].split(":");
	setBoxInformation(ss1[0]);
	img_name = ss1[1] + ".png"
	changeImageCanvas();//画像の切り替え
	//console.log(result);
}

//出力された画像に位置情報がわかる絵を描く
function drawBoxCanvas(ctx,x,y,w,h){
	// 線を描画
	console.log(x,y,w,h);
	ctx.beginPath();
	ctx.moveTo(x,y);
	ctx.lineTo(x,y+h);
	ctx.lineTo(x+w,y+h);
	ctx.lineTo(x+w,y);
	ctx.lineTo(x,y)
	ctx.stroke();
}

//マップ画面に画像を出力する
function changeImageCanvas(){
	var cnvs = document.getElementById('canvas_id');
	var ctx = cnvs.getContext('2d');
	ctx.lineWidth="4";

	var img = new Image();
	img.onload = function() {
		if(device_flag == 1){
			ctx.drawImage(img, 0, 0,cnvs.width,cnvs.height);
			toDevicePoint(img.width,img.height);
		}else{
			ctx.drawImage(img, 0, 0);
		}
		drawBoxCanvas(ctx,x,y,w,h);
		//drawBoxCanvas(ctx,155,450,190,80);
  	};

  	img.src = "/static/img/"+img_name;
}

//画像を消す
function claerCanvas(){
	var cnvs = document.getElementById('canvas_id');
	var ctx = cnvs.getContext('2d');
	ctx.clearRect(0,0,1000,1000);
}


