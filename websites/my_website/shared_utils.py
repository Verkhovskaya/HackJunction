import os

program_path = os.getcwd()
if "/root" in program_path:
    root_path = "/root"
    page_path = "/root/" + program_path.split("/")[-1]
else:
    root_path = "/".join(program_path.split("/")[:-2])
    page_path = program_path

def meta_header(request):
    print("META HEADER")
    domain = request.get_header('host')
    text = """
<nav class="navbar navbar-expand-lg navbar-light" style="background-color: #e3f2fd;">
  <a class="navbar-brand" href="#">Meta</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
    """
    pages = sorted(os.listdir(root_path + '/pages/'))
    for page_name in pages:
        if page_name[0] != ".":
            text += '<li class="nav-item">\n'
            text += '<a class="nav-link" href="http://' + domain + '/' + page_name + '">' + page_name + '</a>\n'
            text += '</li>'
    text += "</div> </nav> "
    return text