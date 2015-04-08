from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			#Objective 3 Step 2 - Create /restarants/new page
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Make a New Restaurant</h1>"
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
				output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>"
				output += "<input type='submit' value='Create'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return
			
			if self.path.endswith("/edit"):
				rest_id = self.path.split("/")[2]
				edited_restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>%s</h1>" % (edited_restaurant.name)
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/edit'>" %rest_id
				output += "<input name = 'editedRestaurantName' type = 'text' placeholder = '%s'>" %edited_restaurant.name
				output += "<input type='submit' value='Rename'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return
				
			if self.path.endswith("/delete"):
				rest_id = self.path.split("/")[2]
				edited_restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1>Are you sure that you want to delete %s?</h1>" % (edited_restaurant.name)
				output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/%s/delete'>" %rest_id
				output += "<input type='submit' value='Delete'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				return	
			

			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				output = ""
				#Objective 3 Step 1 - Create a Link to create a new menu item
				output += "<a href = '/restaurants/new' > >>>Make a New Restaurant Here<<< </a></br></br>"

				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output += "<html><body>"
				output += "<h1> List of Restaurants:</h1>"
				for restaurant in restaurants:
					output += "<h2>%s</h2>" % (restaurant.name,)
					##Objective 2 -- Add Edit and Delete Links
					output += "<a href ='/restaurants/%s/edit' >Edit</a> " % (restaurant.id,)
					output += "</br>"
					output += "<a href ='/restaurants/%s/delete'>Delete</a>" % (restaurant.id,)
					output += "</br></br></br>"

				output += "</body></html>"
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	#Objective 3 Step 3- Make POST method
	def do_POST(self):
		try:
			if self.path.endswith("/delete"):
				rest_id = self.path.split("/")[2]
				edited_restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
				if edited_restaurant:
					session.delete(edited_restaurant)
					session.commit()
					
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()
				
				
			
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile,pdict)
					messagecontent = fields.get('newRestaurantName')

					#Create new Restaurant Object
					newRestaurant = Restaurant(name = messagecontent[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location','/restaurants')
					self.end_headers()
					
			if self.path.endswith("/edit"):				
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile,pdict)
					messagecontent = fields.get('editedRestaurantName')

					#update					
					rest_id = self.path.split("/")[2]
					edit_restaurant = session.query(Restaurant).filter_by(id=rest_id).one()
					if edit_restaurant != []:
						edit_restaurant.name = messagecontent[0]
						session.add(edit_restaurant)
						session.commit()
													
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location','/restaurants')
						self.end_headers()

		except:
			pass

def main():
	try:
		server = HTTPServer(('', 8080), webServerHandler)
		print 'Web server running... Open localhost:8080/restaurants in your browser'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()

if __name__ == '__main__':
	main()
