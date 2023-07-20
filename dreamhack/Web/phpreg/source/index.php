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
        <h4>Step 1 : Open the door & Go to Step 2 !!</h4>
        <div class="door"><div class="door_cir"></div></div>
        <p>
          <form method="post" action="/step2.php">
              <input type="text" placeholder="Nickname" name="input1">
              <input type="text" placeholder="Password" name="input2">
              <input type="submit" value="제출">
          </form>
        </p>
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
      .door { 
        position: relative;
        margin: 20px 0px;
        width: 140px;
        height: 180px;
        background-color: #b9abf7;
        border-radius: 10px;
      }
      .door_cir{
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