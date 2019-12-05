Just HTTP api for send email via smtp server

Right now create only POST request with this params:

| Option | Description                                                                                  |
| ------ | :------------------------------------------------------------------------------------------- |
| files  | dict with necessery template for jinja2, and include additional files int 'rb' type.         |
| data   | dict with necessery vars to,From,subject. Here you can add vars for jinja formating template |
| url    | where you start this server                                                                  |
> For more information see in ./example/example.py


Today we add CI-CD for automate deploy add port style