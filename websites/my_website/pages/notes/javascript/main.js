

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function httpPost(theUrl, data) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", theUrl, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(data));
}

window.onload = function() {
  var te_markdown = document.getElementById("code-markdown");
  te_markdown.value = httpGet('/notes/note/' + document.getElementById('note_title').value);

  window.editor_markdown = CodeMirror.fromTextArea(te_markdown, {
    mode: "markdown",
    lineNumbers: true,
    lineWrapping: true,
    extraKeys: {"Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()); }},
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"]
  });

    window.editor_markdown.setSize("100%", "85%");
};

function save() {
  let name = document.getElementById('note_title').value;
  let body = document.getElementById('code-markdown').value;
  httpPost('/notes/save', {'name': name, 'body': body});
  window.location.href = "/notes/open/" + name;
}