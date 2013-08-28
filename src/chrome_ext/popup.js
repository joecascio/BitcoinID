var hasLatch = false;
var latch_url = "";
var challenge = "";
var current_tab = 0;
var current_url = "";

function get_challenge()
{
    var req = new XMLHttpRequest();
    // process synchronously
    req.open("GET", latch_url + "/latch_challenge", false);
    req.send();
    if (req.status == 200)
    {
        return req.responseText;
    }
    else
    {
        return null;
    }
}
  
function login_w_id(e) {
    
    var id = e.currentTarget.getAttribute('id');
    challenge = get_challenge();
    if (challenge == null) {
        
    }
    var req = new XMLHttpRequest();
    req.open("POST", "http://localhost:9000/challenge_response/" + id, false);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    var addendum = new Date().toString();
    var message = challenge + addendum;
    var json = {}
    json.challenge = challenge;
    json.addendum = addendum;
    json.message = message;
    var jsonstr = JSON.stringify(json);
    
    req.send(jsonstr);
    if (req.status != 200)
    {
        error_msg = req.responseText;
        display_svr_response(error_msg);
    }
    auth_data = req.responseText;
    
    // now call the site with the signed message 
    areq = new XMLHttpRequest();
    areq.open("POST", latch_url + "/latch_login/" + id, false);
    areq.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    areq.send(auth_data); // this contains the challenge, addendum, messsage and signature
    if (areq.status != 200) {
        error_msg = areq.responseText;
        display_svr_response(error_msg);
    } else {
        // reload tab. If were not logged in, should show up
        // as logged in now. This call defaults to selected tab of current window
        chrome.tabs.reload();
        window.close();
    }


}

function register_w_id(e)
{
    // var id = e.currentTarget.getAttribute('id');
    // reload the current tab with the local latch server URL to 
    // create a new id at site record
    var url = "http://localhost:9000/register_id/" + "?latch_url=" + latch_url
    chrome.tabs.update(current_tab, {url: url});
    window.close();
    
}

  
// function register_w_id(e) {
//     
//     var id = e.currentTarget.getAttribute('id');
//     challenge = get_challenge();
//     if (challenge == null) {
//         
//     }
//     var req = new XMLHttpRequest();
//     req.open("POST", "http://localhost:9000/challenge_response/" + id, false);
//     req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//     var addendum = new Date().toString();
//     var message = challenge + addendum;
//     var json = {}
//     json.challenge = challenge;
//     json.addendum = addendum;
//     json.message = message;
//     var jsonstr = JSON.stringify(json);
//     
//     req.send(jsonstr);
//     response_text = req.responseText;
//     
//     if (req.status != 200)
//     {
//         error_msg = response_text;
//         display_svr_response(error_msg);
//     }
//     
//     var response_data = JSON.parse(response_text);
//     if (response_data.result == 'error')
//     {
//         display_svr_response(response_data.message)
//     }
//     
//     // the demographic data is always included in the response
//     auth_data = response_text; 
//     
//     // now call the site with the signed message 
//     areq = new XMLHttpRequest();
//     areq.open("POST", latch_url + "/latch_register/" + id, false);
//     areq.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
//     areq.send(auth_data); // this contains the challenge, addendum, messsage and signature
//     if (areq.status != 200) {
//         error_msg = areq.responseText;
//         display_svr_response(error_msg);
//     } else {
//         // reload tab. If were not logged in, should show up
//         // as logged in now. This call defaults to selected tab of current window
//         chrome.tabs.reload();
//         window.close();
//     }
// 
// 
// }
  
function display_svr_response(html) 
{
    var id_list = document.getElementById('svr_reply');
    id_list.innerHTML = html;
}

function showLatchResponse(e) {
    var zr = e.target.responseText;
    display_svr_response(zr);
    
    var login_buttons = document.getElementsByName('login_button');
    for (var i = 0; i < login_buttons.length; i++)
    {
        login_buttons[i].addEventListener('click', login_w_id);
    }        

    var register_buttons = document.getElementsByName('register_button');
    for (var i = 0; i < register_buttons.length; i++)
    {
        register_buttons[i].addEventListener('click', register_w_id);
    }        

}

function requestLatch(latch_url) {
    var req = new XMLHttpRequest();
    req.onload = showLatchResponse;
    req.open("GET", "http://localhost:9000/ids_at_site/" + latch_url, true);
    req.send();
}


document.addEventListener('DOMContentLoaded', function () {

    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs)
    {
        if (tabs.length > 0)
        {
            current_tab = tabs[0].id;
            current_url = tabs[0].url;
            chrome.tabs.sendMessage(tabs[0].id, {msg_type: "request_latch_url"}, function(response) 
            {
                if (response.latch_url.length > 0)
                {
                    latch_url = response.latch_url
                    
                    // call the latch server
                    requestLatch(response.latch_url);
                }
                else
                {
                    display_svr_response("This site does not accept Latch logins or registrations.")
                }
            });
                        
        }
        
    });
    
});
