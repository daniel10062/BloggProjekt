var all_checkbox = document.getElementsByClassName("checkbox");


for (checkbox of all_checkbox) {
/*  console.log(tile); */
  checkbox.addEventListener("click", function( event ){
    console.log('Clicking on #' + event.target.dataset.itemId);
    var checkbox_value = document.getElementById("checkbox-" + event.target.dataset.itemId);
    console.log(checkbox_value.checked);
    var url = '/update';

    var request = new XMLHttpRequest();
    request.open('POST', url);
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        // Success!
        //var data = JSON.parse(request.responseText);
        console.log(request.responseText);

        // id = "item-" + event.target.dataset.itemId;
        // console.log('Handling id: ' + id);
        // package = document.getElementById(id);

        if (checkbox_value.checked === true) {
          responseData = JSON.parse(request.responseText);
          if (responseData.status == 'ok') {
            document.getElementById('item-' + responseData.itemId).remove();
          }
        }
      } else {
        // We reached our target server, but it returned an error (400, 500)
        console.log('Error...');
      }
    };

    request.onerror = function() {
      // There was a connection error of some sort
    };

    request.send(JSON.stringify({itemId: event.target.dataset.itemId}));
    /* request.send(JSON.stringify({itemDone: checkbox_value.checked}));
    */
  }, false);
}
