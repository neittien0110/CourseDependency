// API
var express = require('express');
var mysql = require('mysql');
//connect to MySQL
var connect = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'',
    database:'siscourse'
});

//Create API

var app=express();
var publicDir=(__dirname+'/public/');
app.use(express.static(publicDir));
app.use(express.json());


//Get image by Course name

app.get("/course/:courseid",(req,res,next)=>{
    connect.query('SELECT Link FROM course where Coursename=?',[req.params.courseid],function(err,result,fields){
        connect.on('error',function(err){
                console.log('SQL ERROR',err);
        });
        if(result && result.length)
        {   var a=JSON.parse(JSON.stringify(result))
            console.log(a[0].Link);
            res.redirect(a[0].Link);
        }
        else
        {
            res.end(JSON.stringify("Khong tim thay"))
        }
    });
});

//Start Server
app.listen(3000,()=>{
    console.log('Server is running on port 3000');
});