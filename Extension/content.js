chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
      console.log("Shit");
      console.log(request.greeting);
    sendResponse({farewell: "Done"});
});
