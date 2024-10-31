#Summary
This project looks to do a few different things. 
1. Randomize DND race, gender, stats, and more to provide a new character to play
2. Create and store the details of your own character
3. Update your character's stats and other information
4. Delete characters
5. Additionally you can view an image of your character stored with the data
6. Register a user
7. A user can login to create chracters
8. A user can create a campaign, relate characters to campaign, and edit stats of a character in a related campaign

#Installation
#First create the docker container
docker build -t CharacterCreation .
#Run the process
docker run CharacterCreation
#makemigration to postgres
docker-compose run web python manage.py makemigrations
#migrate the database
docker-compose run web python manage.py migrate
#compose and build the container again
docker-compose up --build


#Getting Started
docker-compose up


#License
The MIT License (MIT)

Copyright (c) Justin Tobiason 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), 
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
