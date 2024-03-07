from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import uploadedFile
from .urlShortener import URLShortener
import boto3
import os
from PIL import Image
from io import BytesIO
import uuid


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from uploadFile.serializers import CurrentUserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        #fetch refresh token
        refresh = str(RefreshToken.for_user(user))
        return JsonResponse({"refresh":refresh})

class tableView():
    pass
class UserViewSet(viewsets.ViewSet):
    # def list(self, request):
    queryset = User.objects.all()
    serializer = CurrentUserSerializer(queryset, many=True )
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = User.objects.all()
        serializer = CurrentUserSerializer(queryset, many=True)
        return Response(serializer.data)
        # return Response(serializer.data)

    token_obtain_pair = TokenObtainPairView.as_view()
    print(token_obtain_pair)

# Create your views here.
def upload(request):



    if request.method == 'POST':

        s3_client = boto3.client('s3', aws_access_key_id="AKIA6NISAVJ4JKXH3UO2", aws_secret_access_key="jszTf7SA7cL6vvlsyd8TfjzczNKkJi4MIoikptHD")


    # if request.method== 'POST':
    #     s3_client = boto3.client('s3', aws_access_key_id= "", aws_secret_access_key="")
        
        file = request.FILES.get('myfile')
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
            fileName=file_name,
            short_url=short_url,
            file = file,
            url=response

        )
        file_data.save()

        #send url to frontend will be used in upload.html
        context = {
            'uploaded_file_url': response,
            'shortlink':  short_url
        }

        return render(request, 'upload.html', context)
    else:
        return render(request, 'upload.html')



def deleteFile():
    pass

#to delete uploaded file related to user

#we have to store the link in database than fetch the link in frontend based on user that is logged in at
# particular given time.

# create login api
# create token and add it in redis
# create key value pair for user id
# encrypt password and store it in db





# form
#image field
#