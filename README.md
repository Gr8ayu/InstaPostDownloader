# InstaPostDownloader

InstaPostDownloader helps you download all the posts from Instagram public account just by typing their username. It collects and stores the images in a separate folder with their captions. It also stores the displayed content in separate file which can help you get training dataset for your image classification project.

Requirements : 

  -  beautifulsoup4==4.7.1
  - bs4==0.0.1
  - certifi==2019.6.16
  - chardet==3.0.4
  - idna==2.8
  - requests==2.22.0
 - selenium==3.141.0
 - soupsieve==1.9.1
 - urllib3==1.25.3
# How to Use  :
 ###### (For Ubuntu 18.04)
  ####  [create a virtual environment](https://www.geeksforgeeks.org/python-virtual-environment/)
  ```sh
  $ pip install virtualenv
  # test your installation
  $ virtualenv --version
  # create your virtual environment with desired name
  $ virtualenv -p /usr/bin/python3 virtualenv_name
  # Now after creating virtual environment, you need to activate it. 
  $ source virtualenv_name/bin/activate
  
  # Once you are done with the work, you can deactivate the virtual environment by the following command:
  (virtualenv_name)$ deactivate
  ```
  #### installing required modules
  ```sh
  # navigate to requirement.txt and execute following command
  $ pip install -r requirements.txt
  ```
 #### install Geckodriver for Firefox:
 ```sh
# Go to the geckodriver releases page. Find the latest version of the driver for your platform and download it. For example:
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

# Extract the file with:
$ tar -xvzf geckodriver*

# Make it executable:
$ chmod +x geckodriver

Add the driver to /usr/local/bin/:
$ sudo mv geckodriver /usr/local/bin/
 ```
 
 #### Running Script:
 ```sh
 $ python3 InstaPostDownloader.py
 ```

# How To Contribute
Feel free to make any changes to improve functionalities or to add new features
Follow the steps given below,
1. Fork, https://github.com/Gr8ayu/InstaPostDownloader
2. Execute, `git clone https://github.com/<your-github-username>/InstaPostDownloader/`
3. Change your working directory to `../InstaPostDownloader`.
4. Execute, `git remote add origin_user https://github.com/<your-github-username>/InstaPostDownloader/`
5. Execute, `git checkout -b <your-new-branch-for-working>`.
6. Make changes to the code.
7. Add your name and email to the AUTHORS.
8. Execute, `git add .` .
9. Execute, `git commit -m "your-commit-message"` .
10. Execute, `git push origin_user <your-current-branch>` .
11. Make a Pull Request.

