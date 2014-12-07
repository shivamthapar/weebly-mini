====
Mini Weebly REST API
====
A "REST" API to access and manipulate page data for the Mini Weebly Project

#Usage
Use cURL or any other HTTP requests library to call the methods as defined below. In addition, each URL must be supplied a param called `apiToken` with the value of the user's API Token, as defined in the web interface.

#Data Format
The Mini Weebly REST API allows you to access and manipulate `Pages` on the server.

###Page
A `Page` has the following properties:
- `gplusId`: (String) The Google+ ID of the user linked to the page
- `id`: (Integer) The unique ID of the page
- `title`: (String) Title of the page
- `textElements`: (TextElement[]) Array of `TextElement` objects contained in this page
- `imageElements`: (ImageElement[]) Array of `TextElement` objects contained in this page

###TextElement
A `TextElement` represents a block of text. It has the following properties:
- `pageId`: (Integer) The unique ID of the Page the TextElement is part of
- `id`: (Integer) The unique ID of the TextElement
- `content`: (String) The text content of the element
- `xCoord`: (String) Absolute offset from the left boundary of the page. The string is in CSS format (e.g. `"26px"`).
- `yCoord`: (String) Absolute offset from the top boundary of the page. The string is in CSS format (e.g. `"100px"`).
- `width`: (String) Width of the element as a CSS formatted string (eg. `"200px"`).
- `height`: (String) Height of the element as a CSS formatted string (eg. `"200px"`).

