import os

program_path = os.getcwd()
if "/root" in program_path:
    root_path = "/root/my_website"
    page_path = os.path.dirname(os.path.abspath(__file__))
else:
    root_path = "/".join(program_path.split("/")[:-2])
    page_path = program_path



def meta_header(request, override=None):
    print("META HEADER")
    domain = request.get_header('host')
    text = """
<nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #373737;">
  <a class="navbar-brand" href="#">MyWeb</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
    """
    pages = sorted(os.listdir(root_path + '/pages/'))
    if not request.get_cookie('notes') and override != "notes":
        pages.pop(pages.index('notes'))
    if not request.get_cookie('social') and override != "social":
        pages.pop(pages.index('social'))

    for page_name in pages:
        if page_name[0] != ".":
            text += '<li class="nav-item">\n'
            text += '<a class="nav-link" href="http://' + domain + '/' + page_name + '">' + page_name + '</a>\n'
            text += '</li>'
    text += "</div> </nav> "
    return text