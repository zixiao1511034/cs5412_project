<?php 
echo "Welcom";
?>
<!-- <?php
$servername = "localhost";
$username = "root";
$password = "xusiquan1997";

// Create connection
$conn = mysqli_connect($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";
?>  -->
<?php
$servername = "127.0.0.1";
$username = "root";
$password = "xusiquan1997";
$dbname = "cowid";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
$url = "http2";
$id = "cow 2";
if(isset($_GET['url'])){
	$url  = $_GET['url'];
}
if(isset($_GET['id'])){
	$id = $_GET['id'];
}
// $sql = "INSERT INTO cowresults (Cowurl, Cowid)
// VALUES ( ".$_GET['url'].",".$_GET['id']." )";
$sql = "INSERT INTO cowresults (Cowurl, Cowid)
VALUES ('".$url."','".$id."')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
  } else {
    echo "Error: " . $sql . "<br>" . $conn->error;
  }
  
  $conn->close();