# �~�X��s�f���� v2 �ݒ�t�@�C�� rev1.9
# ���̃t�@�C���̕����R�[�h��shift_jis�ŕۑ����ĉ������B
#
#____�ݒ肱������

# �Ǘ��p�X���[�h�i�K���ݒ肵�ĉ������j
$conf{'password'} = '';

# �f���̃^�C�g���ilogview�Aadmin�Ŏg�p����܂��j
$conf{'title'} = '�~�X��s�f���� v2';

# �o�͂��镶���R�[�h ( sjis , euc , jis , utf8 )
# ���ߍ��ݐ��HTML�̕����R�[�h�Ɠ����ɂ��Ă�������
$conf{'charset'} = 'sjis'; 

# �ݒu����URL ( http����S�ċL�q���Ă������� )
$conf{'return_url'} = 'http://';

# bbs.cgi��URL
$conf{'cgi'} = 'http://***/cgi-bin/1linebbs/bbs.cgi';

# ���ߍ��ݎ��̕\������
$conf{'viewline'} = 8;

# logview���̕\������
$conf{'viewline_logview'} = 30;

# ���ߍ��ݎ��̃��b�Z�[�W���я�
# 0 ... �V������
# 1 ... �Â���
$conf{'vieworder'} = 0;

# logview���̃��b�Z�[�W���я�
# 0 ... �V������
# 1 ... �Â���
$conf{'vieworder_logview'} = 0;

# cookie�̎g�p�i�g�p����Ɗ����y�[�W���o��悤�ɂȂ�܂��j
# 0 ... �g�p���Ȃ�
# 1 ... �g�p����
$conf{'use_cookie'} = 0;

# �����y�[�W���玩���Ŗ߂�܂ł̎��� (�b)
$conf{'refresh_time'} = 5;

# ���������N������ ( 1 = on )
$conf{'autolink'} = 1;

# ���������N���ɒu�����閼�O�i��̏ꍇ��URL�����̂܂܃����N����܂��j
$conf{'urlreplace'} = '';

# ���������N����target�����̒l�i�󔒈ȊO�̏ꍇ��target�������}������܂��j
# ��F_blank  ... �V�K�E�B���h�E
#     _top    ... �e�t���[��
$conf{'target'} = '';

# �������߂閼�O�{���͂̍ő咷�i�P�ʁFbyte�j
$conf{'maxlength'} = 512;

# �A���������ݒ�~���ԁi�P�ʁF�b�j
$conf{'stoptime'} = 10;

# ���O�̍ő�ۑ������i�����قǃT�[�o�[�ɕ��ׂ�������܂��j
$conf{'maxlog'} = 300;

# �T�[�o�[�Ƃ̎����i�P�ʁF�b�j
$conf{'timediff'} = 0;

# �S�̂̃f�U�C��
# {cgi}          ... cgi��URL
# {message_list} ... �������݈ꗗ
# {navi}         ... logview�ł̃i�r�Q�[�V�����\��
# {cname}        ... cookie����ǂݏo�������O
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
 / Script made by <a href="http://www.akiyan.com">�~�ϑ���l</a>
</p>
</div>
EOM

# �������݂P�s�̃f�U�C��
# {name}   ... ���O
# {text}   ... ����
# {YEAR}   ... 4���N
# {year}   ... 2���N
# {mon}    ... ��
# {mday}   ... ��
# {hour}   ... ��
# {min}    ... ��
# {sec}    ... �b
# {number} ... �������ݔԍ�
$conf{'html_message'} = <<"EOM";
<p style="margin:0">
[<span style="font-weight:bold">{name}</span>] {YEAR}/{mon}/{mday} {hour}:{min} No.{number}<br>
{text}
</p>
<hr style="height:1px;color:#aaa;border-style:dotted">
EOM

# logview�̑S�̂̃f�U�C���icharset�͕K��shift_jis�j
# {title}      ... �^�C�g��
# {body}       ... �������݈ꗗ
# {return_url} ... ���ߍ��ރy�[�W��URL
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

# logview�ł̃i�r�Q�[�V�����̃f�U�C��
$conf{'html_navi'} = <<"EOM";
<p style="margin:0"><a href="{cgi}?mode=logview&start={start}">Next Page</a></p>
EOM

# �������݊����y�[�W�̃f�U�C��
# {title}        ... �^�C�g��
# {return_url}   ... ���ߍ��ރy�[�W��URL
# {refresh_time} ... �����y�[�W���玩���Ŗ߂�܂ł̎���
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
<h1>{title} �������݊���</h1>
<hr>
<p style="text-align:center;line-height:3em"><span style="font-weight:bold">{title} �ւ̏������݂��������܂����B</span><br>{refresh_time}�b��Ɏ����Ō��̃y�[�W�֖߂�܂��B<br>�i���ɂ���Ă͎����Ő؂�ւ��܂���j</p>
<p style="text-align:center"><a href="{return_url}">�߂�</a></p>
<hr>
<p style="text-align:right"><a href="{cgi}?mode=logview">logview</a> / Script made by <a href="http://www.akiyan.com/">�~�ϑ���l</a></p>
</body>
</html>
EOM

#____�ݒ肱���܂�
1;