#!/usr/bin/perl
#
# 蓄々一行掲示板 v2 rev1.9
#
# このファイルは主となるスクリプトです。
# 設定は conf.cgi で行います。
# バージョンアップ時に差し替えが可能です。
#
# 使い方
#   HTMLに記述するタグの文法 
#     <!--#include virtual="パス/bbs.cgi?mode=latest" --> 
#   記述例 
#     <!--#include virtual="./cgi-bin/1linebbs_v2/bbs.cgi?mode=latest" --> 
#   掲示板に直接リンクする場合
#     <a href="http://..../cgi-bin/1linebbs_v2/bbs.cgi?mode=logview">BBS</a>
#   書き込みの管理
#     掲示板下部のadminリンクを開いて下さい。
#
# 蓄積多趣味人（作者のサイト）
# http://www.akiyan.com/
#
# とほほのSSI入門
# http://tohoho.wakusei.ne.jp/wwwssi.htm
#
# ChangeLog
# 2003-12-05 rev1.9 utf8に対応した。
# 2003-05-28 rev1.8 クッキーの使用を選択できるようにし、使用しない場合は完了ページが出なくなるようにした。
# 2003-03-27 rev1.7 完了ページのデフォルトデザインにmeta refreshを追加。設定項目にリフレッシュまでの秒数を追加。
# 2003-03-26 rev1.6 名前をクッキーに保存・参照機能、メッセージ並び順変更機能、書き込み完了ページを追加。
# 2003-03-18 rev1.5 conf.cgiの記述ミスを修正。
# 2003-02-10 rev1.4 管理ログインページの記述ミスを修正。
# 2003-01-08 rev1.3 conf.cgiの管理ページのスタイルシート設定項目を無効にし、管理ページで表がウィンドウからはみ出て表示される問題を修正。
# 2002-12-26 rev1.2.1 管理ページに書き込みフォームを追加、自動リンクのtarget属性設定を追加。
# 2002-12-23 rev1.2 日付が１ヶ月遅れて表示される問題を修正。 
# 2002-12-19 rev1.1 公開。
#
use Jcode;
require 'conf.cgi';

	&get_query_string();
	if ($conf{'use_cookie'}) {
		&get_cookie();
	}
	$conf{'maxlog'}--;
	$admin_style = <<"EOM";
h1,h2 { 
 font-size:100%;
 font-weight:bold;
 margin:0;
}
body {
 font-size:82%;
 padding:1%;
}
thead {
 font-weight:bold;
}
tbody {
 font-weight:normal;
}
td {
 border-width:0 0 1px 0;
 border-style:dotted;
 border-color:#888;
 margin:0;
 word-break:break-all;
}
EOM
	$MODE   = $FORM{'mode'};
	$ACTION = $FORM{'action'};
	$LOG_FILENAME = './log.cgi';
	@LOG_FORMAT = ('status', 'number' ,'name' ,'text' ,'time' , 'host', 'referer');
	$LOG_CUTSTR = '<>';
	if ($MODE eq '') {
		$conf{'charset'} = 'sjis';
		&put(&login());
		exit;
	}
	&loadlog();
	if ($MODE eq 'write') {
		&write();
		if ($conf{'use_cookie'}) {
			print &write_finish();
		} else {
			print "location: $conf{return_url}\n\n";
		}
		exit;
	}
	if ($MODE eq 'logview') {
		$conf{'charset'}   = 'sjis';
		$conf{'viewline'}  = $conf{'viewline_logview'};
		$conf{'vieworder'} = $conf{'vieworder_logview'};
		&put(&latest());
		exit;
	}
	if ($MODE eq 'latest') {
		&put(&latest());
		exit;
	}
	if ($MODE eq 'admin') {
		$conf{'charset'} = 'sjis';
		if ($FORM{'password'} eq $conf{'password'}) {
			&put(&admin());
		} else {
			&put(&login('<p style="color:#a00">パスワードが違います。</p>'));
		}
		exit;
	}
	exit;

