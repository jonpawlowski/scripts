<html>
<head>
  <title>Customer Database</title>
</head>
<body>
  <h1>Customer Database Application</h1>
  <table border=1 bordercolor=black cellpadding=5 cellspacing=0>
    <th>Rank</th><th>Name</th><th>Universe</th><th>Revenue</th>
<?php
$servername = "192.168.20.201";
$username = "root";
$password = "ChangeMe";
$dbname = "customers";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
//echo "Connected successfully";
//echo "Good job!";
$sql = "SELECT * FROM info";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  //output data to table
  while($row = $result->fetch_assoc()) {
    echo "<tr><td>{$row['Rank']}</td><td>{$row['Name']}</td><td>{$row['Territory']}</td><td>{$row['Revenue']}</td></tr>";
    //echo "<td>{$row['Name']}</td><td>{$row['Territory']}</td><td>{$row['Revenue']}</td></tr>";
  }
}

$conn->close();
?>

  </table>
  </body>
</html>
