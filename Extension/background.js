console.log("Hello World");
console.log("Hello World");
var currentTab = 0;
var prevTab = -1;
/*function send_data(event) {
    chrome.tabs.query({currentWindow:true, active:true}, function(tabs) {
        console.log("print when clicked");
    });
}
*/
function parseDom(domTree) {
    console.log('I received the following DOM content:\n');
}
chrome.browserAction.onClicked.addListener(function(tab) {
    console.log(document.body.innerHTML);
    chrome.tabs.sendMessage(tab.id,{text:'DOM'},parseDom);
});
