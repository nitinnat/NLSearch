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
          var html_parsed = results[0];
          localStorage.setItem("mlvalue", html_parsed);
      });


  }
  someVarName2 = localStorage.getItem("mlvalue");
  console.log(someVarName2);

  document.getElementById("test").addEventListener('click', () => {
    console.log("Popup DOM fully loaded and parsed");
    var input = document.getElementById("boo").value;
    console.log(input);
  });

}
var query = { active: true, currentWindow: true };

chrome.tabs.query(query, callback);
