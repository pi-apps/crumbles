
Pi.init({ version: "2.0", sandbox: true });
$(document).ready(function () {
    const Pi = window.Pi;

    function sendUserInfo(username, userroles) {
        const http = new XMLHttpRequest();
        http.open('POST', '/');
        http.setRequestHeader('Content-type', 'application/json');
        params = {
            user_name: username,
            user_roles: userroles
        };
        http.send(JSON.stringify(params)) // Make sure to stringify
        http.onload = function () {
            // Do whatever with response
            console.log("Sending data to python!")
        }
    }


    async function auth() {
        try {
            const scopes = ['username', 'payments', 'roles'];
            function onIncompletePaymentFound(payment) { };

            console.log("Scopes loaded, starting Pi.authenticate.")
            Pi.authenticate(scopes, onIncompletePaymentFound).then(function (auth) {
                result_username = auth.user.username;
                roles = auth.user.roles;
                console.log('Found username = ' + auth.user.username);
                console.log('Found roles = ' + auth.user.roles);
		
                $('#found_username').text(result_username);
                $('#all_roles').text(roles)
                if (roles[0] === "core_team") {
                    $('#found_role').text("Core_Team");
                }
                if (roles[0] === "mega_mod") {
                    $('#found_role').text("MegaMod");
                }
                if (roles[0] === "moderator") {
                    $('#found_role').text("Moderator");
                }

                //sendUserInfo(auth.user.username, auth.user.roles);


            }).catch(function (error) {
                console.log("An error occured. Pi.authenticate(scopes, onIncompletePaymentFound)... doesn't work.")
                console.error(error)
            });
        } catch (err) {
            console.log("An error during the try/catch-routine of auth() occured");
        }
    }
    const shareData = {
        title: 'Chat 2.0 Test',
        text: 'Testing the authentication-workflow.'
    }
    console.log("sending data to openShareDialog")
    Pi.openShareDialog(shareData.title, shareData.text);

    auth()

});
