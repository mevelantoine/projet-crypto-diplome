"use strict";
const express = require("express");
const bodyParser = require("body-parser");
const { timeStamp } = require("console");
const crypto = require("crypto");
const base32 = require("hi-base32");
const { type } = require("os");

function generateSecret(length = 20) {
  const randomBuffer = crypto.randomBytes(length);
  return base32.encode(randomBuffer).replace(/=/g, "");
}

function generateHOTP(secret, counter) {
  const decodedSecret = base32.decode.asBytes(secret);
  const buffer = Buffer.alloc(8);
  for (let i = 0; i < 8; i++) {
    buffer[7 - i] = counter & 0xff;
    counter = counter >> 8;
  }

  // Step 1: Generate an HMAC-SHA-1 value
  const hmac = crypto.createHmac("sha1", Buffer.from(decodedSecret));
  hmac.update(buffer);
  const hmacResult = hmac.digest();

  // Step 2: Generate a 4-byte string (Dynamic Truncation)
  const code = dynamicTruncationFn(hmacResult);

  // Step 3: Compute an HOTP value
  return code % 10 ** 6;
}

function generateTOTP(secret, window = 0) {
  const counter = Math.floor(Date.now() / 30000);
  return generateHOTP(secret, counter + window);
}

function verifyTOTP(token, secret, window = 1) {
  if (Math.abs(+window) > 10) {
    console.error("Window size is too large");
    return false;
  }

  for (let errorWindow = -window; errorWindow <= +window; errorWindow++) {
    const totp = generateTOTP(secret, errorWindow);
    console.log(totp)
    if (token == totp) {
      return true;
    }
  }

  return false;
}

function dynamicTruncationFn(hmacValue) {
  const offset = hmacValue[hmacValue.length - 1] & 0xf;

  return (
    ((hmacValue[offset] & 0x7f) << 24) |
    ((hmacValue[offset + 1] & 0xff) << 16) |
    ((hmacValue[offset + 2] & 0xff) << 8) |
    (hmacValue[offset + 3] & 0xff)
  );
}

const appExpress = express();

const secret = generateSecret();
const window = 4;

appExpress.get("/token", function (req, res) {
  console.log("token");
  var currentDate = new Date();

  var token = generateTOTP(secret, window);

  res.send("<!DOCTYPE html>\
    <html>\
    <head>\
    <title>OTP</title>\
    <style>\
    h1 {\
        text-align: center;\
        font-size: 75px;\
        color: white;\
        background-color: grey\
    }\
    </style>\
    </head>\
    <body>\
    \
    <h1>Votre OTP est : "+token.toString()+"</h1>\
    \
    </body>\
    </html>");
});

appExpress.get("/verify", function (req, res) {
  console.log("verify");
  console.log(req.query.otp)
  if (verifyTOTP(req.query.otp,secret,window)){
    res.sendStatus(200)
  }
  else{
    res.sendStatus(403)
  }
});

appExpress.listen(80);
console.log("Server listening on port 80");
