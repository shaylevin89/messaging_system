# messaging_system

Messaging system API using JWT authentication<br>
Main server- Python Flask hosting in Heroku on https://shaymessages.herokuapp.com/<br>
Database server- Postgresql hosting in Heroku

<h2>Instructions:</h2>
Import messaging_system.postman_collection.json to postman<br>


<h2>API:</h2><br>
<h3>URL</h3> https://shaymessages.herokuapp.com/<br>

* **Create user**<br>
Method: POST <br>
Path: /register  
Body: JSON object of username and password  {"username": "yourname", "password": "yourpassword"}<br>
Success response: User created, 200 OK<br>
Error response: Credentials missing, 400 bad request<br>
Error response: Username not available, 400 bad request<br>



* **Login**<br> 
Method: POST <br>
Path: /login<br>
Authorization: basic auth- username and password <br>
Success response: Token, 200 OK<br>
Error response: Missing fields, 400 bad request<br>
Error response: Authentication failed, 400 bad request<br>

* **Create message**<br> 
Method: POST <br>
Path: /message<br>
Body: JSON object of receiver, subject, msg_data. {"receiver": "message_to", "subject": "message_subject", "msg_data": "content"}<br>
Authorization: Header with Auth-token key and valid token value <br>
Success response:Message created, 200 OK<br>
Error response: Wrong message format, only JSON accepted, 400 bad request<br>
Error response: Message did not insert, 400 bad request<br>
Error response: Wrong message data, 400 bad request<br>

* **Read all user messages**<br> 
Method: GET <br>
Path: /messages<br>
Authorization: Header with Auth-token key and valid token value <br>
Success response: Array of user messages, 200 OK<br>
Success response:No messages for current user, 200 OK<br>

* **Read all unread messages of user**<br> 
Method: GET <br>
Path: /unread_messages<br>
Authorization: Header with Auth-token key and valid token value <br>
Success response: Array of user unread messages, 200 OK<br>
Success response:No unread messages for current user, 200 OK<br>

* **Read one message**<br> 
Method: GET <br>
Path: /message/<msg_id><br>
Authorization: Header with Auth-token key and valid token value <br>
Success response: JSON message, 200 OK<br>
Error response: Msg_id not available, 400 bad request<br>
Error response: Msg_id not valid, 400 bad request<br>

* **Delete one message**<br> 
Method: DELETE <br>
Path: /message/<msg_id><br>
Authorization: Header with Auth-token key and valid token value <br>
Success response: Message <msg_id> no longer exist, 200 OK<br>
Error response: Msg_id not valid, 400 bad request<br>


