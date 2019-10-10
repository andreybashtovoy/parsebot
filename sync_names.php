<?php

$fp = fopen('names.json', "w+");
fwrite($fp, $_REQUEST['data']);
fclose($fp);

?>