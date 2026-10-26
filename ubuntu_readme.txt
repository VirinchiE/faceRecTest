//......... Installation steps for Ubuntu Server .........

sudo apt-get update && sudo apt update \
sudo apt-get upgrade && sudo apt upgrade
1. mkdir attendance-app
2. cd attendance-app
//first check python and pip version if pip is not installed then:
3. sudo apt install python3-pip
//check if gcc is already installed: gcc --version if not install gcc
4. sudo apt -y install cmake
5. sudo apt-get install qtbase5-dev
6. sudo apt-get install libgtk-3-dev
7. sudo apt install ffmpeg
8. sudo apt install libopenexr-dev
9. sudo apt-get install libwebp-dev
10. sudo apt-get install freeglut3-dev
11. sudo apt install libdc1394-22-dev
12. sudo apt-get install libboost-all-dev

13. sudo pip3 install virtualenv virtualenvwrapper
14. echo "export WORKON_HOME=~/.virtualenvs" >> ~/.bashrc
15. echo "VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.9" >> ~/.bashrc
15. echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc // after this do not forget to reload bashrc by .~/.bashrc command  
16. source `which virtualenvwrapper.sh`
17. mkvirtualenv AttendanceFaceEnv -p python3
18. workon AttendanceFaceEnv
19. pip install cmake
20. pip install numpy scipy matplotlib scikit-image scikit-learn ipython
21. deactivate
22. wget https://github.com/Kitware/CMake/releases/download/v3.15.2/cmake-3.15.2.tar.gz
23. tar -zxvf cmake-3.15.2.tar.gz
24. cd cmake-3.15.2
25. ./bootstrap
26. make
27. sudo make install
28. cd ..
29. git clone https://github.com/opencv/opencv.git
30. git clone https://github.com/opencv/opencv_contrib.git
31. cd opencv
32. mkdir build
33. cd build
34. cmake -DWITH_QT=ON -DBUILD_TBB=ON -DWITH_OPENGL=ON -DWITH_TBB=ON -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF -DBUILD_TESTS=OFF -OPENCV_CONTRIB=OFF -DENABLE_PRECOMPILED_HEADERS=OFF -DOPENCV_GENERATE_PKGCONFIG=ON -DCMAKE_PREFIX_PATH=/Applications/Qt/5.12.3/clang_64/ ..
35. make
36. sudo make install
37. cd ../..
38. echo "export LC_ALL=en_US.UTF-8" >> ~/.bash_profile
39. echo "export CC=/usr/bin/gcc" >> ~/.bash_profile
40. echo "export CPP=/usr/bin/cpp" >> ~/.bash_profile
41. echo "export CXX=/usr/bin/c++" >> ~/.bash_profile
42. [ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" //add this line at the end of bash_profile file and reload it
43. . ~/.bash_profile
44. workon AttendanceFaceEnv
45. pip install dlib
46. deactivate
47. git clone https://github.com/Cubastion/AttendanceFaceRecognition.git
48. chmod 777 AttendanceFaceRecognition -R
49. systemctl status firewalld    // if any firewall active then disable it
50. sudo service firewalld stop
51. cd AttendanceFaceRecognition/
52. workon AttendanceFaceEnv
53. pip install opencv-python
54. pip install -r requirements.txt
55. pip install djangorestframework
56. pip install Django==2.1.*
57. pip install face_recognition
58. pip install requests
59. python manage.py migrate
60. add your IP address in allowed hosts variable in settings.py
61. python manage.py runserver 0.0.0.0:8045

//.........steps for setting tmux session .........

1. tmux ls //for any exisiting tmux sessions
2. tmux new -s "AttendanceFaceSession"
3. tmux attach
4. workon AttendanceFaceEnv
5. cd attendance-app/AttendanceFaceRecognition/
6. python manage.py runserver 0.0.0.0:8045
7. press CTRL + B and D key to dettach from session

