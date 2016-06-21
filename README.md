# BT Text

What is this project?
------
Code for NRV is collaborating with Blacksburg Transit to improve their SMS (texting) and IVR (interactive voice response) systems. While they currently use an in-house solution to provide responses to users that text and call to receive current bus arrival status, they wanted to explore the option of using a third-party service. [Twilio](https://www.twilio.com/) is one of the more popular services offering both SMS and IVR in a REST-based API. This project is the development against that API to provide responses to users of BT.
* Built using Python and [Flask](http://flask.pocoo.org/)

Status
------
Currently a work in progress with no deployment

A single endpoint for SMS replies has been created and works with out any error handling currently implemented.

Contributing
------
Use Issues to join the discussion or come to a [hack night](http://www.meetup.com/CodeforNRV/)

Deploying using Docker
------
A Docker image is available on Gitlab.com and can be run like so:
```bash
docker run --name bt_text -p 80:80 -d registry.gitlab.com/codefornrv/bt_text
```

If you want to do local development, you can do a git clone to put the files on your machine. Then run:
```bash
docker run --name bt_text -p 80:80 -v /path/to/bt_text/:/app -d registry.gitlab.com/codefornrv/bt_text
```
replacing "/path/to/bt_text/" with the location of the git repository you just cloned. To actually test with a Twilio you've setup, 
you'll need this server to be available from the outside world from a public IP or DNS entry so that you can configure your Twilio account to use it.

License
------
BT Text is licensed under the [MIT](LICENSE) license.
