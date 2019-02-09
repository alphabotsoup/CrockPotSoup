/**
 * exports of mysql module
 * @type {Object}
 */
var mysql = require('mysql');

/**
 * exports of express module
 * @type {Object}
 */
var express = require('express');

/**
 * express router for frontend/backend interaction
 * @type {Function}
 */
var router = express.Router();

let connection = mysql.createConnection({
  host: "mariadb-mariadb",
  user: "root",
  password: "X7tM5FvGm6",
  database: "mysql"
});

/**
 * exports of connection definition file
 * @type {Object}
 */
//let conn_info = require('./connection.js');

/**
 * contains the mysql connection information
 * @type {Object}
 */
//let connection = conn_info.connection;

/**
 * route for rendering dbTesting page
 */
router.get('/', function(req, res) {
  res.render('dbTest');
});

/**
 * route for checking if user is logged in
 * @alias GET_testConnection
 */
router.get('/testConnection', function(req, res) {
    console.log("Route Started");
  connection.connect(function(err) {
    if (err) throw err;
    console.log("Connected!");
  });
});

module.exports = router;
