BtcID is a collection of proof-of-concept software for Collateralized Identity. See http://joecascio.net/joecblog/2013/03/25/collateralized-identity-using-bitcoin-to-suppress-sockpuppets/ for a thorough explanation.

There are 4 parts to the prototype.

1. Chrome browser extension that examines the active tab's HTML for a link tag with the id 'latch_login'. This indicates to the extension that the site presents a btcid-compatable api with which the browser can login or register.

2. Local btcid web app. A python-django web app that runs on the user's machine and services requests from the Chrome extension to sign and encrypt messages to the active tab's web site.

3. BtcID application. A Python Qt4 installed app that manages the user's identities and which sites they are used at.

4. A sample web site that accepts btcid logins and registrations. This is a minimal python-django web app that uses collateralized bitcoin IDs as usernames.