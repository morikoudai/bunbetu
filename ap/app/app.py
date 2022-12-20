from flask import Flask,render_template,redirect,url_for,request
from db import db_manager

app=Flask(__name__)

#利用者
#ログイン画面
@app.route("/")
def index():
    e=request.args.get("e")
    return render_template("u_login.html",e=e)

#ログイン処理
@app.route("/",methods=["POST"])
def login():
    u_id=request.form.get("u_id")
    pw=request.form.get("pw")

    try:
        dbmg=db_manager.db_manager()
        sql="select * from User where u_id=%s"
        user=dbmg.exec_query(sql,u_id)
        hash_pw, salt =dbmg.calc_pw_hash(pw, user[0]["salt"])
    except:
        return redirect(url_for('index',e=1))
    
    print("hash_pw" + hash_pw)
    print("db_pw" + user[0]["hash_pw"])

    
    if hash_pw == user[0]["hash_pw"]: # パスワード比較
            # ログイン成功
        return redirect(url_for('top_page'))
    else:
            # ログイン失敗
        return redirect(url_for('index', e=1))

@app.route("/top")
def top_page():
    return render_template("topmenu.html")

# サインアップ画面
@app.route("/entry")
def entry_page():
    e=request.args.get("e") # エラーの受け取り
    return render_template("u_entry.html",e=e)
# サインアップ処理
@app.route("/entry",methods=["POST"])
def entry():
    # フォーム受け取り
    u_id=request.form.get("u_id")
    pw=request.form.get("pw")
    # サインアップ処理
    try:
        dbmg=db_manager.db_manager()
        hash_pw, salt = dbmg.calc_pw_hash(pw)
        sql="insert into User (u_id,hash_pw,salt) value (%s,%s,%s)"
        dbmg.exec_query(sql,(u_id,hash_pw,salt))
    except :
        return redirect(url_for("entry_page", e=2))
    
    return redirect(url_for("entry_page", e=8))

# 検索・表示画面
@app.route("/u_search")
def search_page():
    return render_template("u_search.html")
@app.route("/u_search",methods=["POST"])
def search():
    Garbageid=request.form.get("Garbageid")
    GarbageName=request.form.get("GarbageName")
    Separation=request.form.get("Separation")
    Category=request.form.get("Category")
    initials=request.form.get("initials")
    dbmg=db_manager.db_manager()
    sql=('select GarbageName,Separation,Category from Garbagelist where Garbageid=%s')
    search=dbmg.exec_query(sql,(Garbageid,GarbageName,Separation,Category,initials))
    return render_template("u_search.html",search=search)

# ゴミ一覧
@app.route("/u_tr_list")
def u_tr_list():

    dbmg=db_manager.db_manager()
    sql="select * from Garbagelist"
    u_tr_list=dbmg.exec_query(sql)
    return render_template("u_tr_list.html",u_tr_list=u_tr_list)

# お気に入り登録画面
@app.route("/u_favorite")
def favorite():
    return render_template("u_favorite.html")

# リサイクル回収場所マップ画面
@app.route("/u_re_map")
def map():
    return render_template("u_re_map.html")

# 収集日カレンダー画面

@app.route('/u_co_carender')
def calender():
    return render_template('u_co_carender.html')

#　リサイクル製品紹介画面
@app.route("/u_recycle")
def recycle():

    dbmg=db_manager.db_manager()
    sql="select * from Recycle"
    recycle=dbmg.exec_query(sql)
    return render_template("u_recycle.html",recycle=recycle)

# クイズ画面
@app.route("/u_quize")
def quize():
    return render_template("u_quize.html")




#管理者
#ログイン画面
@app.route("/manager")
def m_index():
    e=request.args.get("e")
    return render_template("m_login.html",e=e)

