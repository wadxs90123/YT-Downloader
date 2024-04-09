## 使用教學

先clone repo到自己的電腦
``` console
git clone https://github.com/wadxs90123/YT-Downloader.git
```

再進入資料夾，並下載需要的套件
``` console
pip install -r requirements.txt
```

最後就是開啟Web Server以及API Server
#### Web Server:
``` console
python ./backend/web-server/web.py 
```
#### API Server:
``` console
uvicorn backend.api-server.api:app --reload
```

然後你就能透過瀏覽器瀏覽
http://127.0.0.1:5000

如果你有需要的話，API網址是
http://127.0.0.1:8000
