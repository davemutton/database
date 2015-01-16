from django.db import models
from django.core.files import File
from property import keys
import urllib, os, requests,json

# Create your models here.
class Client(models.Model):
   clientUID = models.AutoField(primary_key=True)
   client_name = models.CharField(max_length=255)
   def __unicode__ (self):             
      return self.client_name

class Property(models.Model):
   propertyUID = models.AutoField(primary_key=True)
   client = models.ManyToManyField(Client,blank=True)
   street_address = models.CharField(max_length=255, db_index=True)
   suburb = models.CharField(max_length=120, db_index=True)
   state = models.CharField(max_length=3, db_index=True)
   postcode = models.IntegerField(max_length=4, db_index=True, blank=True)
   date_added = models.DateTimeField(editable=False,auto_now=True)
   baths = models.IntegerField(max_length=2,default=0)
   cars = models.IntegerField(max_length=2,default=0)
   beds = models.IntegerField(max_length=2,default=0)
   imagesourceURL = models.URLField(max_length=255,blank=True)
   imagefile = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
   def __unicode__ (self):             
        return "("+str(self.propertyUID) +") "+ str(self.street_address) +" "+ str(self.suburb) +" "+ str(self.state) + " "+str(self.suburb)
   class meta:
      unique_together = ('street_address', 'suburb','state','postcode')
   def cache(self):
      """Store image locally if we have a URL"""

      if self.imagesourceURL and not self.imagefile:
         result = urllib.urlretrieve(self.imagesourceURL)
         self.imagefile.save(
                 os.path.basename(self.imagesourceURL),
                 File(open(result[0]))
                 )
         self.save()
   def getpostcode(self):
    #if there is no postcode then go and get one using the address
    api_key = keys.auspost_api
    baseurl = 'https://auspost.com.au/api/postcode/search.json?q='
    if not self.postcode:
      try:
        url = baseurl +self.suburb+"&state="+self.state
        headers = {"AUTH-KEY": api_key}
        r = requests.get(url,headers=headers)
        dict = json.loads(r.content)

        try:
          self.postcode = dict['localities']['locality']["postcode"]
        except:
          self.postcode = dict['localities']['locality'][0]["postcode"]
        print "The postcode for " + self.suburb +" in " +self.state+" is "+str(self.postcode)
      except: 
        print "Couldn't find the postcode for " + self.suburb +" in " +self.state
        self.postcode = "0000"
        url = baseurl +self.suburb+"&state="+self.state
        headers = {"AUTH-KEY": api_key}
        r = requests.get(url,headers=headers)
        dict = json.loads(r.content)
        print dict
   def getimages(self):
    if not self.imagefile and not self.imagesourceURL:
      api_key = keys.google_imagesearch_apikey
      cse_id = keys.custome_search_engine_ID
      word = str(self.street_address)+" "+str(self.suburb)+" "+str(self.postcode)+" "+str(self.state)
      print word
      url = "https://www.googleapis.com/customsearch/v1?key=" +api_key +"&cx=" +cse_id +"&q=" +word +"&searchType=image&lr=lang_en"
      print url
      r = requests.get(url)
      json = r.json()
      if json["queries"]["request"][0]["totalResults"] > 0:
        self.imagesourceURL = json["items"][0]['link']

   def save(self, *args, **kwargs):
    self.getpostcode()
    self.getimages()
    self.cache()
    super(Property, self).save(*args, **kwargs)





#Removed because steve said he only wanted to have 1 image per property and having multiple images is far harder. 
#
#class PropertyImage(models.Model):
#   imageUID = models.AutoField(primary_key=True)
#   relatedproperty = models.ForeignKey(Property, related_name='images')
#   imagesourceURL = models.URLField(max_length=255,blank=True) 
#   imagefile = models.ImageField(upload_to='photos/%Y/%m/%d')

