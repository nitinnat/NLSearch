chrome.runtime.onMessage.addListener(function(message,sender,response){
    if(message.text == "DOM") {
        response(document);
    }
});