###ImageElement
A `ImageElement` represents an image on the page. It has the following properties:
- `pageId`: (Integer) The unique ID of the Page the TextElement is part of
- `id`: (Integer) The unique ID of the TextElement
- `imgUrl`: (String) The filename of the image. NOTE: As of now, the image is not uploaded, so the image needs to be in the [`../static/`](https://github.com/shivamthapar/weebly-mini/tree/master/app/static) directory.
- `xCoord`: (String) Absolute offset from the left boundary of the page. The string is in CSS format (e.g. `"26px"`).
- `yCoord`: (String) Absolute offset from the top boundary of the page. The string is in CSS format (e.g. `"100px"`).
- `width`: (String) Width of the element as a CSS formatted string (eg. `"200px"`).
- `height`: (String) Height of the element as a CSS formatted string (eg. `"200px"`).

#Methods

GET /api/pages (Get all pages)
--------------------------------------
Get a JSON representation of all of the user's pages.

Sample cURL call:
```
curl --get http://localhost:5000/api/pages?apiToken=APITOKEN
```
Response:
```
{"pages": [{"imageElements": [{"pageId": 1, "yCoord": "50px", "height": "279px", "width": "501px", "xCoord": "10px", "id": 1, "imgUrl": "dummy_image.png"}], "gplusId": "115899113282816200821", "id": 1, "textElements": [{"pageId": 1, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 1}, {"pageId": 1, "yCoord": "390px", "height": "150px", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum volutpat diam et mauris blandit ultricies sed sit amet arcu. Aenean quis lectus nibh. Morbi vulputate, neque vel condimentum volutpat, tellus eros luctus nibh, et tristique massa neque vel nibh. Quisque vitae metus tellus. Etiam blandit dolor non egestas aliquet. Mauris consequat neque ut quam semper placerat. Curabitur vulputate finibus nunc, in ultricies augue tincidunt eu.", "width": "500px", "xCoord": "26px", "id": 2}], "title": "Page Title"}, {"imageElements": [{"pageId": 5, "yCoord": "70px", "height": "279px", "width": "501px", "xCoord": "26px", "id": 4, "imgUrl": "dummy_image.png"}], "gplusId": "115899113282816200821", "id": 5, "textElements": [{"pageId": 5, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 7}, {"pageId": 5, "yCoord": "390px", "height": "150px", "content": "CONTENT CHANGED YAAAY", "width": "500px", "xCoord": "26px", "id": 8}], "title": "Page Title"}]}
```
GET /api/page/:id (Get a specific page)
--------------------------------------
Get a JSON representation of a specific page with the given `id`.

Sample cURL call:
```
curl --get http://localhost:5000/api/pages/1?apiToken=APITOKEN
```
Response:
```
{"imageElements": [{"pageId": 1, "yCoord": "50px", "height": "279px", "width": "501px", "xCoord": "10px", "id": 1, "imgUrl": "dummy_image.png"}], "gplusId": "115899113282816200821", "id": 1, "textElements": [{"pageId": 1, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 1}, {"pageId": 1, "yCoord": "390px", "height": "150px", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum volutpat diam et mauris blandit ultricies sed sit amet arcu. Aenean quis lectus nibh. Morbi vulputate, neque vel condimentum volutpat, tellus eros luctus nibh, et tristique massa neque vel nibh. Quisque vitae metus tellus. Etiam blandit dolor non egestas aliquet. Mauris consequat neque ut quam semper placerat. Curabitur vulputate finibus nunc, in ultricies augue tincidunt eu.", "width": "500px", "xCoord": "26px", "id": 2}], "title": "Page Title"}
```
POST /api/pages (Create a new page)
--------------------------------------
Create a new page with the given attributes. Returns a JSON representation of the page added.

Sample cURL call:
```
curl -X POST -H "application/json" -d  '{"imageElements": [{"pageId": 1, "yCoord": "50px", , "gplusId": "115899113282816200821", "textElements": [{"pageId": 1, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 1}, {"pageId": 1, "yCoord": "390px", "height": "150px", "content": "Text Content.", "width": "500px", "xCoord": "26px", "id": 2}], "title": "Page Title"}' http://localhost:5000/api/pages?apiToken=APITOKEN
```
Response:
```
{"imageElements": [{"pageId": 6, "yCoord": "50px", "height": "279px", "width": "501px", "xCoord": "10px", "id": 5, "imgUrl": "dummy_image.png"}, {"pageId": 6, "yCoord": "50px", "height": "279px", "width": "501px", "xCoord": "10px", "id": 6, "imgUrl": "dummy_image.png"}, {"pageId": 6, "yCoord": "50px", "height": "279px", "width": "501px", "xCoord": "10px", "id": 8, "imgUrl": "dummy_image.png"}], "gplusId": "115899113282816200821", "id": 6, "textElements": [{"pageId": 6, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 9}, {"pageId": 6, "yCoord": "390px", "height": "150px", "content": "Text Content.", "width": "500px", "xCoord": "26px", "id": 10}, {"pageId": 6, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 11}, {"pageId": 6, "yCoord": "390px", "height": "150px", "content": "Text Content.", "width": "500px", "xCoord": "26px", "id": 12}, {"pageId": 6, "yCoord": "364px", "height": "20px", "content": "this is sample text content #1", "width": "200px", "xCoord": "26px", "id": 15}, {"pageId": 6, "yCoord": "390px", "height": "150px", "content": "Text Content.", "width": "500px", "xCoord": "26px", "id": 16}], "title": "Page Title"}
```
PUT /api/page/:id (Update a specific page)
--------------------------------------
Replaces page with the given `id` with the page passed in.

Sample cURL call:
```
curl -X PUT -H "application/json" -d  '{"imageElements": [{"yCoord": "50px", "height": "279px", "width": "501px", "xCoord": "10px", "imgUrl": "dummy_image.png"}], "gplusId": "115899113282816200821", "textElements": [{"yCoord": "390px", "height": "150px", "content": "Text Content.", "width": "500px", "xCoord": "26px"}], "title": "Updated Page Title"}' http://localhost:5000/api/pages/6?apiToken=22af509b2ae9aa32fcf41e60cc935d2a0e881d597d971860823abbf3dbf52b7b
```
DELETE /api/page/:id (Delete a specific page)
--------------------------------------
Deletes page with the given `id`.

Sample cURL call:
```
curl -X DELETE http://localhost:5000/api/pages/6?apiToken=22af509b2ae9aa32fcf41e60cc935d2a0e881d597d971860823abbf3dbf52b7b
```

#Errors
If an API call fails, an Error object is returned with properties, `message` and `code`.

Sample error:
```
{"message": "Invalid API Token.", "code": 401}
```
