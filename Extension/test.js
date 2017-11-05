function callback(tabs) {
  currentTab = tabs[0].id;
  localStorage.setItem("tab", currentTab);
  console.log(currentTab);
  var background = chrome.extension.getBackgroundPage();


  if (background.prevTab != currentTab) {

      background.prevTab = currentTab;

      function modifyDOM() {
          //You can play with your DOM here or check URL against your regex
          console.log('Tab script:');
          console.log(document.body.innerHTML);
          return document.body.innerHTML;
      }
      //We have permission to access the activeTab, so we can call chrome.tabs.executeScript:
      chrome.tabs.executeScript({
          code: '(' + modifyDOM + ')();' //argument here is a string but function.toString() returns function's code
      }, (results) => {
          //Here we have just the innerHTML and not DOM structure
          console.log('Popup script:')
          document.getElementById('boo').disabled = true;
          var html_parsed = results[0];
          var data = {dump:html_parsed};
          var url = 'http://localhost:3000/senvec/indexing/';
          $.ajax({
              type: 'POST',
              url: url,
              data: JSON.stringify (data),
              success: function(data) {
                  localStorage.setItem("mlvalue", data);
                  someVarName2 = localStorage.getItem("mlvalue");
                  console.log("success");
                  console.log(JSON.stringify(someVarName2));
                  document.getElementById('boo').disabled = false;
              },
              contentType: "application/json",
              dataType: 'json'
          });

          /*
          $http.post(url, data).then(function(response){
              if(response.data){
                  localStorage.setItem("mlvalue", response.data);
                  someVarName2 = localStorage.getItem("mlvalue");
                  console.log("success");
                  console.log(someVarName2);
              } else {
                  console.log("failure");
              }
              $( "#boo" ).toggle();
          });
          */
      });


  }

  document.getElementById("test").addEventListener('click', () => {
    console.log("Popup DOM fully loaded and parsed");
    var input = document.getElementById("boo").value;
    someVarName2 = localStorage.getItem("mlvalue");
    console.log(someVarName2);
    var html = "";
    var data = {dump:html};
    var url = 'http://localhost:3000/ssss';

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify (data),
        success: function(data) {
            localStorage.setItem("mlvalue", response.data);
            someVarName2 = localStorage.getItem("mlvalue");
            console.log("success");
            console.log(someVarName2);
            $( "#boo" ).toggle();
        },
        contentType: "application/json",
        dataType: 'json'
    });
    console.log(input);
  });

}
var query = { active: true, currentWindow: true };

chrome.tabs.query(query, callback);
