async function logout()
{
    console.log("CLICKED!");

    response = await fetch("/logout");
    console.log(response.json());
}