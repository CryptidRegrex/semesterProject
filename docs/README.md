**Story 1** (COMPLETED)

As a **user**, I want to **register a new accoutn** so I can **create a new character**

**Acceptance Criteria**
1. A user can create a new user


**Story 2** (COMPLETED)

As a **user**, I want to **create a new character with user input stats for a dnd 5e game** so I can **keep track of my character's stats**.

**Acceptance Criteria**
1. User can input stats, race, and gender into the application and it will be saved to the database

**Story 3** (COMPLETED)

As a **user**, I want to **randomize a new character for a dnd 5e game** so I can **play with a newly randomized character**.

**Acceptance Criteria**
1. User must be able to submit a request to have a new character generated for him
2. The information is returned to the user

**Story 4** (COMPLETED)

As a **user**, I want to **reset my password** so that I can **set a new password for my account**

**Acceptance Criteria**
1. User can reset password based on the user having an existing account
2. It will send an email to the existing user with a reset password link

**Story 5** (COMPLETED)

As a **user**, I want to **delete my chracter** so that I can **remove it from the list of my characters**

**Acceptance Criteria**
1. Allow the user to delete a character 


**Story 6** (COMPLETED)

As a **user**, I want to **update one of my character's stats** so that I can **keep my character up-to-date**

**Acceptance Criteria**
1. Allow a user to select and update a character's stats

**Story 7** (COMPLETED)

As a **user**, I want to **add a picture of my character** so that I can **store my character's look**


**Story 8** (COMPLETED)

As a **admin**, I want to **moderate user images** so that I can **delete images from the database**

**Acceptance Criteria**
1. Allow a admin/superuser to delete user photos from the site

**Story 9** (COMPLETED)


As an **admin**, I want to **disable users** so that **they cannot use their accounts**

**Acceptance Criteria**
1. Give admin/superuser acess to disabling user accounts


**Story 10** (COMPLETED)

As a **DM**, I want to **Create a campaign** players can join **so that I can have all plyer information to view**

**Acceptance Criteria**
1. Create a campaign
2. Relate characters to campaign objects
3. Give access to Owner of campaign to player's character


**Story 11** (COMPLETED)


As a **DM**, I want to **Relate a Character to a Campaign** so that **I can update a player's character info**

**Acceptance Criteria**
1. Allow owner of campaign to update character's info. 





**Mis User Stories**

**Story 1**

As a **bad actor**, I want to **brute force accounts** so that **I can access a user's information**

**Notes**
https://attack.mitre.org/techniques/T1110/

**Acceptance Criteria**
1. Limit the number of times a user can attempt to login an lock that user out for a period of time
2. Set the password creation of users to user NIST acceptable password critieria

**Story 2** (COMPLETED)

As a **bad actor**, I want to **inject malicious software into my service** so that I can **execute malicious code**

**Notes**
https://attack.mitre.org/techniques/T1659/

**Acceptance Criteria**
1. Validate the image uploaded is of certain file types.

**Story 3** (COMPLETED)

As a **bad actor**, I want to **sniff password data in between the user and service** so that I can **access a user's account**

**Notes**
https://attack.mitre.org/techniques/T1557/

**Acceptance Criteria**
1. Enable HTTPS on django

**Story 4** (COMPLETED)

As a **bad actor**, I want to **input bad data into data fields** so that I can **break or manipulate the system**

**Notes**
https://attack.mitre.org/mitigations/M0818/

**Acceptance Criteria**
1. Validate user input to insure injection, record corruption, or system breakage cannot occur.



**Diagrams**

![Index Page](./images/IndexPage.drawio.png)

![Authenticated Index Page](./images/AuthenticatedIndex.drawio.png)

![Login Page](./images/LoginPage.drawio.png)

![Register Page](./images/RegisterPage.drawio.png)

![User Page](./images/UserPage.drawio.png)

![Character Design Page](./images/CharacterDesignPage.drawio.png)

![Create Campaign Page](./images/CreateCampaign.drawio.png)


**C4 Model**

**System**

![Authenticated Index Page](./images/SystemContextDND.drawio.png)

**Container**

![Authenticated Index Page](./images/Container.drawio.png)

**Context**

![Authenticated Index Page](./images/Multi-PageApplication.drawio.png)
