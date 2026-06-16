# -*- coding: utf-8 -*-
import build_photos_v15_catalog as b
for i,im in enumerate(b.pages):
    im.save(f'_chk_pg{i}.png')
print('dumped', len(b.pages))