###
# ログをハッシュの配列に格納 / ログ保存最大件数チェック尻切
sub loadlog
{
	my ($num, $row, $log_src, $array, $key, $value, $num_active);
	@LOG = ();
	@LOG_ALL = ();
	@log_src = file($LOG_FILENAME);
	if ($#log_src > $conf{'maxlog'}) {
		open(OUT, "+< $LOG_FILENAME");
		eval { flock(OUT, 2);    };
		eval { truncate(OUT, 0); };
		eval { seek(OUT, 0, 0);  };
		for($num = 1; $num <= $#log_src; $num++) {
			print(OUT $log_src[$num]);
		}
		close(OUT);
		@log_src = file($LOG_FILENAME);
	}
	@log_src = reverse(@log_src);
	$num_active = 0;
	for ($num = 0; $num <= $#log_src; $num++) {
		my $data;
		$row = $log_src[$num];
		@array = split(/$LOG_CUTSTR/, $row);
		@data = &format_hash(*LOG_FORMAT, *array);
		($data{'sec'}
		,$data{'min'}
		,$data{'hour'}
		,$data{'mday'}
		,$data{'mon'}
		,$data{'YEAR'}
		,$data{'wday'}
		,$data{'yday'}
		,$data{'isdst'}) = localtime($data{'time'});
		$data{'YEAR'} += ($data{'YEAR'} < 1900) ? 1900 : 0;
		$data{'year'} = substr($data{'YEAR'}, 2);
		$data{'mon'}  = &enforce_figure($data{'mon'} + 1, 2);
		$data{'mday'} = &enforce_figure($data{'mday'}, 2);
		$data{'hour'} = &enforce_figure($data{'hour'}, 2);
		$data{'min'}  = &enforce_figure($data{'min'}, 2);
		$data{'sec'}  = &enforce_figure($data{'sec'}, 2);
		while ( ($key, $value) = each %data) {
			$LOG_ALL[$num]{$key} = $value;
		}
		if ($data{'status'} == 0) {
			while ( ($key, $value) = each %data) {
				$LOG[$num_active]{$key} = $value;
			}
			$num_active++;
		}
	}
}

sub put
{
	my ($html) = @_;
	if ($conf{'charset'} ne "" && $conf{'charset'} ne "sjis") {
		Jcode::convert(\$html, $conf{'charset'});
	}
	print $html;
}

sub latest
{
	my ($num, $hash_grob, $html, $contents, $option, $start, $body, $cookie);
	$hash_grob = '';
	$contents{'navi'}  = '';
	$contents{'message_list'}  = '';
	$html = &content_type('text/html');
	my $view_count = 0;
	$start = ( $FORM{'start'} > 0 ) ? $FORM{'start'} : 0;
	for ($num = $start; $num <= $#LOG; $num++) {
		if ($conf{'autolink'}) {
			$LOG[$num]{'text'} = &auto_link($LOG[$num]{'text'}, $conf{'urlreplace'}, $conf{'target'});
		}
		$hash_grob = $LOG[$num];
		if ($conf{'vieworder'}) {
			$contents{'message_list'} = &replace_hash($hash_grob, $conf{'html_message'}) . $contents{'message_list'};
		} else {
			$contents{'message_list'} .= &replace_hash($hash_grob, $conf{'html_message'});
		}
		$view_count++;
		if ($view_count == $conf{'viewline'}) {
			if ($num < $#LOG && $MODE eq 'logview') {
				$option{'start'}  = $FORM{'start'} + $conf{'viewline_logview'};
				$contents{'navi'} = $conf{'html_navi'};
				$contents{'navi'} = &replace_hash(*conf,   $contents{'navi'});
				$contents{'navi'} = &replace_hash(*option, $contents{'navi'});
			}
			$num = $#LOG;
		}
	}
	$cookie{'cname'} = $COOKIE{'cc1linebbsv2_name'};
	if ($MODE eq 'logview') {
		$body{'body'} = $conf{'html_body'};
		$body{'body'} = &replace_hash(*conf    , $body{'body'});
		$body{'body'} = &replace_hash(*cookie  , $body{'body'});
		$body{'body'} = &replace_hash(*contents, $body{'body'});
		$html .= $conf{'html_logview'};
		$html = &replace_hash(*body,     $html);
		$html = &replace_hash(*conf,     $html);
	} else {
		$html .= $conf{'html_body'};
		$html = &replace_hash(*conf,     $html);
		$html = &replace_hash(*cookie  , $html);
		$html = &replace_hash(*contents, $html);
	}
	return($html);
}

