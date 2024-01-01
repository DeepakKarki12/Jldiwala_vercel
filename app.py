from flask import Flask, render_template, request, jsonify, Blueprint
from nearest import nearest_5
import os
import json
from flask import Blueprint, redirect, url_for
from extension import db
from flask import jsonify



app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://jldi_wala_db_user:XGqqD7dHgoxsa1lGUuNFcXm8U2O1jyG2@dpg-cm80q7mn7f5s73ec0u3g-a.oregon-postgres.render.com/jldi_wala_db'
app.config["SQLALCHEMY_DATABASE_URI"] =  os.environ.get("DATABASE_URL")
main = Blueprint("__main__",__name__)
db.init_app(app)

app.register_blueprint(main)
from model import YourModel


   


@app.route('/')
def index():
    return render_template('index.html')
   # return "Hello!! deepak from versel"

@app.route('/re', methods=['POST'])
def receive_location():
    print("hello backend")
    if request.method == 'POST':
        print("pst")
        data = request.json  # Extract JSON data from request
        if data:
            latitude = data.get('latitude')
            longitude = data.get('longitude')
# postgresql://jldi_wala_db_user:XGqqD7dHgoxsa1lGUuNFcXm8U2O1jyG2@dpg-cm80q7mn7f5s73ec0u3g-a/jldi_wala_db

            # latitude = 28.350931
            # longitude = 72.941597
            print(f"Received location - Latitude: {latitude}, Longitude: {longitude}")




            obj = nearest_5(latitude,longitude)
            data = obj.main_fun()
            for sublist in data:
                new_entry = YourModel(column_1=sublist[0], column_2=sublist[1])
                # Adjust column assignments based on your data structure
                db.session.add(new_entry)
            db.session.commit()
            # with open('list_file.txt','w') as file:
            #     json.dump(data,file)
            

            return jsonify({'message': 'Location received successfully'})

    else:
        print("get")
        data = request.json
        print(data)
    
    return jsonify({'message': 'Error receiving location'})


@app.route('/mynear')
def near():
    all_data = YourModel.query.all()
    final_list = []
    
    print("alll dataa",all_data)
    for row in all_data[(len(all_data)-4):]:
        row_list = []
        print("row 1",row.column_1)
        row_list.append(row.column_1)
        print("row 2",row.column_2)
        row_list.append(row.column_2)

        final_list.append(row_list)
    print("final list",final_list)

    # data = [f"<li>{ user.column_1 }</li>" for user in users]
    # print('data',data)
    # return f"<ul>{''.join(users_list_html)}</ul>"
    # with open('list_file.txt','r') as file:
    #     data = json.load(file)
    
    # final_list = [['Perfect Bakery', 'Kaladhungi Rd, Pilikothi, Haldwani, Bomari Tallikham, Uttarakhand 263139'],['DG Cakes Arts', 'S BEND, Gas Godam Rd, Kusumkhera, Haldwani']]

    return render_template('different.html',data=final_list)

@app.route('/alldata')
def all():
    all_data = YourModel.query.all()
    final_list = []
    
    print("alll dataa",all_data)
    for row in all_data:
        row_list = []
        print("row 1",row.column_1)
        row_list.append(row.column_1)
        print("row 2",row.column_2)
        row_list.append(row.column_2)

        final_list.append(row_list)
    # print("final list",final_list)
    return render_template('different.html',data=final_list)


@app.route('/add/<user>')
def add(user):
    new_entry = YourModel(column_1=user, column_2="hello")
    # Adjust column assignments based on your data structure
    db.session.add(new_entry)
    db.session.commit()
    all_data = YourModel.query.all()
    single = all_data[-1]
    final_list = []
    row_list = []
    row_list.append(single.column_1)
    row_list.append(single.column_2)    
    final_list.append(row_list)
    return render_template('different.html',data=final_list)



@app.route('/delete')
def delete_all_data():
    try:
        YourModel.query.delete()
        db.session.commit()
        return jsonify({'message': 'All tables deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
