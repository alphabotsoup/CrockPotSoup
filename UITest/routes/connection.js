/**
 * exports of mysql module
 * @type {Object}
 */
var mysql = require('mysql');

/**
 * a mysql connection object
 * @type {Object}
 */
let connection = mysql.createConnection({
  host: "mariadb-mariadb",
  user: "root",
  password: "X7tM5FvGm6",
  database: "mysql"
});

exports.connection = connection;