sub write
{
	my (@data, $wdata, $first, $row);
	$wdata = '';
	$first = 1;
	$data{'number'}  = &select_max(*LOG_ALL, 'number') + 1;
	$data{'name'}    = &real_html($FORM{'name'});
	$data{'text'}    = &real_html($FORM{'text'});
	$data{'time'}    = &gettime($conf{'timediff'});
	$data{'status'}  = 0;
	$data{'host'}    = ($ENV{'REMOTE_HOST'} ne '') ? $ENV{'REMOTE_HOST'} : $ENV{'REMOTE_ADDR'};
	$data{'referer'} = $ENV{'HTTP_REFERER'};
	if ($data{'name'} eq "") {
		&error('名前が入力されていません。');
		exit;
	}
	if ($data{'text'} eq "") {
		&error('メッセージが入力されていません。');
		exit;
	}
	if (length($data{'name'} . $data{'text'}) > $conf{'maxlength'}) {
		&error('入力可能な最大の長さは、名前とメッセージで' . $conf{'maxlength'} . 'バイトまでです。');
		exit;
	}
	if ((time() - (stat($LOG_FILENAME))[9]) <= $conf{'stoptime'}) {
		&error($conf{'stoptime'} . '秒以内の連続書き込みは禁止されています。');
		exit;
	}
	foreach $row (@LOG_FORMAT) {
		$wdata .= ($first != 1) ? $LOG_CUTSTR : '';
		$wdata .= $data{$row};
		$first = 0;
	}
	open(OUT, ">> $LOG_FILENAME");
	eval { flock(OUT, 2); };
	print(OUT "$wdata\n");
	close(OUT);
	if ($conf{'use_cookie'}) {
		&set_cookie(key => 'cc1linebbsv2_name', value => $data{name}, expires => 'Thu, 28 Jan 2079 23:59:59 +0900', domain => '', path => '/');
	}
}

sub write_finish
{
	my $html;
	$html = &content_type('text/html');
	$html .= $conf{'html_write_finish'};
	$html = &replace_hash(*conf, $html);
	return $html;
}

sub login
{
	my ($message) = @_;
	my ($html);
	if ($conf{'password'} eq '') {
		$message .= '<p><strong style="color:#a00">【警告】</strong>パスワードが設定されていません。conf.cgiを編集してパスワードを設定してください。（そのままボタンを押せばログインは出来ます）</p>';
	}
	$html = &content_type('text/html');
	$html .= &html_header($conf{'title'}.' 管理ログイン',$admin_style);
	$html .= <<"EOM";
<h1>$conf{'title'} 管理ログイン</h1>
<hr>
<form action="$conf{'cgi'}" method="post" name="login">
$message
<p>Password:<input type="password" size="9" name="password"><input type="hidden" name="mode" value="admin"> <input type="submit" name="submit" value="ログイン"></p>
</form>
<hr>
<p style="text-align:right"><a href="$conf{'cgi'}?mode=logview">logview</a> / Script made by <a href="http://www.akiyan.com/">蓄積多趣味人</a></p>
</body>
</html>
EOM
	return($html);
}

