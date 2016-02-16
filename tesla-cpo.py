
import os
import re
import cgi
import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import memcache
import hashlib
import random
from string import letters, replace
import json
import datetime



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

class BaseHandler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

  def render_json(self, d):
      json_txt = json.dumps(d)
      self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
      self.write(json_txt)

  def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html' 

class Admin(db.Model):
  user_name = db.StringProperty(required=True)
  pw_hash = db.StringProperty(required=True)

  @classmethod
  def login(cls, Username, Password):
    a = Admin.all().filter('user_name =', Username).get()
    if a and valid_pw(Username, Password, a.pw_hash):
      return True

class Cars(db.Model):
  Id = db.StringProperty(required = True)
  Created_at = db.DateTimeProperty(auto_now_add = True)
  Last_Update = db.DateTimeProperty()
  Status = db.StringProperty()
  Location = db.StringProperty()
  Year = db.StringProperty()
  Model = db.StringProperty()
  Mileage = db.FloatProperty()
  Price = db.FloatProperty()
  Paint = db.StringProperty()
  Interior = db.StringProperty()
  Roof = db.StringProperty()
  Wheel = db.StringProperty()
  Pic = db.StringProperty()

  def as_dict(self):
    d = {'Id': self.Id,
          'Created_at': str(self.Created_at),
          'Last_Update': str(self.Last_Update),
          'Status': self.Status,
          'Location': self.Location,
          'Year': self.Year,
          'Model': self.Model,
          'Mileage': self.Mileage,
          'Price': self.Price,
          'Paint': self.Paint,
          'Interior': self.Interior,
          'Roof': self.Roof,
          'Wheel': self.Wheel,
            'Pic': self.Pic}
    return d

class ShowCarsAlt(BaseHandler):
  def get(self):
    if self.format == 'html':
      self.render("base2.html")
    else:
      carlist = Cars.all().run()
      self.render_json([c.as_dict() for c in carlist])

class ShowCars(BaseHandler):
    
  def get(self):
    max_price = 150000
    max_mileage = 80000
    model = "Any"
    location = "Any"
    year = "Any"
    roof = "Any"
    wheel = "Any"
    logging = []
    if self.format == 'html':
      q = Cars.all().filter("Status =", "Active")
      if len(self.request.GET.items()) != 0:
        
        model = self.request.get('Model')
        if model and model != "Any":
          q.filter("Model =", model)
         
        year = self.request.get('Year')
        if year and year != "Any":
          q.filter("Year =", str(year))
         
        location = str(replace(self.request.get('Location'), "+", " ")).replace("%2F", "/")
        if location and location != "Any":
          q.filter("Location =", location)

        wheel = self.request.get('Wheel')
        if wheel and wheel != "Any":
          q.filter("Wheel =", str(wheel))

        roof = self.request.get('Roof')
        if roof and roof != "Any":
          q.filter("Roof =", str(roof))
          
        max_price = float(self.request.get('Price'))
        max_mileage = float(self.request.get('Mileage'))
        q.filter("Mileage <=", max_mileage)
        logging.append(str(max_mileage)) 
        
      
      carlist = q.run()
      finallist = []
      logging.append(str(max_price))
      for car in carlist:
        if car.Price <= max_price:
          finallist.append(car)
      if len(finallist) > 100:
        finallist = finallist[0:100]
      if carlist:
        self.render("index.html", cars=finallist, logging="", max_price=max_price, max_mileage=max_mileage,
                    model=model, year=year, location=location, roof=roof, wheel=wheel, numcars=len(finallist))
      else:
        self.render("index.html", cars="")
    else:
      carlist = Cars.all().filter("Status =", "Active").run()
      self.render_json([c.as_dict() for c in carlist])

class ShowCarsData(BaseHandler):
    
  def get(self):
    max_price = float(self.request.get('Price'))
    data = memcache.get(self.request.path_qs)
    if data is None:
      q = Cars.all().filter("Status =", "Active")
      if len(self.request.GET.items()) != 0:
        
        model = self.request.get('Model')
        if model and model != "Any":
          q.filter("Model =", model)
         
        year = self.request.get('Year')
        if year and year != "Any":
          q.filter("Year =", str(year))
         
        location = str(replace(self.request.get('Location'), "+", " ")).replace("%2F", "/")
        if location and location != "Any":
          q.filter("Location =", location)

        wheel = self.request.get('Wheel')
        if wheel and wheel != "Any":
          q.filter("Wheel =", str(wheel))

        roof = self.request.get('Roof')
        if roof and roof != "Any":
          q.filter("Roof =", str(roof))
          
        max_price = float(self.request.get('Price'))
        max_mileage = float(self.request.get('Mileage'))
        q.filter("Mileage <=", max_mileage)
         
        
      
      carlist = q.fetch(limit=None)
      memcache.add(self.request.path_qs, carlist)
    else:
      carlist = data
    finallist = []
    
    for car in carlist:
      if car.Price <= max_price:
        finallist.append(car)
    self.render_json([c.as_dict() for c in finallist])
    
