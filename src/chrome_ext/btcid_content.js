
chrome.extension.onMessage.addListener(
    function(request, sender, sendResponse) {
        //debugger;
        if (request.msg_type == 'request_btcid_url')
        {
            var resp = { "btcid_url":"" };
            //window.alert("in content script");
            var btcid = document.getElementById("btcid_login");
            //window.alert("getElementById did not throw");
            if (btcid != null)
            {
                resp.btcid_url = btcid.getAttribute("href");
            }
            else
            {
                resp.btcid_url = "";
            }
            sendResponse(resp);            
        }

    });

