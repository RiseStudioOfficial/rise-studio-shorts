#!/usr/bin/env bash
set -e
QUOTE="$1"; AUTHOR="$2"; BG="$3"; OUT="$4"
FONT="assets/fonts/YourFont.ttf"

# 1) Берём кадр из видео или подготавливаем фото под вертикаль
if [[ "$BG" == *.jpg || "$BG" == *.png ]]; then
  ffmpeg -y -i "$BG" -vf "scale=1080:1920:force_original_aspect_ratio=cover" -frames:v 1 __bg.jpg
else
  # берём кадр на 1.5 секунде
  ffmpeg -y -ss 1.5 -i "$BG" -vf "scale=1080:1920:force_original_aspect_ratio=cover" -frames:v 1 __bg.jpg
fi

# 2) Накладываем затемнение и текст
SAN=$(echo "$QUOTE" | sed "s/[:]/\\:/g; s/[']/\\'/g; s/\"/'/g")
ffmpeg -y -i __bg.jpg -vf "\
format=yuv420p,drawbox=0:0:iw:ih:color=black@0.25:t=fill,\
drawtext=fontfile=$FONT:text='$SAN':fontcolor=white:fontsize=70:line_spacing=14:box=1:boxcolor=black@0.35:boxborderw=24:x=(w-tw)/2:y=(h/2-th/2),\
drawtext=fontfile=$FONT:text='— $AUTHOR':fontcolor=white@0.85:fontsize=44:x=(w-tw)/2:y=h-220\
" -q:v 3 "$OUT"

rm -f __bg.jpg
