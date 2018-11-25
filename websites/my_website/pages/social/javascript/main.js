window.onload = function()
{
    load_stalkees();
    load_stalkers();
    load_my_posts();
    load_friends_post();
}

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function load_stalkees() {
    let stalkees = JSON.parse(httpGet('/social/stalkees'));
    let stalkees_div = document.getElementById("stalkees_div");
    for (let i=0; i<Object.keys(stalkees).length; i++) {
        let key = Object.keys(stalkees)[i];
        let post_div = document.createElement('div');
        stalkees_div.appendChild(post_div)
            let post_p = document.createElement('p');
        if (stalkees[key]['status'] != 'pending') {
            post_div.appendChild(post_p);
            let post_text = document.createTextNode(key);
            post_p.appendChild(post_text);
        } else {
            post_div.appendChild(post_p);
            let post_text = document.createTextNode(key + " (pending)");
            post_p.appendChild(post_text);
        }
            let delete_button = document.createElement('a');
            delete_button.appendChild(document.createTextNode("delete"));
            delete_button.href = '/social/delete_stalkee/' + key;
            post_p.appendChild(delete_button);
    }
    innerText = httpGet('/social/stalkees').toString();
}

function load_stalkers() {
    let stalkers = JSON.parse(httpGet('/social/stalkers'));
    console.log(stalkers);
    let stalkers_div = document.getElementById("stalkers_div");
    let stalkees_div = document.getElementById("stalkees_div");
    for (let i=0; i<Object.keys(stalkers).length; i++) {
        let key = Object.keys(stalkers)[i];
        let post_div = document.createElement('div');
        let post_p = document.createElement('p');
        if (stalkers[key]['status'] != 'pending') {
            post_div.appendChild(post_p);
            let post_text = document.createTextNode(key);
            post_p.appendChild(post_text);
        } else {
            post_div.appendChild(post_p);
            let post_text = document.createTextNode(key + " (pending)");
            post_p.appendChild(post_text);
            let delete_button = document.createElement('a');
            delete_button.appendChild(document.createTextNode("confirm"));
            delete_button.href = '/social/confirm_stalker/' + key;
            delete_button.style.marginLeft = "1em";
            post_p.appendChild(delete_button);
            let br = document.createElement('br');
            post_div.appendChild(br);
        }

        if (stalkers[key]['status'] == 'pending') {
            stalkers_div.appendChild(post_div);
        } else {
            stalkees_div.appendChild(post_div);
        }
            let delete_button = document.createElement('a');
            delete_button.appendChild(document.createTextNode("delete"));
            delete_button.href = '/social/delete_stalker/' + key;
            delete_button.style.marginLeft = "1em";
            post_p.appendChild(delete_button);
    }
}

function load_my_posts() {
    let my_posts_list = JSON.parse(httpGet('/social/my_posts'));
    console.log(my_posts_list);
    let posts_div = document.getElementById("my_posts_div");
    for (let i=0; i<my_posts_list.length; i++) {
        let post_div = document.createElement('div');
        post_div.style.backgroundColor = "#DCD0C0";
        post_div.style.margin = "2em";
        post_div.style.padding = "2em";
        let post_p = document.createElement('h2');
        post_p.style.fontWeight = "200";
        let post_text = document.createTextNode('Me: ' + httpGet('/social/get_text/' + my_posts_list[i]));
        let post_img = document.createElement('img');
        post_img.src = '/social/get_img/' + my_posts_list[i];
        post_img.style.maxWidth = "100%";
        post_p.appendChild(post_text);
        post_div.appendChild(post_p);
        posts_div.appendChild(post_div);
        post_div.appendChild(post_img);
        post_div.appendChild(document.createElement('br'));
        post_div.appendChild(document.createElement('br'));
        let delete_wrapper = document.createElement('a');
        delete_wrapper.href = '/social/delete_post/' + my_posts_list[i];
        let delete_button = document.createElement('button');
        delete_button.class = "btn btn-light";
        delete_button.appendChild(document.createTextNode("delete"));
        delete_button.style.marginLeft = "1em";
        post_div.appendChild(delete_wrapper);
        delete_wrapper.appendChild(delete_button);

        let log_wrapper = document.createElement('a');
        log_wrapper.href = '/social/log/' + my_posts_list[i];
        let log_button = document.createElement('button');
        log_button.class = "btn btn-light";
        log_button.appendChild(document.createTextNode("log"));
        log_wrapper.appendChild(log_button);
        post_div.appendChild(log_wrapper);
        posts_div.appendChild(document.createElement('hr'));
    }
}

function load_friends_post() {
    let friends = JSON.parse(httpGet('/social/stalkees'));
    console.log(Object.keys(friends));
    for (let x = 0; x < Object.keys(friends).length; x++) {
        console.log(Object.keys(friends)[x]);
        let my_posts_list = JSON.parse(httpGet('http://' + Object.keys(friends)[x] + '/social/my_posts'));
        console.log(my_posts_list);
        let key = Object.keys(friends)[x];
        let posts_div = document.getElementById("friends_posts_div");
        if (friends[key]['status'] != 'pending') {
            for (let i = 0; i < my_posts_list.length; i++) {
                let post_div = document.createElement('div');
                post_div.style.backgroundColor = "#DCD0C0";
                post_div.style.margin = "2em";
                post_div.style.padding = "2em";
                let post_p = document.createElement('h2');
                post_p.style.fontWeight = "200";
                let post_text = document.createTextNode(key + ": " + httpGet('http://' + Object.keys(friends)[x] + '/social/get_text/' + my_posts_list[i]));
                let post_img = document.createElement('img');
                post_img.style.maxWidth = "100%";
                post_img.src = 'http://' + Object.keys(friends)[x] + '/social/get_img/' + my_posts_list[i];
                post_p.appendChild(post_text);
                post_div.appendChild(post_p);
                posts_div.appendChild(post_div);
                post_div.appendChild(post_img);
                posts_div.appendChild(document.createElement('hr'));
            }
        }
    }

    load_other();
}

function load_other() {
    let friends = JSON.parse(httpGet('/social/stalkers'));
    console.log(Object.keys(friends));
    for (let x=0; x<Object.keys(friends).length; x++) {
        console.log(Object.keys(friends)[x]);
        let my_posts_list = JSON.parse(httpGet('http://' + Object.keys(friends)[x] + '/social/my_posts'));
        console.log(my_posts_list);
        let key = Object.keys(friends)[x];
        let posts_div = document.getElementById("friends_posts_div");
        if (friends[key]['status'] != 'pending') {
            for (let i=0; i<my_posts_list.length; i++) {
                let post_div = document.createElement('div');
                post_div.style.backgroundColor = "#DCD0C0";
                post_div.style.margin = "2em";
                post_div.style.padding = "2em";
                let post_p = document.createElement('h2');
                post_p.style.fontWeight = "200";
                let post_text = document.createTextNode(key + ": " + httpGet('http://' + Object.keys(friends)[x] + '/social/get_text/' + my_posts_list[i]));
                let post_img = document.createElement('img');
                post_img.style.maxWidth = "100%";
                post_img.src = 'http://' + Object.keys(friends)[x] + '/social/get_img/' + my_posts_list[i];
                post_p.appendChild(post_text);
                post_div.appendChild(post_p);
                posts_div.appendChild(post_div);
                post_div.appendChild(post_img);
                posts_div.appendChild(document.createElement('hr'));
            }
        }
    }
}