class AddCars(BaseHandler):
  def get(self):
      self.render("add_form.html")
    
  def post(self):
    if self.format == 'html':
      Id = self.request.get("Id")
      Status = self.request.get("Status")
      Location = self.request.get("Location")
      Year = self.request.get("Year")
      Model = self.request.get("Model")
      Mileage = self.request.get("Mileage")
      Price = self.request.get("Price")
      Paint = self.request.get("Paint")
      Interior = self.request.get("Interior")
      Roof = self.request.get("Roof")
      Wheel = self.request.get("Wheel")
      Pic = self.request.get("Pic")
      Username = self.request.get("Username")
      Password = self.request.get("Password")
      a = Admin.login(Username, Password)
      if a:
        c = Cars(Id=Id, Status=Status, Location=Location, Year=Year, Model=Model,
                Mileage=float(Mileage), Price=float(Price), Paint=Paint, Interior=Interior, Roof=Roof,
                Wheel=Wheel, Pic=Pic)
        c.put()
        self.redirect('/')
      else:
        self.redirect('/')
    else:
      data = json.loads(self.request.body)
      if len(data) > 2:
        a = Admin.login(data[0]["Username"], data[0]["Password"])
        if a:
          cars_to_add = []
          for i in range(1, len(data)):
            c = data[i]
            car = Cars(key_name=c["Id"], Id=c["Id"], Status=c["Status"], Location=c["Location"], Year=c["Year"],
                        Model=c["Model"], Mileage=float(c["Mileage"]), Price=float(c["Price"]),
                         Paint=c["Paint"], Interior=c["Interior"], Roof=c["Roof"], Wheel=c["Wheel"], Pic=c["Pic"])
            cars_to_add.append(car)
          db.put(cars_to_add)
        else:
          self.response.set_status(403)


class Signup(BaseHandler):
  def get(self):
    self.render("edit_form.html")
  
  def post(self):
    Username = self.request.get("Username")
    Password = self.request.get("Password")
    h = make_pw_hash(Username, Password)
    a = Admin(user_name=Username, pw_hash=h)
    a.put()
    self.redirect('/')

class EditCars(BaseHandler):
  def get(self):
      self.render("edit_form.html")
    
  def post(self):
    now = datetime.datetime.now()
    if self.format == 'html':
      Id = self.request.get("Id")
      Status = self.request.get("Status")
      UpDatetime = self.request.get("Datetime")
      Mileage = self.request.get("Mileage")
      Price = self.request.get("Price")
      Username = self.request.get("Username")
      Password = self.request.get("Password")
      a = Admin.login(Username, Password)
      c = Cars.all().filter("Id =", Id).get()
      if a and c:
        c.Status = Status
        c.Last_Update = UpDatetime
        c.Mileage = float(Mileage)
        c.Price = float(Price)
        c.put()
        self.redirect('/')
      else:
        self.redirect('/')
    else:
      data = json.loads(self.request.body)
      if len(data) >= 2:
        a = Admin.login(data[0]["Username"], data[0]["Password"])
        if a:
          cars_to_edit = []
          for i in range(1, len(data)):
            c = data[i]
            car = Cars.all().filter("Id = ", c["Id"]).get()
            car.Status =c["Status"]
            car.Last_Update = now
            car.Location=c["Location"]
            car.Mileage=float(c["Mileage"])
            car.Price=float(c["Price"])
            car.Pic =c["Pic"]
            cars_to_edit.append(car)
          db.put(cars_to_edit)
        else:
          self.response.set_status(403)




#######################################################################################
###########URL HANDLER#################################################################            
app = webapp2.WSGIApplication([ ('/?(?:.json)?', ShowCarsAlt),
                                ('/api/?(?:.json)?', ShowCarsData),
                                ('/add?(?:.json)?', AddCars),
                                ('/edit?(?:.json)?', EditCars),
                                ('/signup', Signup) 
                                ], debug=True)



















    













