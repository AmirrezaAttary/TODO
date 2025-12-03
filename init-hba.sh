#!/bin/sh
# بعد از ساخت دیتابیس، فایل pg_hba.conf اولیه ایجاد می‌شود
# سپس ما فایل خودمان را جایگزین می‌کنیم

echo "Applying custom pg_hba.conf..."
cp /docker-entrypoint-initdb.d/pg_hba.conf /var/lib/postgresql/data/pg_hba.conf
chmod 600 /var/lib/postgresql/data/pg_hba.conf
