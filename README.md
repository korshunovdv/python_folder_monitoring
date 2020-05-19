# folder_monitoring
Mini program to automatically receive new files from server.

Mini program (python and RabbitMQ) for monitoring folder on server and copy/remove files on clients folder according to server.

Usage: 
1. On first terminal starting RabbitMQ - 'rabbitmq-server' (https://www.rabbitmq.com/download.html - visit if not installed)
2. On server side starting server.py and choosing folder for monitoring - 'python server.py "target_folder" '
3. On client side starting client.py and choosing server address - ' python client.py "localhost" '

Thats all. When you copy new file to your server folder, user will see this file in client side. The same with removing file on server. 
