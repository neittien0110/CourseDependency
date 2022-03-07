# Course Dependency

## Overview

A website and webapi show the dependency tree of courses, help students choose which course need to be accomplished early and arrange their learning plan.

## Structure of the Source Folder

```dos
│   Readme.docx            
│   README.md
│
├───api                     (simple web server)
│       index.js                
│
└───viz                     
    │   chromedriver.exe
    │   Course.csv
    │   CourseListdata.csv
    │   CourseListdataextend.csv
    │   crawldata.py
    │   DK.txt
    │   example.dot
    │   fdpclust.gv
    │   fdpclust.gv.pdf
    │   firebase.py
    │   graphcourse.py
    │   graphcoursemoredetail.py
    │   graphcourseupdate.py
    │   Hello.py
    │   IT3070
    │   main.py
    │   siscourse-firebase-adminsdk-rghqn-2861cb8a24.json
    │   test.py
    │   Untitled.ipynb
    │   viz.zip
    │
    ├───.idea
    │   │   .gitignore
    │   │   aws.xml
    │   │   misc.xml
    │   │   modules.xml
    │   │   viz.iml
    │   │
    │   └───inspectionProfiles
    │           profiles_settings.xml
    │
    ├───dotsource
    │       coursesBEE3110
    │       coursesBEE3110.png
    │       coursesBF2011
    │       coursesBF2011.png
    │       .......................

```

* Thư mục **api** chứa code web server 
* Thư mục viz chứa code crawl data , dữ liệu được crawl và dữ liệu đã phân tích và render bằng graphviz
* API test:
* http://sinno.soict.ai:37080/CH4040 (http://sinno.soict.ai:37080/{courseid})
* http://sinno.soict.ai:37080/simple/CH4040 (http://sinno.soict.ai:37080/simple/courses{courseid}.png)
* Graphviz:( bỏ đuôi .png trên các kết quả trả về)
* http://sinno.soict.ai:37080/dotsourcemoredetail/coursesCH4040 (http://sinno.soict.ai:37080/dotsourcemoredetail/courses{courseid})
* http://sinno.soict.ai:37080/dotsource/coursesCH4040 (http://sinno.soict.ai:37080/dotsource/courses{courseid})
