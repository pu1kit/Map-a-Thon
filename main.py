#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.ext.webapp import template
import webapp2
import urllib
import json

MAIN_PAGE_HTML = """\
<html>
  <body> 
	{{ft}}  
	Hi !!!!!!!!!!
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
	g = {'ft':"lll"           }
	path = os.path.join(os.path.dirname(__file__), 'main.html')
	self.response.write(template.render(path,g))

    def post(self):
	start_latitude = self.request.get('long_start')
	start_longitude = self.request.get('lat_start')
	end_latitude = self.request.get('long_end')
	end_longitude = self.request.get('lat_end')
	page = urllib.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin="+str(start_latitude)+","+str(start_longitude)+"&destination="+str(end_latitude)+","+str(end_longitude)+"&key=AIzaSyBcv-1eIIy9uIC1hAu2AhtavYy2oKvuqSU")
	data = json.loads(page.read())
	s= start_latitude+","+start_longitude+"|"
	pth = data['routes'][0]['legs'][0]['steps']
	for i in xrange(len(pth)):
	    s = s+str(pth[i]['start_location']['lat'])+","+str(pth[i]['start_location']['lng'])+"|"
	    s = s+str(pth[i]['start_location']['lat'])+","+str(pth[i]['start_location']['lng'])+"|"
	s = s+end_latitude+","+end_longitude
	           
	fg = {
	'url' : "http://maps.google.com/maps/api/staticmap?size=512x512&markers=size:mid|color:red|label:S|"+str(start_latitude)+","+str(start_longitude)+"&markers=size:mid|color:red|label:D|"+str(end_latitude)+","+str(end_longitude)+"&sensor=false&path="+s+"&geodesic=True"

	}
	path2 = os.path.join(os.path.dirname(__file__), 'map.html')
	self.response.write(template.render(path2,fg))    



	
	    
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)