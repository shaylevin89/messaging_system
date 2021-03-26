# messaging_system

Messaging system API using JWT authentication<br>
Main server- Python Flask hosting in Heroku on https://shaymessages.herokuapp.com/<br>
Database server- Postgresql hosting in Heroku

<h3>Instructions:</h3>
Import messaging_system.postman_collection.json to postman<br>


<h3>API:</h3>

Create user- POST request to /register. With JSON body of username and password<br>
Example- [POST] https://shaymessages.herokuapp.com/register [body] {"username": "yourName", "password": "abcd1234"}

Login- POST request to /login with basic authentication, username and password<br>
Example- [POST] https://shaymessages.herokuapp.com/login [basic auth] username: yourname, password: abcd1234

Create message- POST request to /message. With JSON body of receiver, subject, msg_data. (have to be logged in)<br>
Example- [POST] https://shaymessages.herokuapp.com/message [body] {"receiver": "another username", "subject": "message subject", "msg_data": "the message content"}

Read all user messages (sent or received)- GET request to /messages. (have to be logged in)<br>
Example- [GET] https://shaymessages.herokuapp.com/messages

Read all unread messages of user (sent or received)- GET request to /unread_messages. (have to be logged in)<br>
Example- [GET] https://shaymessages.herokuapp.com/unread_messages

Read one message of user (sent or received)- GET request to /message/<msg_id>. (have to be logged in)<br>
Example- [GET] https://shaymessages.herokuapp.com/message/15

Delete one message of user (sent or received)- DELETE request to /message/<msg_id>. (have to be logged in)<br>
Example- [DELETE] https://shaymessages.herokuapp.com/message/18
