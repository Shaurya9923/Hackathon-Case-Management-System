/* <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script> */
require("https://code.jquery.com/ui/1.12.1/jquery-ui.js");
require("https://code.jquery.com/jquery-1.12.4.js");
require("//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css");

import { hello } from './module.js';
let val = hello();  // val is "Hello";

$( function() {
          $( "#lawyername" ).autocomplete({
            source: ['hi','hello']
          });
        } );

{/* $.import_js('/path_to_project/scripts/somefunctions.js');        
require("/scripts/subscript.js"); */}