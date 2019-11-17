<?php 
    if(isset($_POST['generateButton'])){ 

        $fileName = $_POST["fileName"];

        $command = escapeshellcmd('python3 ./clipper.py '.$fileName);
        $output = shell_exec($command);

        $dir    = 'res/output';
        $clips = array_diff(scandir($dir), array('..', '.'));
        foreach ($clips as $clip) {
            echo '<div class="clips" data-url="'.$clip.'"></div>';
        }

    }
?>


<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">



        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
     
        <link href="https://vjs.zencdn.net/7.5.5/video-js.css" rel="stylesheet" />
        <script src="https://vjs.zencdn.net/7.5.5/video.js"></script>

        <link rel="stylesheet" href="assets/style.css">

    </head>
    <body>

        <div class="container">
            <div class="row text-center">
                <h1>Highlights Generator</h1>

                <form action="" method="post" enctype="multipart/form-data">
                    <br><br>
                    File name : <input type="text" class="form-control" id="fileName" name="fileName">
                    <br>
                    <button class="btn btn-primary" id="generateButton" name="generateButton">Generate <i class="fa fa-film"></i></button>
                </form>

                <img src="img/loader.gif" id="loader">
            
            </div>  

        </div>

            <div class="row player-container" style="margin-left:250px;">

            </div>  
            


        <script>
            $('#generateButton').click(function(){
                $('#loader').show();
            });

            $( ".clips" ).each(function( index ) {

                var url = $(this).attr("data-url");
                var div = document.createElement('div');
                div.innerHTML = `
                    <div class="playersBlock">
                          <video
                            id="my-video2"
                            class="video-js"
                            controls
                            preload="auto"
                            poster="MY_VIDEO_POSTER.jpg"
                            data-setup="{}"
                          >
                            <source src="res/output/`+url+`" type="video/mp4" />
                          </video>
                    </div>
                    <div>
                        <a href="res/output/`+url+`" class="btn btn-success downloadBtn" download>Download <i class="fa fa-download"></i> </a>
                    </div>
                    
                `;
                $('.player-container').append(div);

            });


        </script>
    </body>

</html>


