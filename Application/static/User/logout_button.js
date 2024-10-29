async function logout()
{
    var info = document.getElementById("Info");
    info.innerHTML = "Logging out";

    var button = document.getElementById("Logout");
    button.disabled = true;

    var response = await fetch("/logout");

    response.json().then((response)=>{
        if (response.message == "Successful")
        {
            info.innerHTML = "Logged out";
            
            window.setTimeout(()=>{window.location.href = response.redirect;}, 1000);
        }
        else
        {
            info.innerHTML = "Error occured";
        }
    });

    
}