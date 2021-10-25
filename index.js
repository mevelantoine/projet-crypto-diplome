"use strict";
const express = require("express");
const bodyParser = require("body-parser");
const { timeStamp } = require("console");

const appExpress = express();

appExpress.get("/token",function (req,res) {
  console.log("token")
  var currentDate = new Date();
  var timestamp = currentDate.getTime()

  var token = Math.floor(timestamp / 30)

  res.send(token.toString())
});

appExpress.get("/verify",function (req,res) {
  var i;
  var isFound;
  console.log("verify")
  	for(i=0;i<hashes.length;i++){
	  if (req.query.hash == hashes[i]){
			isFound=True 
			res.sendStatus(200);
		}
	}

  if (isFound) {
    console.log("oui");
    res.sendStatus(200)
  }
  else{
	  console.log("non");
	  res.sendStatus(403);
  }
});

appExpress.listen(80);
console.log("Server listening on port 80");
