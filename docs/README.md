**Story 1**

As a **user**, I want to **register a new accoutn** so I can **create a new character**

**Acceptance Criteria**
1. A user can create a new user


**Story 2**

As a **user**, I want to **create a new character with user input stats for a dnd 5e game** so I can **keep track of my character's stats**.

**Acceptance Criteria**
1. User can input stats, race, and gender into the application and it will be saved to the database

**Story 3**

As a **user**, I want to **randomize a new character for a dnd 5e game** so I can **play with a newly randomized character**.

**Acceptance Criteria**
1. User must be able to submit a request to have a new character generated for him
2. The information is returned to the user

**Story 4**

As a **user**, I want to **reset my password** so that I can **set a new password for my account**

**Acceptance Criteria**
1. User can reset password based on the user having an existing account

**Story 5**

As a **user**, I want to **delete my chracter** so that I can **remove it from the list of my characters**

**Acceptance Criteria**
1. Allow the user to delete a character 


**Story 6**

As a **user**, I want to **update one of my character's stats** so that I can **keep my character up-to-date**

**Acceptance Criteria**
1. Allow a user to select and update a character's stats

**Story 7**

As a **user**, I want to **add a picture of my character** so that I can **store my character's look**


**Story 8**

As a **admin**, I want to **moderate user images** so that I can **delete images from the database**

**Acceptance Criteria**
1. Allow a admin/superuser to delete user photos from the site

**Story 9**


As an **admin**, I want to **disable users** so that **they cannot use their accounts**

**Acceptance Criteria**
1. Give admin/superuser acess to disabling user accounts


**Mis User Stories**

**Story 1**

As a **bad actor**, I want to **brute force accounts** so that **I can access a user's information**

**Notes**
https://attack.mitre.org/techniques/T1110/

**Acceptance Criteria**
1. Limit the number of times a user can attempt to login an lock that user out for a period of time
2. Set the password creation of users to user NIST acceptable password critieria

**Story 2**

As a **bad actor**, I want to **inject malicious software into my service** so that I can **execute malicious code**

**Notes**
https://attack.mitre.org/techniques/T1659/

**Acceptance Criteria**
1. Validate the image uploaded is of certain file types.

**Story 3**

As a **bad actor**, I want to **sniff password data in between the user and service** so that I can **access a user's account**

**Notes**
https://attack.mitre.org/techniques/T1557/

**Acceptance Criteria**
1. Enable HTTPS on django