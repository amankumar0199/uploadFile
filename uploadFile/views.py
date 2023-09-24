from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import uploadedFile
from .urlShortener import URLShortener
import boto3
import os
from PIL import Image
from io import BytesIO
import uuid


# Create your views here.
def upload(request):
    if request.method== 'POST':        
        s3_client = boto3.client('s3', aws_access_key_id= "AKIA6NISAVJ4JKXH3UO2", aws_secret_access_key="jszTf7SA7cL6vvlsyd8TfjzczNKkJi4MIoikptHD")
        
        img = Image.open(request.FILES.get('myfile'))
        img_byte = BytesIO()
        img.save(img_byte, format='JPEG')
        img_byte = img_byte.getvalue()

        #create unique file name with format
        
        file_id = uuid.uuid4().hex
        file_name = "Image_" + str(file_id)

        '''.format is available in pillow we could use it to fetch the format from uploaded file'''
        file_name = file_name + '.' + img.format

        #upload the file to s3 bucket
        s3_client.upload_fileobj(BytesIO(img_byte), 'fileupload991', file_name)

        #creates a public url to download the image, this link will be available for 1 hr
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': 'fileupload991', 'Key': file_name}, ExpiresIn=3600)
        


        #for url shortening
        url_shortener = URLShortener()

        # Shorten a long URL
        short_url = url_shortener.shorten_url(response)
        
        # store response in database
        '''to add data to database'''
        file_data = uploadedFile(
            fileName = file_name,
            short_url = short_url
        )
        file_data.save()

        #send url to frontend will will used in upload.html 
        context = {
            'uploaded_file_url': response,
            'shortlink':  short_url
        }

        return render(request, 'upload.html', context)
    else:
        return render(request, 'upload.html')




