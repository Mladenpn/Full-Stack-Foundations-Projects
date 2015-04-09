from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant/')
def defaultRestaurantMenu():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)
    
    
@app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
    edited_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_restaurant.name = request.form['name']
            session.add(edited_restaurant)
            session.commit
            return redirect(url_for("defaultRestaurantMenu"))
    else:
        return render_template("editRestaurant.html", restaurant_id = restaurant_id, restaurant = edited_restaurant)
        
@app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deleted_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleted_restaurant)
        session.commit
        return redirect(url_for("defaultRestaurantMenu"))
    else:
        return render_template("deleteRestaurant.html", restaurant_id = restaurant_id, restaurant = deleted_restaurant)
        
    



@app.route('/restaurant/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)
    
#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template("newmenuitem.html", restaurant_id = restaurant_id)

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            session.add(editedItem)
            session.commit()
            flash("menu item edited!")
            return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template("editmenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
        
        
        
    

#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template("deletemenuitem.html", restaurant_id = restaurant_id, menu_id = menu_id, item = deletedItem)
    
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
