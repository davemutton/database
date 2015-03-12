from django.db import models
from django.core.files import File
from property import keys
import urllib, os, requests,json
from jsonfield import JSONField

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
        return "("+str(self.propertyUID) +") "+ str(self.street_address) +" "+ str(self.suburb) +" "+ str(self.state) + " "+str(self.postcode)
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


# Create your models here.


class QueryJob(models.Model):
  queryUID = models.AutoField(primary_key=True)
  client = models.ManyToManyField(Client,blank=True)
  Json = JSONField()
  street_column =models.TextField()
  state_column =models.TextField(blank=True) 
  suburb_column =models.TextField(blank=True) 
  postcode_column =models.TextField(blank=True) 
  def __unicode__ (self):            
    return "Query number "+ str(self.queryUID)
  def createqueries(self):
    #json_data = json.loads(self.Json)
    print self.Json
    for each in self.Json:
      try:
        Street = each[self.street_column]
        State = each[self.state_column]
        Suburb = each[self.suburb_column]
        Postcode = each[self.postcode_column]
        q = PropertyQuery(street_address = Street, state=State ,suburb = Suburb,postcode=Postcode,queryID=self)
        q.save()
      except:
        pass



  def save(self, *args, **kwargs):
    super(QueryJob, self).save(*args, **kwargs)
    self.createqueries()
    super(QueryJob, self).save(*args, **kwargs)

class PropertyQuery(models.Model):
  queryID = models.ForeignKey(QueryJob,blank=True,null=True)
  linkedproperty = models.ForeignKey(Property,blank=True,null=True)
  street_address = models.CharField(max_length=255, db_index=True,null=True)
  suburb = models.CharField(max_length=120, db_index=True,blank=True,null=True)
  state = models.CharField(max_length=3, db_index=True,blank=True,null=True)
  postcode = models.IntegerField(max_length=4, db_index=True, blank=True,null=True)
  matcheduncertainty = models.PositiveSmallIntegerField(blank=True,null=True)
  def __unicode__ (self):             
    return "(" +str(self.queryID)+") "+self.street_address
  def search_for_a_match(self):
    if self.postcode:
      print self.postcode

      print Property.objects.filter(postcode=self.postcode)
      try:
        property_list = Property.objects.filter(postcode=self.postcode)

        print property_list 
      except:
        print "no properties in that postcode"
        return
    elif self.suburb:
      try:
        property_list = Property.objects.filter(suburb=self.suburb)
        print property_list 
      except:
        print "no properties in that suburb"
    elif self.state:
      try:
        property_list = Property.objects.filter(state=self.state)
        print property_list 
      except:
        print "no properties in that state"
        return
    else:
      print "no properties found"
      return
    for possible in property_list:
      if possible.street_address == self.street_address:
        self.linkedproperty = possible
        self.matcheduncertainty = 100
        return
    else:
      print "we will need to try something else" 




  def save(self, *args, **kwargs):
    super(PropertyQuery, self).save(*args, **kwargs)
    self.search_for_a_match()
    super(PropertyQuery, self).save(*args, **kwargs)