sub admin
{
	my ($html, $contents, $num, $hash_grob, $wdata, $start, $nextstart);
	if (($ACTION eq 'delete' || $ACTION eq 'revival') && $FORM{'number'} ne '') {
		open(OUT, "+< $LOG_FILENAME");
		eval { flock(OUT, 2);    };
		eval { truncate(OUT, 0); };
		eval { seek(OUT, 0, 0);  };
		for ($num = $#LOG_ALL ;$num >= 0; $num--) {
			if($LOG_ALL[$num]{'number'} eq $FORM{'number'}) {
				if ($ACTION eq 'delete') {
					$LOG_ALL[$num]{'status'} = 1;
				} else {
					$LOG_ALL[$num]{'status'} = 0;
				}
			}
			$first = 1;
			$wdata = '';
			foreach $row (@LOG_FORMAT) {
				$wdata .= ($first != 1) ? $LOG_CUTSTR : '';
				$wdata .= $LOG_ALL[$num]{$row};
				$first = 0;
			}
			print(OUT "$wdata");
		}
		close(OUT);
		&loadlog();
	}
	$html = &content_type('text/html');
	$html .= &html_header($conf{'title'}.' 管理', $admin_style);
	$contents{'message_list'} = '';
	my $view_count = 0;
	$start = ( $FORM{'start'} > 0 ) ? $FORM{'start'} : 0;
	for ($num = $start; $num <= $#LOG; $num++) {
		$hash_grob = $LOG[$num];
		$contents{'message_list'} .= &replace_hash($hash_grob, "<tr><td>{number}</td><td>{name}</td><td>{text}</td><td>{YEAR}/{mon}/{mday} {hour}:{min}</td><td>{host}　</td></tr>");
		$view_count++;
		if ($view_count == $conf{'viewline_logview'}) {
			if ($num < $#LOG) {
				$nextstart  = $start + $conf{'viewline_logview'};
				$contents{'navi'} = <<"EOM";
<form action="$conf{'cgi'}" name="next" method="post">
<p><input type="hidden" name="mode" value="admin"><input type="hidden" name="start" value="$nextstart"><input type="hidden" name="password" value="$conf{'password'}"><input type="submit" name="submit" value="next"></p>
</form>
EOM
			}
			$num = $#LOG;
		}
	}
	$html .= <<"EOM";
<h1>$conf{'title'} 管理</h1>
<hr>
<table border="0" style="width:100%">
<thead>
<tr><td style="width:4ex">No.</td><td style="width:16ex">Name</td><td>Message</td><td style="width:18ex">Timestamp</td><td style="width:20ex">Host</td></tr>
</thead>
<tbody>
$contents{'message_list'}
<tbody>
</table>
$contents{'navi'}
<div style="text-align:right;margin-top:1em">
<form action="$conf{'cgi'}" method="post" name="ob" style="display:inline">
Name:<input type="text" name="name" size="8">
 Message:<input type="text" name="text" size="40"><input type="submit" value="write">
<input type="hidden" name="mode" value="write">
</form>
<form action="$conf{'cgi'}" name="delete" method="post" style="display:inline;margin-left:1em">
<input type="hidden" name="mode" value="admin"><input type="hidden" name="action" value="delete"><input type="hidden" name="password" value="$conf{'password'}">Delete No.<input type="text" name="number" size="4"><input type="submit" name="submit" value="delete">
</form>
<form action="$conf{'cgi'}" name="revival" method="post" style="display:inline;margin-left:1em">
<input type="hidden" name="mode" value="admin"><input type="hidden" name="action" value="revival"><input type="hidden" name="password" value="$conf{'password'}">Revival No.<input type="text" name="number" size="4"><input type="submit" name="submit" value="Revival">
</form>
</div>
<hr>
<p style="text-align:right"><a href="$conf{'cgi'}?mode=logview">logview</a> / Script made by <a href="http://www.akiyan.com/">蓄積多趣味人</a></p>
</body>
</html>
EOM
	return($html);
}

sub error
{
	my ($message) = @_;
	my $html;
	$html = &content_type('text/html');
	$html .= &html_header($conf{'title'} . ' エラー', $admin_style);
	$html .= <<"EOM";
<h1>$conf{'title'} エラー</h1>
<hr>
<p style="color:#a00">$message</p>
<p><a href="$conf{'return_url'}">Return</a></p>
<hr>
EOM
	$html .= &html_futter();
	&put($html);
	exit;
}

#____サブルーチン群

###
# クエリー文字列を読み込む
#
# @return void
#
sub get_query_string
{
	my ($conv) = @_;
	my ($a, $name, $value, $query_string);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $query_string, $ENV{'CONTENT_LENGTH'});
	} else {
		$query_string = $ENV{'QUERY_STRING'};
	}
	@a = split(/\&/, $query_string);
	foreach $a (@a) {
		($name, $value) = split(/=/, $a);
		$value =~ tr/+/ /;
		$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		if ( $conv ne "" ) {
			Jcode::convert(\$value,$conv);
		}
		$FORM{$name} = $value;
	}
}

###
# クッキーを読み込む
#
# @return void
#
sub get_cookie {
    my ($row, $name, $value);
    foreach $row (split(/; */, $ENV{'HTTP_COOKIE'})) {
        ($name, $value) = split(/=/, $row);
        $value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;
        $COOKIE{$name} = $value;
    }
}

