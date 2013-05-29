var hasLatch = false;
var latch = {
    
      
  requestLatch : function(latch_url) {
      var req = new XMLHttpRequest();
      req.open("GET", "http://localhost:9000/ids_at_site/" + latch_url, true);
      req.onload = this.showLatchResponse_.bind(this);
      req.send();
  },
  
  showLatchResponse_: function (e) {
      var zr = e.target.responseText;
      var id_list = document.getElementById('ids_at_site');
      id_list.innerHTML = zr;
      
  }
};

document.addEventListener('DOMContentLoaded', function () {
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs)
    {
        if (tabs.length > 0)
        {
            chrome.tabs.sendMessage(tabs[0].id, {msg_type: "request_latch_url"}, function(response) 
            {
                if (response.latch_url.length > 0)
                {
                    // call the latch server
                    latch.requestLatch(response.latch_url);
                }
            });
            
        }
        
    });
});
