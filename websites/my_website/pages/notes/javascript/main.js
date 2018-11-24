window.onload = function() {
  var te_markdown = document.getElementById("code-markdown");

  window.editor_markdown = CodeMirror.fromTextArea(te_markdown, {
    mode: "markdown",
    lineNumbers: true,
    lineWrapping: true,
    extraKeys: {"Ctrl-Q": function(cm){ cm.foldCode(cm.getCursor()); }},
    foldGutter: true,
    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"]
  });
};