###
# クッキーをセットする
# @param hash string key     => キー名
#             string value   => 値
#             string expires => 有効期限(RFC2822)
#             string path    => パス
#
sub set_cookie
{
    my %arg = @_;
    $arg{'value'} = &urlencode($arg{'value'});
    print "Set-cookie: $arg{key}=$arg{value}; expires=$arg{expires}; path=$arg{path}\n";
}

###
# content-typeヘッダ
# @param string
#
# @return string
#
sub content_type
{
	if ($_content_type_printed) {
		return("");
	}
	$_content_type_printed = 1;
	return("Content-type: $_[0]\n\n");
}

###
# HTMLヘッダ
#
# @return string
#
sub html_header
{
	my ($title,$style) = @_;
	return <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
$style
</style>
<title>$title</title>
</head>
<body>
EOM
}

###
# HTMLフッタ
#
# @return string
#
sub html_futter
{
	return <<"EOM";
</body>
</html>
EOM
}

###
# {}に囲まれたキーをハッシュで置換
#
# @param *hash 置換するキーと値
# @param string 置換対象
#
# @return string 置換済の対象
#
sub replace_hash
{
	my ($hash, $body, $key, $value);
	(*hash, $body) = @_;
	while ( ($key, $value) = each %hash) {
    	$body =~ s/\{$key\}/$value/g;
	}
	return($body);
}

###
# ファイルを読み込んで配列に格納
# @param string ファイル名
#
# @return array ファイル内容
#
sub file
{
	my ($filename) = @_;
	my ($row, @data);
	if(!open(IN, "< $filename")) {
		print &content_type('text/html');
		print "file does not open '$filename'";
		exit;
	}
	eval { flock(IN, 1); };
	@data = <IN>;
	eval { flock(IN, 8); };
	close(IN);
	return(@data);
}

###
# 引数１をキーとし、引数２を値としてハッシュを返す
# @param *array 名前
# @param *array 値
#
# @return hash
#
sub format_hash
{
	my ($key, $value, $num, @data);
	(*key, *value) = @_;
	for ($num = 0; $num <= $#key; $num++) {
		$data{$key[$num]} = $value[$num];
	}
	return(@data);
}

sub enforce_figure
{
	my ($string, $figure) = @_;
	return(substr('0000000000000000' . $string, 16 + length($string) - $figure, $figure));
}

###
# ハッシュの配列の特定のフィールドから最大値を得る
# @param *hash_array ハッシュの配列
# @param string 選択するフィールド名
#
# @return int 最大値
#
sub select_max
{
	my ($data, $name, $max_num);
	(*data, $name) = @_;
	($num, $max_num) = (0, 0);
	for ($num = 0; $num <= $#data; $num++) {
		$max_num = ($data[$num]{$name} > $max_num) ? $data[$num]{$name} : $max_num;
	}
	return $max_num;
}

###
# 現在の時刻を返す
# @param int 時差
#
# @return int
#
sub gettime
{
	my ($timediff) = @_;
	return(time() + $timediff);
}

###
# 実態参照に置換
# @param string
#
# @return string
#
sub real_html
{
	my ($html) = @_;
	$html =~ s/&/&amp\;/g;
	$html =~ s/"/&quot\;/g;
	$html =~ s/\</&lt\;/g;
	$html =~ s/\>/&gt\;/g;
	return($html);
}

###
# URLエンコード
# @param string
#
# @return string
#
sub urlencode
{
	my ($str) = @_;
	$str =~ s/([^0-9A-Za-z_ ])/'%'.unpack('H2',$1)/ge;
	$str =~ s/\s/+/g;
	return $str;
}

###
# 変数をtext/htmlで出力する
# @param mixed
#
# @return void
#
sub var_dump
{
	my ($var) = @_;
	print &content_type('text/html');
	print $var . "\n";
}

###
# URLの自動リンク
# @param string 自動リンクする文字列
# @param string 置換後の文字列
#
# @return string a hrefが付加された文字列
#
sub auto_link {
	my ($html, $replace_word, $target) = @_;
	if ($target ne '') {
		$target = " target=\"$target\"";
	}
	if ($replace_word ne "") {
		$html =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" title=\"$2\"$target>$replace_word<\/a>/g;
	} else {
		$html =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\"$target>$2<\/a>/g;
	}
	return($html);
}
