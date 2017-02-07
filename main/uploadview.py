from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse,Http404
import hashlib
import re


def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

@csrf_protect
def upload_image(request):
    if request.method == 'POST':
        callback = request.GET.get('CKEditorFuncNum')
        try:
            path = "upload/ckeditor/"
            f = request.FILES["upload"]
            name = md5(f.name.encode('utf-8'))
            try:
                filetype = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', f.name)[0]
            except:
                filetype=""
            file_name = path + name + filetype
            print (file_name)
            des_origin_f = open(file_name, "wb+")
            for chunk in f:
                des_origin_f.write(chunk)
            des_origin_f.close()
        except Exception as e:
            print (e)
        res = r"<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+file_name+"', '');</script>"
        return HttpResponse(res)
    else:
        raise Http404()
