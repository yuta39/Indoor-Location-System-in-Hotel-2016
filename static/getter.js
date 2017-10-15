
//ブラウザに入力されている部屋番号を取得
function getKeyNumber(){
	var value = $('[name=key-number]').val();
	return value;
}

//ブラウザに入力されているパスワードを取得
function getKeyPassword(){
	var value = $('[name=key-password]').val();
	return value;
}

//ブラウザに埋め込まれている部屋番号を取得
function getResponseText(){
	element = document.getElementById("response_txt");
	return element.innerHTML;
}

