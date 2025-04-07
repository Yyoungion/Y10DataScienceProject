# Year 10 Software Engineering Documentation
**API** \
https://pokeapi.co/

## Requirements Definition

### Functional Requirements
**Data Retrieval** 
* The user has to be able to see a text box that the user will need to enter a pokemon name. 
* The user will also need to see the link of the sound file of the pokemon. 
* The user should be able to store the pokemon and go back to the sound.

**User Interface**
* The user has to type in pokemon names that they are interested in. 
* If there is enough time, there might be a GUI with buttons instead of typing to lower user error. 

**Data Display**
* After the user inputs the name of a pokemon, it will play the pokemons cry. 
* If the pokemon does not exist or the user inputs a error, it will play 10 random pokemon's cry at the same time.


### Non-Functional Requirements

**Performance**
* The system should perform decently well with little to no delays in the system. 
* The system should not freeze or crash unless the user is messing around.

**Reliablilty**
* The data is really reliable as the API is used by thousands of people each month. 
* The system should run reliably with little to no crashes and breaks in the code. 
* It should not break with a error by user input.

**Usability and Accessibility**
* The system should have easy to follow instructions that anyone can understand and follow. 
* It should be easy to navigate and follow.

## Determining Specifications

### Functional Specifications

**User Requirements**
* The user needs to be able to input words & phrases when asked a question in the code
* The user needs to be able to hear sound playing
* The user needs to be able to intereact with the system through commands and responses 

**Inputs and Outputs**
* The user will need to input the name of a pokemon
* The user will hear a sound output of the pokemon selected
* If the pokemon does not exist, the user will need to hear sound output of 10 differnt pokemon 
* The user will be able to store the pokemon and go back to in later in the program.

**Core Features**
* The program needs to request from the pokemon api
* The program needs to ask users for a pokemon name
* The program needs to store the user's pokemon
* The program needs to pull from the api
* The program needs to store a pokemon
* The program needs to play the sound of the pokemon stored 

**User Interaction**
* The user will interact with the system via line command
* If time allows it, there might be a GUI
* A README.md file will contain all instructions on how to run the application and any dependencies
* A txt file will contain the requirements for the system to function i.e Windows 

**Error Handleing**
* If the user inputs a pokemon that does not exist or a number/symbol, then the system will output 10 random pokemon sounds at the same time.
* It it is a system error, it will most likely be fixed upon release. However, if the error is not fixed, it will play 10 random pokemon sounds at the same time




### Non-Functional Specifications

**Performance**
* The system should run programs within seconds
* The system should not lag or take to long to process inputs and outputs to maintain user engagement
* To make the system more efficient, classes and functions will be used to minimise the repetition of code in the program.

**Useability / Accessibility**
* The program should be easy to read and simple when asking for user interaction
* It should avoid unnessisary interactions with the user.
* Simple terms should be used to make the system easier to understand

**Reliability**
* The system should not crash
* If an error occures, the system will output 10 different pokemon sounds 

### Use Cases
**Actor**
* User

**Preconditions**
* Access to the internet
* API of pokemon is available
* Pip installed
* Playsound installed
* Pygame installed

**Main Flow**
* *Search of pokemon* - User eners the name of their pokemon and the system retreives the sound of the pokemon from the api
* *Sound display* - It will output the pokemon's cry
* *Pokemon Storage* - It will store the pokemon
* *Storeage output* - It will output stored pokemon sounds

**Alternative Flows**
* *Error* - If the pokemon does not exist, it will output 10 random pokemon cries

**Postconditions**
* The name of the pokemon is retreived
* The cry of the pokemon is outputed


## Design

### Gantt Chart
![](Images/Gantt-chart.png "")

### Structure Chart
![](Images/Structure-chart.png "")

### Algorithms - Flowchart
**Main**
![](Images/Algorithms-main().png "") 
**Play Sound** \
![](Images/Algorithms-playsound().png "")\
**Play Random Sound** \
![](Images/Algorithms-playrandomsound().png "")

