const { exec, execSync } = require('child_process');  // Gọi tiến trình tạo ảnh dựa trên giả định về mã học phần

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Thư mục chứa kết quả
COURSE_COLLECTION_FOLDER = "../assets"

// API
var express = require('express');

//Create API
var app=express();
var path = require('path');
var fs = require('fs');
var publicDir=(__dirname + COURSE_COLLECTION_FOLDER );
app.use(express.static(publicDir));
app.use(express.json());


//Giới thiệu
app.get("/",(req,res,next)=>{
    res.send("A webapi shows the dependency tree of courses, help students choose which course need to be accomplished early and arrange their learning plan.<br/>"+
              "API: http://&lt;domain&gt;:&lt;port&gt;/course?id=...<br/>" +
              "API: http://&lt;domain&gt;:&lt;port&gt;/course?id=...&type=json<br/>" +
              "API: http://&lt;domain&gt;:&lt;port&gt;/course?id=...&type=png&graph=1<br/>" +
              "API: http://&lt;domain&gt;:&lt;port&gt;/course?id=...&condition=<br/>" +
              "Parameters:<br/>" +
              " - id = &lt;mã học phần&gt; <br/>" +
              " - type = svg | json | png | graphviz <br/>" +
              " - graph = 0 | 1 <br/>" +
              " - condition = &lt;điều kiện HP phụ thuộc thử nghiệm&gt; <br/>" +
              "Symbols:" +
              " - blue node: prerequisite<br/>"+
              " - pink node: dependant course<br/>"+
              " - dot edge: half-dependant course."+
              "");
})

app.get("/course",(req,res,next)=>{
    /** mã học phần, từ tham số HTTP-GET */
    var courseID = NaN
    /** dạng thông tin trả về, từ tham số HTTP-GET */
    var type = NaN; // Kiểu kết quả trả về
    /** Dạng đồ thị trả về, từ tham số HTTP-GET */
    var graph = NaN; // Kiểu kết quả trả về
    /** Giả định về học phần điều kiện */
    var condition = NaN // 

    try {
        courseID = req.query.id.toUpperCase();
        type = req.query.type;
        graph = req.query.graph; 
        condition = req.query.condition;
    } catch {
        res.json({"error":"param is invalid.", 'message': 'the path must has ?id=...&condition=...&graph=...'}); return;
    }
    console.log(type)
    if (type == undefined) {
        type = "svg";
    } else {
        type = type.toLowerCase(); // Kiểu kết quả trả về
    }
    if (graph == undefined) {
        graph = "0";
    } 

    // Xác định thư mục chứa ảnh học phần
    var folder;
    if (condition !=  undefined) {
        folder = "trial"
    } else {
        switch (graph) {
            case "0": folder = "graph0"; break;
            case "1": folder = "graph1"; break;
            case "2": folder = "graph2"; break;
        }
    }

    // Tạo ảnh dựa trên dữ liệu học phần phụ thuộc giả định
    if (condition !=undefined) {
        condition = (String(condition)).replaceAll(" ","").replaceAll("\t","");
        execSync("cd ../viz; python3 ./gentree.py -s " + courseID + " -c " + condition)
        console.log(`HP ${condition} với giả định phụ thuộc  ${condition}`)
    }

    var imagePath = path.resolve(__dirname + `/${COURSE_COLLECTION_FOLDER}/${folder}/${courseID}`)
    if (condition !=undefined) {
        // Hiệu chỉnh tên file nếu có điều kiện học phần giả định.
        // Đồng thời đổi kí tự đặc biệt vì không phù hợp với tên file
        imagePath = imagePath + "." + condition.replaceAll("/","+")
    }
    console.log(imagePath);

    switch (type) {
        case 'json':  { // Chuyển đổi ảnh thành base64
                        var imageAsBase64 = fs.readFileSync(imagePath + ".png", 'base64');
                        res.json({ result: "data:image/png;base64," + imageAsBase64 });
                        break;
                      } 
        case 'png':   { // Gửi file ảnh có sẵn
                        res.sendFile(imagePath + "." + type);
                        break;
                      };  
        case 'svg':   { // Gửi file ảnh có sẵn
                        res.sendFile(imagePath + "." + type);
                        break;
                      };    
        case 'graphviz': { // Gửi file ảnh có sẵn
                        //res.setHeader()
                        res.send(fs.readFileSync(imagePath).toString())
                        break;
                      };                                            
        default: res.json({error:"type is invalid.", 'message':'the ' + type + ' type is not supported. It must be png or json (default).'}); return;
      }
});

//Start Server
app.listen(80,()=>{
    console.log('Server is running on port 80');
});