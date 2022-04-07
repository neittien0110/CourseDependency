# Course Dependency

## Overview

A website and webapi show the dependency tree of courses, help students choose which course need to be accomplished early and arrange their learning plan.

## How to run

- Step 1: crawling. It takes about 120 minutes.

```dos
    python ./crawldata.py
    Output:../assets/CourseListdata.csv and,
           ../assets/CourseListdataextend.csv
```

- Step 2: generate dependency graphs

- Step 3: run web api

```dos
      nodejs ./index.js
```

## Structure of the Source Folder

```dos
|   Readme.docx
|   README.md                       (guideline)
|       
├───api
|   |   index.js                    (simple web server)
|   |   package-lock.json
|   |   package.json
|   |   
|               
├───assets
|       CourseListdata - Copy.csv
|       CourseListdata.csv
|       
├───dotsourcemoredetail
|       HE3011
|       HE3011.png
|       IT3030
|       IT3030.png
|       
├───viz
|   |   crawldata.py
|   |   Digraph.gv
|   |   Digraph.gv.png
|   |   example.dot
|   |   gentree.py
|   |   graphcoursemoredetail.py
|   |   requirements.txt
|   |   try.py
|   |   Untitled.ipynb
|   |   
|   ├───.idea
|   |   |   .gitignore
|   |   |   aws.xml
|   |   |   misc.xml
|   |   |   modules.xml
|   |   |   viz.iml
|   |   |   
|   |   ÀÄÄÄinspectionProfiles
|   |           profiles_settings.xml
|   |           
|   ├───.ipynb_checkpoints
|   |       Untitled-checkpoint.ipynb
|   |       
|   ├───BrowserDrivers
|   |       chromedriver.exe
|   |       geckodriver.exe
|   |       msedgedriver.exe
|   |       
|   ├───dotsourcemoredetail
|   |       BF2010
|   |       BF2010.png
|   |       BF2410
|   |       
|   ├───templates
|   |       course.html
|   |       picture.html
|   |       

```

* Thư mục **api** chứa code web server 
* Thư mục **viz** chứa code crawl data , dữ liệu được crawl và dữ liệu đã phân tích và render bằng graphviz
* API test:
* http://sinno.soict.ai:37080/CH4040 (http://sinno.soict.ai:37080/{courseid})
* http://sinno.soict.ai:37080/simple/CH4040 (http://sinno.soict.ai:37080/simple/courses{courseid}.png)
* Graphviz:( bỏ đuôi .png trên các kết quả trả về)
* http://sinno.soict.ai:37080/dotsourcemoredetail/coursesCH4040 (http://sinno.soict.ai:37080/dotsourcemoredetail/courses{courseid})
* http://sinno.soict.ai:37080/dotsource/coursesCH4040 (http://sinno.soict.ai:37080/dotsource/courses{courseid})
