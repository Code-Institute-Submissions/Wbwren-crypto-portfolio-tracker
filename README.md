# Crypto Portfolio Tracker


## Project purpose 
The purpose of this website is to provide quick access to a users current cryptocurrency portfolio net worth.
The website will allow users to create an account and input their purchase history. This information will be compared to the current price of each coin and a total portfolio value and breakdown will be provided. Logging into secure cryptocurrency exchanges can be time consuming with two factor authentication and lengthy intricate passwords. This website will not have access to trading features and thus will not require such a secure, time consuming log in process. In addition, if the user wished to access, their current portfolio value on a device which they believe may be insecure, this website will provide peace of mind that even if their account is compromised, their investments will be safe.

## UX

### User stories
* As a user, I want to be able to register to the site, so that I can securely login.

    * 

* As a user, I want to be able to sign into my account, so that I have access to my personal porfolio.

    * 

* As a user, I would like the user experience on the website to be
intuitive, so that %%

    * The user dashboard provides a [minimal and intuitve UI](https://github.com/Wbwren/crypto-portfolio-tracker/blob/master/assets/img/user-dashboard.png)

* As a user, I want to be able to record my purchased coins, so that I can keep track of my portfolio

    * 

* As a user, I want to be able to record any coins I sell, so that I can keep my portfolio up to date.

    * 

* As a user, I want to be able to view the current value of my portfolio, so that I know when I reach my investment targets.

    * 

* As a user, I want to view my total profit and loss, so that I can assess the effectiveness of my 
investing startegy.
    
    * 




### Strategy
__Goal__: Allow users to quickly view how their portfolio is performing without access to their funds directly.


### Scope
* A website that allows users to create an account, log cryptocurrency transaction history and monitor their portfolio value.

### Design and colors:


#### Colors:

* Alice Blue - font color


#### Wireframes
* [Mobile View](https://github.com/Wbwren/crypto-portfolio-tracker/blob/master/wireframes/mobile-wireframe.png)

* [Tablet View](https://github.com/Wbwren/crypto-portfolio-tracker/blob/master/wireframes/tablet-wireframe.png)

* [Desktop View](https://github.com/Wbwren/crypto-portfolio-tracker/blob/master/wireframes/desktop-wireframe.png)


### Features:

#### Nomics API

This application uses the Nomics API to retreive live coin prices. Each time the user directs to the dashboard, the API is called and prices updated. Nomics prices are updated every 10 seconds.

#### Symbol retreiver
A script called symbol_retreiver is located in the root directory for retreiver ticker symbols and loading into the csv file.
When new coins are added by the Nomics API, running this script will integrate them into the website.


### Deployment

#### Cloning - Github 

1. Follow this link to my [Repository on Github](https://github.com/Wbwren/crypto-portfolio-tracker) and open it.
2. Click `Clone or Download`.
3. In the Clone with HTTPs section, click the `copy` icon.
4. In your local IDE open Git Bash.
5. Change the current working directory to where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied earlier.
7. Press enter and your local clone will be ready.

### Technology Used:

#### Languages:

* HTML5
* CSS3
* JavaScript
* Python

#### Libraries, Frameworks and Tools

* <a href="https://www.heroku.com/">Heroku</a> for hosting the deployed application
* <a href="https://flask.palletsprojects.com/en/2.0.x/">Flask</a> for the project configuration
* <a href="https://jinja.palletsprojects.com/en/3.0.x/">Jinja2</a> as a templating engine
* <a href="https://p.nomics.com/cryptocurrency-bitcoin-api">Nomics</a> for retreiving live price data
* <a href="https://code.visualstudio.com/">VSCode</a> as the IDE
* <a href="https://git-scm.com/">Git</a> for version control
* <a href="https://github.com">Github</a> remote git storage service
* <a href="https://validator.w3.org/">W3C Validator</a> Used to check the validity of my HTML and CSS.
* <a href="http://pep8online.com/">PEP 8 Online Validator</a> Used to validate the Python code.
* <a href="https://moqups.com">Balsamiq</a> for creating the wireframes.
* <a href="https://getbootstrap.com/">Bootstrap</a> for developing a responsive, mobile-first website
* <a href="https://jquery.com/">jQuery</a> JavaScript library
* <a href="https://fonts.google.com/specimen/Nunito">Google Fonts</a>
* <a href="https://fontawesome.com/">FontAwesome</a>

#### Databases
* <a href="https://www.mongodb.com/">MongoDB</a> as the database service
 

## Testing

### Code Validation
* HTML was validated using W3C Markup Validation Service.

* CSS was validated using W3C CSS Validation Service - Jigsaw

* JavaScript was passed through the linter jshint with no warnings
### Functionality Tests
| Num | Test                                                                         | Action                              | Outcome image                                                                                                                        | Result |
|-----|------------------------------------------------------------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|--------|
| 1   | Navigation bar links work correctly | Click on each nav icon              | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 2   | User registraion requires valid data | Attempt to enter invalid data for each field | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 3   | User can login to site after registraition | Register for site and attempt to login | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 4   | User can access their dashboard after logging in | Login and click dashboard in navbar | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 5   | User can access the transactions page after logging in | Login and click transactions in navbar | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 6   | User can successfully logout | Click logout button in navbar | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 7   | User add add a transaction | Add a transaction and see if it apears in the transaction list | [Image of ](https://github.com/Wbwren/%%%.png) | Pass   |
| 8   | User can edit a transaction | Add transaction and attempt to edit it on the transactions page | [Image of form ](https://github.com/Wbwren/%%%.png) | Pass   |
| 9   | User can delete a transaction | Add transaction and attempt to delete it on the transactions page | [Image of form ](https://github.com/Wbwren/%%%.png) | Pass   |

### Non Functional Requirements
| Num | Test                                                                         | Action                              | Outcome image                                                                                                                        | Result |
|-----|------------------------------------------------------------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|--------|
| 1   | Dashboard is loaded in less than 2 seconds | Login and time the loadtime | [Image of form ](https://github.com/Wbwren/%%%.png) | Pass   |

Notes: initially the dashboard took excessivly long (>5s) to load when retreiving ticker symbols from mongodb. Placing the ticker
symbols in a csv in the root directory acheived this non funtional requirement.


<br>

### Browser Compatibility
| Num | Browser         | Test result |
| ---|:-------------:| :----: |
| 1 | Chrome | Passed
| 2 | Opera | Passed
| 3 | Mozzilla | Passed

<br>

### Responsiveness Testing
* Chrome developer tools was used to test a wide variety of device sizes and resolutions.

* The website has been tested on a Samsung Galaxy s10, Lenovo Legion and a desktop PC with a 1080p and 4k monitor, respectfully.



#### Deploy to Heroku 

1. On Heroku create an account and log in.
2. Click `new` and `create new app`.
3. Choose a unique name for your app, select region and click on `Create App`
4. Under the `Settings` click `Reveal Config Vars` and set IP to 0.0.0.0 and the PORT to 5000
5. Go to the CLI and type `$ sudo snap install --classic heroku`
6. Type `$ heroku login` command into the terminal
7. Create `requirements.txt` ($ sudo pip3 freeze --local > requirements.txt)
8. Create a `Procfile` (`$ echo web: python app.py > Procfile`)
9. Go back to Heroku, under `Deploy` find `Existing Git repository` and copy the command:`$ heroku git:remote -a <app_name>` Paste this into the terminal.
10. (If repository was not created already, type:
11. `$ cd my-project/`
12. `$ git init`
13. `$ heroku git:remote -a <app_name>`)
14. Type `$ heroku ps:scale web=1` into the terminal.
15. Go back to Heroku, and at `Settings` copy `https://<app_name>.herokuapp.com/` 
16. In the terminal type `git remote add http://<app_name>.herokuapp.com/`
16. Type `git push -u heroku master`
17. In the app dashboard, under `Settings` click on `Reveal Config Vars`
21. Set "MONGO_URI" and "MONGO_DBNAME" and "SECRET_KEY"
22. Once the build is complete, go back to Heroku and click on `Open App`