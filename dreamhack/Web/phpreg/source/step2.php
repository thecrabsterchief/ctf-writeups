<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
<title>PHPreg</title>
</head>
<body>
  <!-- Fixed navbar -->
  <nav class="navbar navbar-default navbar-fixed-top">
    <div class="container">
      <div class="navbar-header">
        <a class="navbar-brand" href="/">PHPreg</a>
      </div>
      <div id="navbar">
        <ul class="nav navbar-nav">
          <li><a href="/">Step 1</a></li>
          <li><a href="/step2.php">Step 2</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </nav><br/><br/><br/>
  <div class="container">
    <div class="box">
      <!-- PHP code -->
      <?php
          // POST request
          if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $input_name = $_POST["input1"] ? $_POST["input1"] : "";
            $input_pw = $_POST["input2"] ? $_POST["input2"] : "";

            // pw filtering
            if (preg_match("/[a-zA-Z]/", $input_pw)) {
              echo "alphabet in the pw :(";
            }
            else{
              $name = preg_replace("/nyang/i", "", $input_name);
              $pw = preg_replace("/\d*\@\d{2,3}(31)+[^0-8]\!/", "d4y0r50ng", $input_pw);

              if ($name === "dnyang0310" && $pw === "d4y0r50ng+1+13") {
                echo '<h4>Step 2 : Almost done...</h4><div class="door_box"><div class="door_black"></div><div class="door"><div class="door_cir"></div></div></div>';

                $cmd = $_POST["cmd"] ? $_POST["cmd"] : "";

                if ($cmd === "") {
                  echo '
                        <p><form method="post" action="/step2.php">
                            <input type="hidden" name="input1" value="'.$input_name.'">
                            <input type="hidden" name="input2" value="'.$input_pw.'">
                            <input type="text" placeholder="Command" name="cmd">
                            <input type="submit" value="제출"><br/><br/>
                        </form></p>
                  ';
                }
                // cmd filtering
                else if (preg_match("/flag/i", $cmd)) {
                  echo "<pre>Error!</pre>";
                }
                else{
                  echo "<pre>--Output--\n";
                  system($cmd);
                  echo "</pre>";
                }
              }
              else{
                echo "Wrong nickname or pw";
              }
            }
          }
          // GET request
          else{
            echo "Not GET request";
          }
      ?>
    </div>
  </div>

  <style type="text/css">
    h4 {
      color: rgb(84, 84, 84);
    }
    .box{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    pre {
      width: 80%;
    }
    .door_box {
      position: relative;
      width: 240px;
      height: 180px;
      margin: 20px 0px;
    }
    .door_black {
      position: absolute;
      width: 140px;
      height: 180px;
      background-color: black;
      border-radius: 10px;
      right:0px;
    }
    .door {
      z-index: 2;
      position: absolute;
      width: 140px;
      height: 180px;
      background-color: #b9abf7;
      border-radius: 10px;
      right: 100px;
    }
    .door_cir{
      z-index: 3;
      position: absolute;
      border-radius: 50%;
      width: 20px;
      height: 20px;
      border: 2px solid rgba(255, 222, 113, 0.873);
      background-color: #ffea98;
      top: calc( 180px / 2 - 10px );
      right: 10px;
    }
  </style>
</body>
</html>