#ログイン処理
@app.route("/manager",methods=["POST"])
def m_login():
    m_id=request.form.get("m_id")
    pw=request.form.get("pw")

    try:
        dbmg=db_manager.db_manager()
        sql="select * from Manager where m_id=%s"
        manager=dbmg.exec_query(sql,m_id)
        hash_pw, salt =dbmg.calc_pw_hash(pw, manager[0]["salt"])
    except:
        return redirect(url_for('m_index',e=3))
    
    print("hash_pw" + hash_pw)
    print("db_pw" + manager[0]["hash_pw"])

    
    if hash_pw == manager[0]["hash_pw"]: # パスワード比較
            # ログイン成功
        return redirect(url_for('m_trash_list'))
    else:
            # ログイン失敗
        return redirect(url_for('m_index', e=3))

# 登録ごみ情報一覧
@app.route("/m_trash_list")
def m_trash_list():
    dbmg=db_manager.db_manager()
    sql="select * from Garbagelist"
    trash_list=dbmg.exec_query(sql)
    return render_template("m_trash_list.html",trash_list=trash_list)

# ごみ情報登録
@app.route("/m_trash_entry")
def m_trash_entry():
    e=request.args.get("e")
    return render_template("m_trash_entry.html",e=e)
@app.route("/m_trash_entry",methods=["POST"])
def trash_entry():
    
    try:
        GarbageID=request.form.get("GarbageID")
        GarbageName=request.form.get("GarbageName")
        Separation=request.form.get("Separation")
        Category=request.form.get("Category")
        dbmg=db_manager.db_manager()
        sql="insert into Garbagelist(GarbageID,GarbageName,Separation,Category) value (%s,%s,%s,%s)"
        dbmg.exec_query(sql,(GarbageID,GarbageName,Separation,Category))
    except:
        return redirect(url_for("m_trash_entry", e=5))

    return redirect("/m_trash_list")

# ごみ情報削除
@app.route("/m_trash_delete")
def m_trash_delete():
    e=request.args.get("e")
    return render_template("m_trash_delete.html",e=e)
@app.route("/m_trash_delete",methods=["POST"])
def delete_page():
    try:
        GarbageID=request.form.get("GarbageID")
        dbmg = db_manager.db_manager()
        sql = "delete from Garbagelist where GarbageID=%s"
        dbmg.exec_query(sql,GarbageID)
    except:
        return redirect(url_for("m_trash_delete", e=6))

    return redirect(url_for("m_trash_list"))



# ごみ情報修正
@app.route("/m_trash_modify")
def m_trash_modify():
    e=request.args.get("e")
    return render_template("m_trash_modify.html",e=e)
@app.route("/m_trash_modify",methods=["POST"])
def modify_page():
    GarbageID=request.form.get("GarbageID")
    GarbageName=request.form.get("GarbageName")
    Separation=request.form.get("Separation")
    Category=request.form.get("Category")

    #try:
    dbmg = db_manager.db_manager()
    sql = "update Garbagelist set GarbageName=%s,Separation=%s,Category=%s where GarbageID=%s"
    dbmg.exec_query(sql,(GarbageID,GarbageName,Separation,Category))
    sql = ("select * from Garbagelist where GarbageID=%s")
    m_t_modify=dbmg.exec_query(sql,(GarbageID))
    #except:
           #return redirect(url_for("m_trash_modify", e=7))

    return render_template("m_trash_modify.html",m_t_modify=m_t_modify,GarbageID=GarbageID,GarbageName=GarbageName,
        Separation=Separation,Category=Category)
















# サインアップ画面
@app.route("/m_entry")
def m_entry_page():
    e=request.args.get("e") # エラーの受け取り
    return render_template("m_entry.html",e=e)
# サインアップ処理
@app.route("/m_entry",methods=["POST"])
def m_entry():
    # フォーム受け取り
    m_id=request.form.get("m_id")
    pw=request.form.get("pw")
    # サインアップ処理
    try:
        dbmg=db_manager.db_manager()
        hash_pw, salt = dbmg.calc_pw_hash(pw)
        sql="insert into Manager(m_id,hash_pw,salt) value (%s,%s,%s)"
        dbmg.exec_query(sql,(m_id,hash_pw,salt))
    except :
        return redirect(url_for("m_entry_page", e=4))
    
    return redirect(url_for("m_index"))

if __name__=="__main__":
    # 外部IP空のアクセスを許可 8080ポートで起動
    app.run(host="0.0.0.0", port=8080)