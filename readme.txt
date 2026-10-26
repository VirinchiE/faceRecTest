//......... Installation steps for Redhat Server ..........

1. yum update
2. cvVersion="master"
3. mkdir installation
4. mkdir installation/OpenCV-"$cvVersion"
5. cwd=$(pwd)
6. sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
7. sudo yum -y install epel-release
8. sudo yum -y install git gcc gcc-c++ cmake3
9. sudo yum -y install qt5-qtbase-devel
10. sudo yum install -y python34 python34-devel python34-pip
11. sudo yum install -y python python-devel python-pip
12. sudo yum -y install python-devel numpy python34-numpy
13. sudo yum -y install gtk2-devel
14. sudo rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
15. sudo rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm
16. sudo yum install -y ffmpeg
17. sudo yum install -y ffmpeg-devel
18. sudo yum install -y libpng-devel
19. sudo yum install -y openexr-devel
20. sudo yum install -y libwebp-devel
21. sudo yum -y install libjpeg-turbo-devel
22. sudo yum install -y freeglut-devel mesa-libGL mesa-libGL-devel
23. sudo yum -y install libtiff-devel
24. sudo yum -y install libdc1394-devel --skip-broken
25. sudo yum -y install tbb-devel eigen3-devel
26. sudo yum -y install boost boost-thread boost-devel
27. sudo yum -y install python3-devel
28. sudo pip3 install virtualenv virtualenvwrapper
29. echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
30. echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
  or
31. export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3

//  if virtualenvwrapper.sh is found in /usr/bin then execute line 32 else execute line 33

32. echo "source /usr/bin/virtualenvwrapper.sh" >> ~/.bashrc   
or
33. source /usr/local/bin/virtualenvwrapper.sh
34. mkvirtualenv OpenCV-"$cvVersion"-py3 -p python3
35. workon OpenCV-"$cvVersion"-py3
36. pip install cmake
37. pip install numpy scipy matplotlib scikit-image scikit-learn ipython
38. deactivate
39. wget https://github.com/Kitware/CMake/releases/download/v3.15.2/cmake-3.15.2.tar.gz
40. tar -zxvf cmake-3.15.2.tar.gz
41. cd cmake-3.15.2
42. ./bootstrap
43. make
44. sudo make install
45. cd ..
46. git clone https://github.com/opencv/opencv.git
47. git clone https://github.com/opencv/opencv_contrib.git
48. cd opencv
49. mkdir build
50. cd build
51.  cmake -DWITH_QT=ON -DBUILD_TBB=ON -DWITH_OPENGL=ON -DWITH_TBB=ON -DBUILD_EXAMPLES=OFF -DBUILD_DOCS=OFF -DBUILD_TESTS=OFF -OPENCV_CONTRIB=OFF -DENABLE_PRECOMPILED_HEADERS=OFF -DOPENCV_GENERATE_PKGCONFIG=ON -DCMAKE_PREFIX_PATH=/Applications/Qt/5.12.3/clang_64/ ..
52. make
53. sudo make install
54. cd ../..
55. echo "export LC_ALL=en_US.UTF-8" >> ~/.bash_profile
56. echo "export CC=/usr/bin/gcc" >> ~/.bash_profile
57. echo "export CPP=/usr/bin/cpp" >> ~/.bash_profile
58. echo "export CXX=/usr/bin/c++" >> ~/.bash_profile
59. workon OpenCV-master-py3
60. pip install dlib
61. deactivate
62. sudo yum -y groupinstall "Development Tools"
63. git clone https://github.com/Cubastion/AttendanceFaceRecognition.git
64. chmod 777 AttendanceFaceRecognition -R
65. systemctl status firewalld    // if any firewall active then disable it
66. sudo service firewalld stop
67. cd AttendanceFaceRecognition/
68. workon OpenCV-master-py3
69. pip install opencv-python
70. pip install -r requirements.txt
71. pip install Django==2.1.*
72. python manage.py makemigrations
73. python manage.py migrate
74. cd m1cr0face/
75. add your IP address in allowed hosts variable in settings.py
76. cd ..
77. python manage.py runserver 0.0.0.0:8045
