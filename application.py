import re
from flask import Flask,session,request,render_template,send_file,redirect
import os
from PyPDF2 import PdfFileReader,PdfFileMerger,PdfFileWriter
from werkzeug.utils import redirect


application = Flask(__name__)
application.secret_key='pass'

@application.route('/')
def home():
    return render_template('home.html')

@application.route('/split',methods=['GET','POST'])
def upload():
    if request.method=="POST":
        file_content = request.files['file']
        session['filename'] = file_content.filename
        a = request.files['file'].filename[-1:-5:-1]
        extension_file = a[::-1]
        if extension_file==".pdf":
            frompage = int(request.form['from'])
            topage = int(request.form['to'])
            PDF_content = PdfFileReader(file_content)
        
            new_pdf = PdfFileWriter()
            os.path.join('files')
            if frompage>0 and topage>0 and topage<=PDF_content.getNumPages() and frompage <= topage :
                for data in range(frompage-1,topage):
                    new_pdf.addPage(PDF_content.getPage(data))

                with open('split.pdf','wb') as split:
                    new_pdf.write(split)    
                return render_template('download.html')
        
            elif topage > PDF_content.getNumPages() or frompage > PDF_content.getNumPages():
                message = "Number of Pages in this PDF is {} !".format(PDF_content.getNumPages())
                return render_template('index.html',message=message)

            elif frompage > topage:
                message = "From Page must be less than To Page "
                return render_template('index.html',message=message)
        
            else:
                message = "Page number Cannot be 0/Negative/Blank"
                return render_template('index.html',message=message)
        else:
            message = "Uploaded File should be in PDF Format !"
            return render_template('index.html',message=message)
    else:
        return render_template('index.html')

@application.route('/download',methods=["GET","POST"])
def download():
    if request.method=="POST":
        file_name = "split_" + session.get('filename') 
        return send_file('split.pdf',as_attachment=True,download_name=file_name)
           
    else:
        return redirect('/upload')



@application.route('/merge',methods=["GET","POST"])
def merge():
    if request.method=="POST":

        merger = PdfFileMerger()
        file1 = request.files['file1']
        file2 = request.files['file2']
        a = file1.filename[-1:-5:-1]
        b = file2.filename[-1:-5:-1]
        extension_file1 = a[::-1]
        extension_file2 = b[::-1]
        if extension_file1 == ".pdf" and extension_file2==".pdf":
            pdf1_content = PdfFileReader(file1)
            pdf2_content = PdfFileReader(file2)
            merger.append(pdf1_content)
            merger.append(pdf2_content)
            with open('merged.pdf','wb') as merged:
                merger.write(merged)
            session['mergefilename'] = file1.filename + file2.filename
            return render_template('download_merged.html')
        else:
            message = "Uploaded File should be in PDF Format !"
            return render_template('merge.html',message=message)
    else:
        return render_template('merge.html')

@application.route('/merged',methods=["GET","POST"])
def merged():
    if request.method=="POST":
        filename = session['mergefilename']
        return send_file('merged.pdf',as_attachment=True,download_name="MergedPDF.pdf")
    else:
        return redirect('/uploadfiles')


if __name__ =='__main__':
    application.run(debug=True)


