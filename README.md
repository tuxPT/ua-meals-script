# __WARNING__ : THIS REPOSITORY IS BEING MERGED INTO https://github.com/GLUA-UA/meals-ua 

# Install
```shell
$ cp systemd/* ~/.config/systemd/user/
$ mkdir ~/.ua-meals
$ cp meals.py ~/.ua-meals/
$ systemctl --user enable meals.timer
$ pip3 install --user requirements.txt 
```
