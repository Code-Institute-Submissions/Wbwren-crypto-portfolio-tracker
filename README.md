# Crypto Portfolio Tracker

## Project purpose 
The purpose of this website is to provide quick access to a users current cryptocurrency portfolio net worth.
The website will allow users to create an account and input their purchase history. This information will be compared to the current price of each coin and a total portfolio value and breakdown will be provided. Logging into secure cryptocurrency exchanges can be time consuming with two factor authentication and lengthy intricate passwords. This website will not have access to trading features and thus will not require such a secure, time consuming log in process. In addition, if the user wished to access, their current portfolio value on a device which they believe may be insecure, this website will provide peace of mind that even if their account is compromised, their investments will be safe.

## UX

## UX

### User stories
* As a user, I want to be able to register to the site, so that I can securely login.

    * 

* As a user, I want to be able to sign into my account, so that I have access to my personal porfolio.

    * 

* As a user, I would like the user experience on the website to be
intuitive, so that 

    * The user dashboard provides a [minimal and intuitve UI](https://github.com/Wbwren/crypto-porfolio-tracker/blob/master/assets/img/user-dashboard.png)

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

#### Fonts:

%%, from Google Fonts.

%% is used as the backup font.

#### Colors:

* %% - font color

* %% - card, media background color


#### Wireframes
* [Mobile View](https://github.com/Wbwren/crypto-porfolio-tracker/blob/master/wireframes/mobile-wireframe.png)

* [Tablet View](https://github.com/Wbwren/crypto-porfolio-tracker/blob/master/wireframes/tablet-wireframe.png)

* [Desktop View](https://github.com/Wbwren/crypto-porfolio-tracker/blob/master/wireframes/desktop-wireframe.png)


### Features:

#### Nomics API

This application uses the Nomics API to retreive live coin prices. Each time the user directs to the dashboard, the API is called and prices updated. Nomics prices are updated every 10 seconds.


### Deployment

#### Cloning - Github 

1. Follow this link to my [Repository on Github](https://github.com/Wbwren/crypto-portfolio-tracker) and open it.
2. Click `Clone or Download`.
3. In the Clone with HTTPs section, click the `copy` icon.
4. In your local IDE open Git Bash.
5. Change the current working directory to where you want the cloned directory to be made.
6. Type `git clone`, and then paste the URL you copied earlier.
7. Press enter and your local clone will be ready.
 

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