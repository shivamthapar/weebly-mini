====
Mini Weebly REST API
====
A "REST" API to access and manipulate page data for the Mini Weebly Project

#Usage
Use cURL or any other HTTP requests library to call the methods as defined below. In addition, each URL must be supplied a param called `apiToken` with the value of the user's API Token, as defined in the web interface.

#Methods

GET /api/pages (Get all pages)
--------------------------------------
Get a JSON representation of all of the user's pages.

Sample cURL call:
```

```
GET /api/page/:id (Get a specific page)
--------------------------------------
POST /api/pages (Create a new page)
--------------------------------------
PUT /api/page/:id (Update a specific page)
--------------------------------------
DELETE /api/page/:id (Delete a specific page)
--------------------------------------
