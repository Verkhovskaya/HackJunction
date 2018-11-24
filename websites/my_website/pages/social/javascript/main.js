window.onload = function()
{
    load_stalkees();
    load_stalkers();
    load_my_posts();
}



function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function load_stalkees() {
    document.getElementById("stalkees_div").innerText = httpGet('/stalkees').toString();
}

function load_stalkers() {
    document.getElementById("stalkers_div").innerText = httpGet('/stalkers').toString();
}

function load_my_posts() {
    let my_posts_list = JSON.parse(httpGet('/my_posts'));
    console.log(my_posts_list);
    let posts_div = document.getElementById("my_posts_div");
    for (let i=0; i<my_posts_list.length; i++) {
        let post_div = document.createElement('div');
        let post_p = document.createElement('p');
        let post_text = document.createTextNode(httpGet('/get_text/' + my_posts_list[i]));
        let post_img = document.createElement('img');
        post_img.src = '/get_img/' + my_posts_list[i];
        post_p.appendChild(post_text);
        post_div.appendChild(post_p);
        posts_div.appendChild(post_div);
        posts_div.appendChild(post_img);
        let delete_button = document.createElement('a');
        delete_button.appendChild(document.createTextNode("delete"));
        delete_button.href = '/delete_post/' + my_posts_list[i];
        posts_div.appendChild(delete_button);
    }
}


function load_friends_post() {
    let my_posts_list = JSON.parse(httpGet('/my_posts'));
    console.log(my_posts_list);
    let posts_div = document.getElementById("my_posts_div");
    for (let i=0; i<my_posts_list.length; i++) {
        let post_div = document.createElement('div');
        let post_p = document.createElement('p');
        let post_text = document.createTextNode(httpGet('/get_text/' + my_posts_list[i]));
        let post_img = document.createElement('img');
        post_img.src = '/get_img/' + my_posts_list[i];
        post_p.appendChild(post_text);
        post_div.appendChild(post_p);
        posts_div.appendChild(post_div);
        posts_div.appendChild(post_img);
        let delete_button = document.createElement('a');
        delete_button.appendChild(document.createTextNode("delete"));
        delete_button.href = '/delete_post/' + my_posts_list[i];
        posts_div.appendChild(delete_button);
    }
}
