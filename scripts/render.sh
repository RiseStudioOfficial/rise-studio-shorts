#!/usr/bin/env bash
set -e
QUOTE="$1"; AUTHOR="$2"; BG="$3"; MUSIC="$4"; OUT="$5"
FONT="assets/fonts/YourFont.ttf"

# Подготовка фона (видео/фото) 20 сек, вертикаль 1080x1920
if [[ "$BG" == *.jpg || "$BG" == *.png ]]; then
  ffmpeg -y -loop 1 -i "$BG" -t 20 -vf "scale=1080:1920,zoompan=z='min(zoom+0.0012,1.08)':d=600" -r 30 -pix_fmt yuv420p temp_bg.mp4
else
  ffmpeg -y -i "$BG" -t 20 -vf "scale=1080:1920:force_original_aspect_ratio=cover,fps=30" -pix_fmt yuv420p temp_bg.mp4
fi

# Наложение затемнения + текста
SAN=$(echo "$QUOTE" | sed "s/[:]/\\:/g; s/[']/\\'/g; s/\"/'/g")
ffmpeg -y -i temp_bg.mp4 -i "$MUSIC" -filter_complex "\
[0:v]format=yuv420p,drawbox=0:0:iw:ih:color=black@0.25:t=fill,\
drawtext=fontfile=$FONT:text='$SAN':fontcolor=white:fontsize=54:line_spacing=12:box=1:boxcolor=black@0.35:boxborderw=20:x=(w-tw)/2:y=(h/2-th/2),\
drawtext=fontfile=$FONT:text='— $AUTHOR':fontcolor=white@0.85:fontsize=36:x=(w-tw)/2:y=h-220\
" -c:v libx264 -preset veryfast -t 20 -c:a aac -shortest "$OUT"

rm -f temp_bg.mp4
