import requests
import json
json_str = '{"imageElements": [{"pageId": 1, "yCoord": "90px", "height": "279px", "width": "501px", "xCoord": "26px", "id": 1, "imgUrl": "dummy_image.png"}], "gplusId": "115899113282816200821", "id": 1, "textElements": [{"pageId": 1, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 1}, {"pageId": 1, "yCoord": "390px", "height": "150px", "content": "CONTENT CHANGED YAAAY", "width": "500px", "xCoord": "26px", "id": 2}], "title": "Page Title"}'
payload = json.loads(json_str)
r = requests.delete("http://localhost:5000/api/pages/6?apiToken=22af509b2ae9aa32fcf41e60cc935d2a0e881d597d971860823abbf3dbf52b7b")
print r
try:
  print r.json()
except Exception as e:
  print e
