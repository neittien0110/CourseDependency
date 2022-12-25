# Course Dependency

## Overview

A website and webapi show the dependency tree of courses, help students choose which course need to be accomplished early and arrange their learning plan.

## How to run

- Step 1: crawling. It takes about 120 minutes.

```dos
    cd viz
    python ./crawl_personalsis.py
    Output:../assets/CourseListdata.csv and,
           ../assets/CourseListdataextend.csv
```

- Step 2: generate dependency graphs

```dos
      python ./gentree.py
```

- Step 3: run web api

```dos
      nodejs ./index.js
```

## Other features

- Generate the condition tree of a single subject

```dos
    python ./gentree.py -s subject
    python ./gentree.py -s IT1110
```

- Generate the condition tree of a single subject and force a trial condition expression

```dos
    python ./gentree.py -s subject -c condition
    python ./gentree.py -s IT3030 -c "(IT111/IT1120/IT1130),IT2000"
```

- Generate the condition tree of a group of subjects, like a education programme

```dos
    python ./gentree.py -n name -p subjectInCSV
    python ./gentree.py -n IT1  -p  IT2030,IT4991,IT3420,IT3020
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
|   |   CourseListdata.csv           (crawling results)
|   |    
|   ├───graph0
|   |       HE3011
|   |       HE3011.png
|   |       IT3030
|   |       IT3030.png
|       
├───viz
|   |   crawl_personalsis.py        (crawling program)
|   |   example.dot
|   |   gentree.py                  (crawling results to graph) 
|   |   graphcoursemoredetail.py    (not in used)
|   |   requirements.txt
|   |   Untitled.ipynb
|   |   
|   ├───BrowserDrivers
|   |       chromedriver.exe
|   |       geckodriver.exe
|   |       msedgedriver.exe
|   |       
```

* Thư mục **api** chứa code web server 
* Thư mục **viz** chứa code crawl data , dữ liệu được crawl và dữ liệu đã phân tích và render bằng graphviz

## Demo

- Xem ảnh vẽ mối quan hệ phụ thuộc của 1 học phần nào đó: **<span>http</span>://sinno.soict.ai:37080/course?id={courseid}**
  - http://sinno.soict.ai:37080/course?id=ch4040 
  - http://sinno.soict.ai:37080/course?id=it3030 
- Xem mối quan hệ phụ thuộc của 1 học phần nào đó ở dạng json, phù hợp để tích hợp vào một GUI control trên website khác: **<span>http</span>://sinno.soict.ai:37080/course?id={courseid}&type=json**
  - http://sinno.soict.ai:37080/course?id=it1110&type=json
- Xem mối quan hệ phụ thuộc của 1 học phần nào đó ở các dạng đồ thị khác nhau: **<span>http</span>://sinno.soict.ai:37080/course?id={courseid}&graph={index}**
  - http://sinno.soict.ai:37080/course?id=it3030&graph=0 
  - http://sinno.soict.ai:37080/course?id=it3030&graph=1 