### Algorithms - Pseudocode
**Main** \
BEGIN main() \
&nbsp;&nbsp; choice = 0 \
&nbsp;&nbsp; WHILE choice is not 4 \
&nbsp;&nbsp;&nbsp;&nbsp; INPUT choice \
&nbsp;&nbsp;&nbsp;&nbsp; WHILE choice is bigger than 4 \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; playrandomsound \
&nbsp;&nbsp;&nbsp;&nbsp; ENDWHILE \
&nbsp;&nbsp;&nbsp;&nbsp; IF choice is 1 THEN \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; playsound \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; IF storesound is true THEN \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; storesound \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ELSE \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; do nothing \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ENDIF \
&nbsp;&nbsp;&nbsp;&nbsp; ELSEIF choice is 2 THEN \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; playstoresound \
&nbsp;&nbsp;&nbsp;&nbsp; ELSE \
&nbsp;&nbsp;&nbsp;&nbsp; do nothing \
&nbsp;&nbsp;&nbsp;&nbsp; ENDIF \
&nbsp;&nbsp; ENDWHILE \
END main() 

**Play Sound**\
BEGIN playsound(number) \
&nbsp;&nbsp; request API \
&nbsp;&nbsp; pokemon = number \
&nbsp;&nbsp; DISPLAY pokemon sound \
END playsound() 

**Play Random Sound**\
BEGIN playrandomsound() \
&nbsp;&nbsp; i = 0 \
&nbsp;&nbsp; WHILE i is smaller than 10 \
&nbsp;&nbsp;&nbsp;&nbsp; rn is equal to random.randint(1, 1302) \
&nbsp;&nbsp;&nbsp;&nbsp; playsound(rn) \
&nbsp;&nbsp;&nbsp;&nbsp; i is equal to i + 1 \
&nbsp;&nbsp; ENDWHILE \
END playrandomsound()

### Data Dictionary
| Variable | Data Type | Format for Display | Size in Bytes | Size for Display | Description | Example | Validation |
| -------- | ------- | -------- | ------- | -------- | ------- | -------- | -------- |
| PokemonID | Integer | Whole number | 4 | 4 | The pokemon's ID number | 123 | It has to be bigger or equal to one or small or equal to 1302 |
| PokemonName | String | Text | 50 | 50 | The pokemon's name number | Ditto | It has to be a valid pokemon name |
| Username | String | Text | 50 | 50 | The username of the user | Yyoungion | It has to be a regestered username from the Login.csv. |
| Password | String | Text | 50 | 50 | The password in relation to the username | Password1 | It has to be the regestered password from Login.csv in relation to the username inputed. |



## Editing Github Commits

**Mar 5**
* Documentation
* Started working on Documenting the requirements and specifications on markdown. I got up to Non-Functional Requirements - Reliability.

**Mar 7**
* Began Program Experimenting
* I tried to test playing sound from my API. It did not work. I then found a tutorial that taught me how to request from an API. It allowed me to request things like ID and Typings for pokemon, which allowed me to start understanding how requesting worked. Next, I needed to figure out how to download a MP3 file from a provied link.

**Mar 10**
* Project Development
* I continued to work on my documentation, finished the reqirements and specifications. I also created a Gantt chart. 

**Mar 11**
* Flowchart & Structure Chart
* I created my Flowchart for main() and Sructure chart. 

**Mar 13**
* Program testing
* Nothing much was done here. I tried to play sound but it failed miserably. 

**Mar 17**
* Algorithm - Playrandomsound
* I have added a flowchart for playrandomsound 

**Mar 18**  
* Algorithm Playsound
* I added a flowchart for playsound.  I also developed my python. It can now obtain the download link for pokemon sound file.

**Mar 19**
* Attempted to play sound
* I tried to playsound using the download link. I then figured out that I have to download the file before being able to play sound from it

**Mar 20**
* Psuedocode
* I created psuedocode for all 3 of my flowcharts. I also made a Data Dictionary

**Mar 21**
* Playsound!
* I can now download and playsound from the API. However, I ran into a problem where the path for the folder was different for each person, which I had to find a way to fix.

**Mar 24**
* Fixed Downloading problem
* The program now does not break if an already downloaded file wants to get downloaded again. 

**Mar 25**
* GUI Attempt
* I tried to create a gui but I had no idea how to do it. I almost broke my code and later had to revert back to an earlier commit. I then made a simple version of my GUI later that afternoon.

**Mar 26**
* Easteregg
* I created a fun thin where every time someone wanted to view stored sounds, all the buttons were random colors.

**Mar 27**
* Error handling
* Created a thing where if there were no stored sounds, it would output: No stored sounds found, instead of breaking.

**Apr 2**
* Created Login
* I created a login, which allowed for individual people's sounds to be stored in their own seperate folders. 

**Apr 7** (Current)
* Redid the Github Commits. I also updated the structure chart to match the my program, such as the addition of a login.

