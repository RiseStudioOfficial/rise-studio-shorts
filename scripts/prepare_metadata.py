#!/usr/bin/env python3
import sys, os, datetime, random

LINK = os.getenv("LINK_HUB_URL","")
quote = sys.argv[1]; author = sys.argv[2]; tags = sys.argv[3] if len(sys.argv)>3 else ""
title = (quote[:60] + "…") if len(quote)>60 else quote
title += " | Мотивация на день"
desc = f"{quote}\n— {author}\n\nПодборка книг и инструментов 👉 {LINK}\n#мотивация #цитаты #саморазвитие #shorts"
keywords = ["мотивация","цитаты","успех","привычки"] + [t.strip() for t in tags.split(",") if t.strip()]
print(title); print("-----"); print(desc); print("-----"); print(",".join(keywords))
