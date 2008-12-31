# 蓄々一行掲示板 v2 設定ファイル rev1.9
# このファイルの文字コードはshift_jisで保存して下さい。
#
#____設定ここから

# 管理パスワード（必ず設定して下さい）
$conf{'password'} = '';

# 掲示板のタイトル（logview、adminで使用されます）
$conf{'title'} = '蓄々一行掲示板 v2';

# 出力する文字コード ( sjis , euc , jis , utf8 )
# 埋め込み先のHTMLの文字コードと同じにしてください
$conf{'charset'} = 'sjis'; 

# 設置するURL ( httpから全て記述してください )
$conf{'return_url'} = 'http://';

# bbs.cgiのURL
$conf{'cgi'} = 'http://***/cgi-bin/1linebbs/bbs.cgi';

# 埋め込み時の表示件数
$conf{'viewline'} = 8;

# logview時の表示件数
$conf{'viewline_logview'} = 30;

# 埋め込み時のメッセージ並び順
# 0 ... 新しい順
# 1 ... 古い順
$conf{'vieworder'} = 0;

# logview時のメッセージ並び順
# 0 ... 新しい順
# 1 ... 古い順
$conf{'vieworder_logview'} = 0;

# cookieの使用（使用すると完了ページが出るようになります）
# 0 ... 使用しない
# 1 ... 使用する
$conf{'use_cookie'} = 0;

# 完了ページから自動で戻るまでの時間 (秒)
$conf{'refresh_time'} = 5;

# 自動リンクをする ( 1 = on )
$conf{'autolink'} = 1;

# 自動リンク時に置換する名前（空の場合はURLがそのままリンクされます）
$conf{'urlreplace'} = '';

# 自動リンク時のtarget属性の値（空白以外の場合にtarget属性が挿入されます）
# 例：_blank  ... 新規ウィンドウ
#     _top    ... 親フレーム
$conf{'target'} = '';

# 書き込める名前＋文章の最大長（単位：byte）
$conf{'maxlength'} = 512;

# 連続書き込み停止時間（単位：秒）
$conf{'stoptime'} = 10;

# ログの最大保存件数（多いほどサーバーに負荷がかかります）
$conf{'maxlog'} = 300;

# サーバーとの時差（単位：秒）
$conf{'timediff'} = 0;

# 全体のデザイン
# {cgi}          ... cgiのURL
# {message_list} ... 書き込み一覧
# {navi}         ... logviewでのナビゲーション表示
# {cname}        ... cookieから読み出した名前
$conf{'html_body'} = <<"EOM";
<div style="font-size:82%;background-color:#fff;border:1px solid #666;padding:1ex">
<form action="{cgi}" method="post" name="ob" style="margin:0">
<p style="margin:0">
Name:<input type="text" name="name" size="8" value="{cname}" style="border:1px solid #888">
 Message:<input type="text" name="text" size="40" value="" style="border:1px solid #888">
 <input type="submit" value="write" style="color:#000;background-color:#ccc;border:1px outset #888">
<input type="hidden" name="mode" value="write">
</p>
</form>
<hr style="height:1px;color:#aaa;border-style:dotted">
{message_list}
{navi}
<p style="margin:0;text-align:right">
<a href="{cgi}?mode=logview">logview</a>
 / <a href="{cgi}">admin</a>
 / Script made by <a href="http://www.akiyan.com">蓄積多趣味人</a>
</p>
</div>
EOM

# 書き込み１行のデザイン
# {name}   ... 名前
# {text}   ... 文章
# {YEAR}   ... 4桁年
# {year}   ... 2桁年
# {mon}    ... 月
# {mday}   ... 日
# {hour}   ... 時
# {min}    ... 分
# {sec}    ... 秒
# {number} ... 書き込み番号
$conf{'html_message'} = <<"EOM";
<p style="margin:0">
[<span style="font-weight:bold">{name}</span>] {YEAR}/{mon}/{mday} {hour}:{min} No.{number}<br>
{text}
</p>
<hr style="height:1px;color:#aaa;border-style:dotted">
EOM

# logviewの全体のデザイン（charsetは必ずshift_jis）
# {title}      ... タイトル
# {body}       ... 書き込み一覧
# {return_url} ... 埋め込むページのURL
$conf{'html_logview'} = <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Trasitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<title>{title}</title>
</head>
<body>
<h1 style="font-size:100%;margin-bottom:1ex;text-align:center">{title}</h1>
{body}
<p style="font-size:82%"><a href="{return_url}">Return</a></p>
</body>
</html>
EOM

# logviewでのナビゲーションのデザイン
$conf{'html_navi'} = <<"EOM";
<p style="margin:0"><a href="{cgi}?mode=logview&start={start}">Next Page</a></p>
EOM

# 書き込み完了ページのデザイン
# {title}        ... タイトル
# {return_url}   ... 埋め込むページのURL
# {refresh_time} ... 完了ページから自動で戻るまでの時間
$conf{'html_write_finish'} = <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Trasitional//EN">
<html lang="ja">
<head>
<meta http-equiv="refresh" content="{refresh_time};url={return_url}"> 
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
h1 { 
 font-size:100%;
 font-weight:bold;
 margin:0;
}
body {
 padding:1%;
}
</style>
<title>{title}</title>
</head>
<body>
<h1>{title} 書き込み完了</h1>
<hr>
<p style="text-align:center;line-height:3em"><span style="font-weight:bold">{title} への書き込みが完了しました。</span><br>{refresh_time}秒後に自動で元のページへ戻ります。<br>（環境によっては自動で切り替わりません）</p>
<p style="text-align:center"><a href="{return_url}">戻る</a></p>
<hr>
<p style="text-align:right"><a href="{cgi}?mode=logview">logview</a> / Script made by <a href="http://www.akiyan.com/">蓄積多趣味人</a></p>
</body>
</html>
EOM

#____設定ここまで
1;