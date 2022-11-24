# ベースイメージの選択
FROM mysql:latest
# sqlファイルをエントリーポイントにコピー
COPY ./init.sql /docker-entrypoint-initdb.d/
# 設定ファイルのコピー
COPY my.cnf /etc/mysql/conf.d/my.cnf