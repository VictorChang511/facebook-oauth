from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import os
import random, string
import requests

from dotenv import load_dotenv
load_dotenv()

def login(request):
  redirect_uri = request.GET.get('redirect')
  state = ''.join(random.choice(string.ascii_letters) for x in range(10))
  request.session['state'] = state
  request.session['redirect'] = redirect_uri

  permission_url = 'https://www.facebook.com/{api_version}/dialog/oauth??response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}'.format(
    api_version=os.getenv('FACEBOOK_API_VERSION'),
    response_type='code',
    client_id=os.getenv('FACEBOOK_APP_ID'),
    redirect_uri=redirect_uri,
    state=state,
    scope=','.join(['public_profile', 'email', 'ads_management', 'ads_read', 'business_management']),
  )
  return redirect(permission_url)

class CallbackView(APIView):
  def get(self, request):
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    if state == request.session['state']:
      url = 'https://graph.facebook.com/{api_version}/oauth/access_token?client_id={app_id}&client_secret={app_secret}&redirect_uri={redirect_uri}&code={code}'.format(
        api_version=os.getenv('FACEBOOK_API_VERSION'),
        app_id=os.getenv('FACEBOOK_APP_ID'),
        app_secret=os.getenv('FACEBOOK_APP_SECRET'),
        redirect_uri=request.session['redirect'],
        code=code
      )
      try:
        r = requests.get(url)
        access_token = r.json()['access_token']
        print(access_token)
        return Response(status=status.HTTP_200_OK)
      except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)
