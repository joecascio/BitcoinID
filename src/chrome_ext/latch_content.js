
chrome.extension.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.msg_type == 'request_latch_url')
        {
            var resp = { "latch_url":"" };
            //window.alert("in content script");
            var latch = document.getElementById("latch_login");
            //window.alert("getElementById did not throw");
            if (latch != null)
            {
                resp.latch_url = latch.getAttribute("href");
            }
            else
            {
                resp.latch_url = "";
            }
            sendResponse(resp);            
        }

    });

