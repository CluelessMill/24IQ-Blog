from requests import post

url = "http://localhost:8000/api/posts/create"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiQWNjZXNzVG9rZW4iLCJ1c2VyX2lkIjoyNSwiY3JlYXRlZCI6IjIwMjQtMDUtMDNUMTE6NTQ6MTYuNDk2MDE3KzAwOjAwIiwiZXhwaXJlZCI6IjIwMjQtMDUtMDNUMTI6MjQ6MTYuNDk2MDE3KzAwOjAwIn0.Fdh85xyKSvD_5siI54n8Kaas0UjLMbrHuUb5ZdCP0Es"
title = "Liminal creature"
text = 'In the example above, we declare both quote and fact in the same line with one operator (:=). These variables are then assigned their respective values based on the ordering of variables and value. Since quote is the first variable, and the string "Bears, Beets, Battlestar Galactica" is the first value, quote has a value of "Bears, Beets, Battlestar Galactica". Similarly, fact then is assigned the value true.'
category = "development"

with open(file="2.jpg", mode="rb") as logo_file, open(
    file="1.jpg", mode="rb"
) as main_img_file:
    files = {
        "title": (None, title),
        "text": (None, text),
        "categofry": (None, category),
        "logoImg": ("logo.jpg", logo_file, "image/jpeg"),
        "mainImg": ("nn.jpg", main_img_file, "image/jpeg"),
    }

    response = post(url=url, files=files, cookies={"accessToken": access_token})

if response.status_code == 201:
    print("News uploaded successfully. News ID:", response.text)
else:
    print("Failed to upload news. Status code:", response.status_code)
    print("Error message:", response.text)
