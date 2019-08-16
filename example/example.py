import requests
import test

# test.host like 'localhost:80'
url = "http://" + test.host + "/sendTemplate"

data = {
    # Send to like 'example@ex.com'
    'to': test.to,
    # Send from like 'example@ex.com'
    'From': test.From,
    # Subject like 'Example subject'
    'subject': test.subject,
}


files = {
    'example.png': open('example.png', 'rb'),
    'template': open('template.html.j2', 'rb'),
    'att1.html': open('template.html.j2', 'rb')
}
r = requests.post(url, files=files, data=data)
print(r.text)
