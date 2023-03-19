var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : '10.10.21.52',
  user     : 'root',
  password : '123',
  database : 'joinerp_user'
});
 
connection.connect();
 
connection.query('SELECT * FROM user LIMIT 1000;', function (error, results, fields) {
  if (error) throw error;
  console.log('The solution is: ', results[0].solution);
});